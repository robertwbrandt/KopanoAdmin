#!/usr/bin/env python
"""
Python wrapper for zarafa-stats --system
"""
import argparse, textwrap, datetime
import xml.etree.cElementTree as ElementTree
import subprocess

# Import Brandt Common Utilities
import sys, os
sys.path.append( os.path.realpath( os.path.join( os.path.dirname(__file__), "/opt/brandt/common" ) ) )
import brandt
sys.path.pop()

args = {}
args['cache'] = 5
args['output'] = 'text'
args['user'] = ''
args['delimiter'] = ""

version = 0.3
encoding = 'utf-8'

headers = ['parameter','description','value']

class customUsageVersion(argparse.Action):
  def __init__(self, option_strings, dest, **kwargs):
    self.__version = str(kwargs.get('version', ''))
    self.__prog = str(kwargs.get('prog', os.path.basename(__file__)))
    self.__row = min(int(kwargs.get('max', 80)), brandt.getTerminalSize()[0])
    self.__exit = int(kwargs.get('exit', 0))
    super(customUsageVersion, self).__init__(option_strings, dest, nargs=0)
  def __call__(self, parser, namespace, values, option_string=None):
    # print('%r %r %r' % (namespace, values, option_string))
    if self.__version:
      print self.__prog + " " + self.__version
      print "Copyright (C) 2013 Free Software Foundation, Inc."
      print "License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>."
      version  = "This program is free software: you can redistribute it and/or modify "
      version += "it under the terms of the GNU General Public License as published by "
      version += "the Free Software Foundation, either version 3 of the License, or "
      version += "(at your option) any later version."
      print textwrap.fill(version, self.__row)
      version  = "This program is distributed in the hope that it will be useful, "
      version += "but WITHOUT ANY WARRANTY; without even the implied warranty of "
      version += "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the "
      version += "GNU General Public License for more details."
      print textwrap.fill(version, self.__row)
      print "\nWritten by Bob Brandt <projects@brandt.ie>."
    else:
      print "Usage: " + self.__prog + " [options] [username]"
      print "Script used to find details about Zarafa system.\n"
      print "Options:"
      options = []
      options.append(("-h, --help",              "Show this help message and exit"))
      options.append(("-v, --version",           "Show program's version number and exit"))
      options.append(("-o, --output OUTPUT",     "Type of output {text | csv | xml}"))
      options.append(("-c, --cache MINUTES",     "Cache time. (in minutes)"))
      options.append(("-d, --delimiter DELIM",   "Character to use instead of TAB for field delimiter"))
      length = max( [ len(option[0]) for option in options ] )
      for option in options:
        description = textwrap.wrap(option[1], (self.__row - length - 5))
        print "  " + option[0].ljust(length) + "   " + description[0]
      for n in range(1,len(description)): print " " * (length + 5) + description[n]
    exit(self.__exit)
def command_line_args():
  global args, version
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument('-v', '--version', action=customUsageVersion, version=version, max=80)
  parser.add_argument('-h', '--help', action=customUsageVersion)
  parser.add_argument('-c', '--cache',
          required=False,
          default=args['cache'],
          type=int,
          help="Cache time. (in minutes)")
  parser.add_argument('-d', '--delimiter',
          required=False,
          default=args['delimiter'],
          type=str,
          help="Character to use instead of TAB for field delimiter")
  parser.add_argument('-o', '--output',
          required=False,
          default=args['output'],
          choices=['text', 'csv', 'xml'],
          help="Display output type.")
  args.update(vars(parser.parse_args()))
  if args['delimiter']: args['delimiter'] = args['delimiter'][0]
  if not args['delimiter'] and args['output'] == "csv": args['delimiter'] = ","

