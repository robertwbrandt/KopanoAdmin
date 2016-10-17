#!/usr/bin/env python
"""
Python wrapper for zarafa-admin --list-orphans
"""
import argparse, textwrap, fnmatch, datetime, re
import xml.etree.cElementTree as ElementTree
import subprocess

# Import Brandt Common Utilities
import sys, os
sys.path.append( os.path.realpath( os.path.join( os.path.dirname(__file__), "/opt/brandt/common" ) ) )
import brandt
sys.path.pop()

args = {}
args['output'] = 'text'
args['group'] = ''
args['delimiter'] = ""

version = 0.3
encoding = 'utf-8'

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
      print "Usage: " + self.__prog + " [options]"
      print "Script used to find details about Zarafa orphan stores.\n"
      print "Options:"
      options = []
      options.append(("-h, --help",              "Show this help message and exit"))
      options.append(("-v, --version",           "Show program's version number and exit"))
      options.append(("-o, --output OUTPUT",     "Type of output {text | csv | xml}"))
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
  command = '/usr/sbin/zarafa-admin --list-orphans'
  p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = p.communicate()
  if err: raise IOError(err)

  orphans = []
  for line in out.strip().split('\n')[3:]:
    tmp = re.sub("\t+", "\t", line).strip().split('\t')
    if line and len(tmp) > 4:
      orphans.append({"store":brandt.strXML(tmp[0]), 
                      "username":brandt.strXML(tmp[1]), 
                      "logon":brandt.strXML(tmp[2]), 
                      "size":brandt.strXML(tmp[3]), 
                      "type":brandt.strXML(tmp[4])})
  return orphans

# Start program
if __name__ == "__main__":
  try:
    output = ""
    error = ""
    xmldata = ElementTree.Element('error', code="-1", msg="Unknown Error", cmd=brandt.strXML(" ".join(sys.argv)))
    exitcode = 0

    command_line_args()  

    orphans = get_data()

    if args['output'] == 'text':
      if not args['delimiter']: args['delimiter'] = "\t"
      orphans.insert(0, { "store":"Store GUID", "username":"Guessed Username", "logon":"Last Logon", "size":"Store Size", "type":"Store Type" })      
      width = {"store":0, "username":0, "logon":0, "size":0, "type":0 }
      for orphan in orphans:
        width = { "store":max(len(orphan["store"]),width["store"]), 
                  "username":max(len(orphan["username"]),width["username"]), 
                  "logon":max(len(orphan["logon"]),width["logon"]), 
                  "size":max(len(orphan["size"]),width["size"]), 
                  "type":max(len(orphan["type"]),width["type"]) }

      output = "Zarafa Orphaned Stores (" + str(len(orphans)) + ")\n"
      for orphan in orphans:
        output += str(orphan["store"]).ljust(width["store"]) + args['delimiter'] + \
                  str(orphan["username"]).ljust(width["username"]) + args['delimiter'] + \
                  str(orphan["logon"]).center(width["logon"]) + args['delimiter'] + \
                  str(orphan["size"]).rjust(width["size"]) + args['delimiter'] + \
                  str(orphan["type"]).center(width["type"]) + "\n"
    elif args['output'] == 'csv':
      headers = ( "Store GUID", "Guessed Username", "Last Logon", "Store Size", "Store Type")
      output = args['delimiter'].join(headers) + '\n'
      output += "\n".join([ args['delimiter'].join([o['store'], o['username'], o['logon'], o['size'], o['type']]) for o in orphans ])
    else:
      xmldata = ElementTree.Element('orphans')
      today = datetime.datetime.today()

      for orphan in orphans:
        try:
          logon = datetime.datetime.strptime(orphan.get("logon").decode('unicode_escape'),'%m/%d/%y %H:%M:%S')
          orphan["logon"] = brandt.strXML(logon)
          orphan["lag"] = brandt.strXML((today - logon).days)          
        except:
          logon = datetime.datetime.strptime('01/01/01 00:00:00','%y/%m/%d %H:%M:%S')
          orphan["lag"] = brandt.strXML((today - logon).days)           

        orphan["username"] = orphan["username"].lower()
        orphan["size"] = orphan["size"].split()[0]

        ElementTree.SubElement(xmldata, "orphan", **orphan)

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
