#!/usr/bin/env python
"""
Python wrapper for analyzing at zarafa logs
"""
import argparse, textwrap, fnmatch, datetime
import xml.etree.cElementTree as ElementTree

# Import Brandt Common Utilities
import sys, os
sys.path.append( os.path.realpath( os.path.join( os.path.dirname(__file__), "/opt/brandt/common" ) ) )
import brandt
sys.path.pop()

args = {}
args['output'] = 'text'
args['count'] = 10000
args['log'] = 'system'
args['filters'] = ''
args['sort'] = True
args['list'] = False

version = 0.3
encoding = 'utf-8'

# Logs have roughly 135 (89-165) Bytes per line.
logSizeLimit = 20000 * 135
logDefaults = {'system':{"logfile":"/var/log/syslog","oldlogfile":"/var/log/syslog.1"},
               'zarafa':{"logfile":"/var/log/zarafa/server.log","oldlogfile":"/var/log/zarafa/server.log.1"},
               'mysql':{"logfile":"/var/log/mysql/mysql.log","oldlogfile":"/var/log/mysql/mysql.log.1"},
               'mysql-error':{"logfile":"/var/log/mysql/error.log","oldlogfile":"/var/log/mysql/error.log.1"},
               'mail':{"logfile":"/var/log/mail.log","oldlogfile":"/var/log/mail.log.1"},
               'mail-error':{"logfile":"/var/log/mail.err","oldlogfile":"/var/log/mail.err.1"},               
               'z-push':{"logfile":"/var/log/z-push/z-push.log","oldlogfile":"/var/log/z-push/z-push.log.1"},
               'z-push-error':{"logfile":"/var/log/z-push/z-push-error.log","oldlogfile":"/var/log/z-push/z-push-error.log.1"}}

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
      print "Usage: " + self.__prog + " [options] [filters]"
      print "Script used to analyzing at zarafa logs.\n"
      print "Options:"
      options = []
      options.append(("-h, --help",              "Show this help message and exit"))
      options.append(("-v, --version",           "Show program's version number and exit"))
      options.append(("-o, --output OUTPUT",     "Type of output {text | xml}"))
      options.append(("-c, --count COUNT",       "Max Number of lines to return (Default: " + str(args['count']) + ")"))      
      options.append(("-l, --log LOG",           "Log to analyse {" + " | ".join(sorted(logDefaults.keys())) + "}"))
      options.append(("    --ascending",         "Sort by ascending order."))
      options.append(("    --descending",        "Sort by descending order."))
      options.append(("    --list",              "List the logs available."))
      options.append(("filters",                 "Filters to apply to log."))
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
  parser.add_argument('-o', '--output',
          required=False,
          default=args['output'],
          choices=['text', 'xml'],
          help="Display output type.")
  parser.add_argument('-c', '--count',
          required=False,
          default=args['count'],
          type=int,
          help="Max Number of lines to return.")  
  parser.add_argument('-l', '--log',
          required=False,
          default=args['log'],
          choices=sorted(logDefaults.keys()),
          help="Log to analyse.")
  parser.add_argument('--ascending',
          required=False,
          default=args['sort'],
          action='store_true',
          dest='sort',
          help="Sort by ascending order.")
  parser.add_argument('--descending',
          required=False,
          default=args['sort'],
          action='store_false',
          dest='sort',          
          help="Sort by descending order.")
  parser.add_argument('--list',
          required=False,
          default=args['list'],
          action='store_true',
          help="List the logs available.")  
  parser.add_argument('filters',
          nargs='*',
          default= args['filters'],
          type=str,          
          action='store',
          help="Filters to apply to log.")  
  args.update(vars(parser.parse_args()))
  args['count'] = abs(args['count'])
  tmp = []
  for f in args['filters']:
    for t  in f.split():
      if t: tmp.append(t.lower())
  args['filters'] = " ".join(tmp)

def get_data():
  global args

  size = os.stat(logDefaults[args['log']]['logfile']).st_size
  data = []
  if size < logSizeLimit:
    if os.path.isfile(logDefaults[args['log']]['oldlogfile']):
      f = open(logDefaults[args['log']]['oldlogfile'], 'r')
      data = f.read().split('\n')
      f.close()

  f = open(logDefaults[args['log']]['logfile'], 'r')
  data += f.read().split('\n')[:-1]
  f.close()

  return data

def process_logs(logdata):
  global args

  for f in args['filters'].split():
    if f:
      if f[:6].lower() == "count:" or f[:6].lower() == "count=":
         args['count'] = abs(int(f[6:]))
      elif f[0] == "-":
        for l in reversed(range(len(logdata))):
          if f[1:].lower() in str(logdata[l]).lower():
            del logdata[l]
      else:
        if f[0] == "+": f = f[1:]
        f = str("*" + f + "*").replace("**","*")
        logdata = fnmatch.filter(logdata, f)

  logdata = logdata[-args['count']:]
  if not args['sort']: logdata = logdata[::-1]

  if args['output'] == "text":
    print "\n".join(logdata)
    sys.exit(0)

  xml = ElementTree.Element('log', log=brandt.strXML(brandt.proper(args['log'])), filters=brandt.strXML(args['filters']))
  for line in logdata:
    xmldata = ElementTree.SubElement(xml, "line")
    xmldata.text = brandt.strXML(line)
  return xml

# Start program
if __name__ == "__main__":
  try:
    output = ""
    error = ""
    xmldata = ElementTree.Element('error', code="-1", msg="Unknown Error", cmd=brandt.strXML(" ".join(sys.argv)))
    exitcode = 0

    command_line_args()  

    if args['list']:
      if args['output'] != 'xml':
        output = "\n".join([ str(k) + ", " + str(logDefaults[k]['logfile']) for k in logDefaults.keys() ])
      else:
        xmldata = ElementTree.Element('logs')
        for k in logDefaults.keys():
          ElementTree.SubElement(xmldata, "log", name=brandt.strXML(k), 
                                                 display=brandt.proper(k), 
                                                 location=brandt.strXML(logDefaults[k]['logfile']))
    else:
      logdata = get_data()
      xmldata = process_logs(logdata)

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