def get_data():
  global args
  command = '/usr/bin/zarafa-stats --system --dump'
  cachefile = '/tmp/zarafa-system.cache'    

  args['cache'] *= 60
  age = args['cache'] + 1
  try:
    age = (datetime.datetime.now() - datetime.datetime.fromtimestamp(os.stat(cachefile).st_mtime)).seconds
  except:
    pass

  if age > args['cache']:
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err: raise IOError(err)

    out = out.strip().split('\n')[1:]
    for c in reversed(range(len(out))):
      if out[c]:
        tmp = out[c].split(";")
        if len(tmp) == 3: continue
      out.pop(c)

    f = open(cachefile, 'w')
    f.write("\n".join(out))
    f.close()
  else:
    f = open(cachefile, 'r')
    out = f.read().split('\n')
    f.close()

  return out

def zarafa_system(data):
  global args

  if args['output'] == 'csv':
    print args['delimiter'].join([ line.split(";")[0] for line in data ])
    print args['delimiter'].join([ line.split(";")[2] for line in data ])
    sys.exit(0)

  elif args['output'] == 'text':
    if not args['delimiter']: args['delimiter'] = "\t"
    width = max( [ len(line.split(";")[1]) for line in data ] )
    for line in data:
      parameter, desc, value = line.split(";")
      if parameter in ['server_start_date','cache_purge_date','config_reload_date','sql_last_fail_time']:
        if value:
          value = str(datetime.datetime.strptime(value.decode('unicode_escape'),'%a %b %d %H:%M:%S %Y'))
      print str(desc).ljust(width) + args['delimiter'] + str(value)
    sys.exit(0)

  else:
    attrib = {}
    dates = {}

    for line in data:
      parameter, desc, value = line.split(";")
      if parameter in ['server_start_date','cache_purge_date','config_reload_date','sql_last_fail_time']:
        try:
          dates[parameter] = {}
          dates[parameter]['text'] = value
          dates[parameter]['date'] = datetime.datetime.strptime(value.decode('unicode_escape'),'%a %b %d %H:%M:%S %Y')
        except:
          dates[parameter] = {}          
          dates[parameter]['text'] = value
          dates[parameter]['date'] = datetime.datetime.strptime("0001-01-01 00:00".decode('unicode_escape'),'%Y-%m-%d %H:%M')

      else:
        attrib[parameter] = brandt.strXML(value)

    xml = ElementTree.Element('system', **attrib)
    today = datetime.datetime.today()
    for parameter in ['server_start_date','cache_purge_date','config_reload_date','sql_last_fail_time']:
      if dates.has_key(parameter) and dates[parameter].get('text',""): 
        ElementTree.SubElement(xml, parameter, date=brandt.strXML(dates[parameter]['text']), lag=brandt.strXML((today - dates[parameter]['date']).days) + '.' + brandt.strXML((today - dates[parameter]['date']).seconds/60) )

    return xml

# Start program
if __name__ == "__main__":
  try:
    output = ""
    error = ""
    xmldata = ElementTree.Element('error', code="-1", msg="Unknown Error", cmd=brandt.strXML(" ".join(sys.argv)))
    exitcode = 0

    command_line_args()  

    xmldata = zarafa_system(get_data())

  except SystemExit as err:
    pass
  except Exception as err:
    try:
      exitcode = int(err[0])
      errmsg = str(" ".join(err[1:]))
    except:
      exitcode = -1
      errmsg = str(err)

    if args['output'] != 'xml': 
      error = "(" + str(exitcode) + ") " + str(errmsg) + "\nCommand: " + " ".join(sys.argv)
    else:
      xmldata = ElementTree.Element('error', code=brandt.strXML(exitcode), 
                                             msg=brandt.strXML(errmsg), 
                                             cmd=brandt.strXML(" ".join(sys.argv)))
  finally:
    if args['output'] != 'xml': 
      if output: print str(output)
      if error:  sys.stderr.write( str(error) + "\n" )
    else:
      xml = ElementTree.Element('zarafaadmin')
      xml.append(xmldata)
      print '<?xml version="1.0" encoding="' + encoding + '"?>\n' + ElementTree.tostring(xml, encoding=encoding, method="xml")
    sys.exit(exitcode)
