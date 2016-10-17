#!/usr/bin/env python
"""
Python wrapper for zarafa-admin --user-count
"""
import argparse, textwrap, fnmatch, datetime, json
import xml.etree.cElementTree as ElementTree
import subprocess

# Import Brandt Common Utilities
import sys, os
sys.path.append( os.path.realpath( os.path.join( os.path.dirname(__file__), "/opt/brandt/common" ) ) )
import brandt
sys.path.pop()

args = {}
args['output'] = 'text'
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
      print "Script used to find details about Zarafa licensing.\n"
      print "Options:"
      options = []
      options.append(("-h, --help",              "Show this help message and exit"))
      options.append(("-v, --version",           "Show program's version number and exit"))
      options.append(("-o, --output OUTPUT",     "Type of output {text | csv | xml | json}"))
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
          choices=['text', 'csv', 'xml', 'json'],
          help="Display output type.")
  args.update(vars(parser.parse_args()))
  if args['delimiter']: args['delimiter'] = args['delimiter'][0]
  if not args['delimiter'] and args['output'] == "csv": args['delimiter'] = ","

def get_data():
  command = '/usr/sbin/zarafa-admin --user-count'
  p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = p.communicate()
  if err: raise IOError(err)

  data = {'active': {'used': '0', 'available': '', 'allowed': '', 'users': '', 'rooms': '', 'equipment': ''},
          'non-active': {'used': '0', 'available': '', 'allowed': '', 'users': '', 'rooms': '', 'equipment': ''},
          'total': {'used': '0', 'available': '', 'allowed': '', 'users': '', 'rooms': '', 'equipment': ''}}

  for line in out.split('\n')[3:]:
    line = line.split()
    if line:
      line[0] = str(line[0]).strip().lower()
      if line[0] == 'active' and len(line) > 3:
        data['active'].update({'allowed':line[1], 'used':line[2], 'available':line[3]})
      elif line[0] == 'non-active' and len(line) > 3:
        data['non-active'].update({'allowed':line[1], 'used':line[2], 'available':line[3]})
      elif line[0] == 'users' and len(line) > 1:
        data['non-active'].update({'users':line[1]})
      elif line[0] == 'rooms' and len(line) > 1:
        data['non-active'].update({'rooms':line[1]})
      elif line[0] == 'equipment' and len(line) > 1:
        data['non-active'].update({'equipment':line[1]})
      elif line[0] == 'total' and len(line) > 1:
        data['total'].update({'used':line[1]})

  return data

# Start program
if __name__ == "__main__":
  try:
    error = ""
    xmldata = ""
    exitcode = 0
    lic = {}

    command_line_args()
    lic = get_data()

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
    if args['output'] == 'xml': 
      xml = ElementTree.Element('zarafaadmin')
      if xmldata: xml.append(xmldata)
      xmllic = ElementTree.SubElement(xml, 'license')
      ElementTree.SubElement(xmllic, "active", **lic['active'])
      ElementTree.SubElement(xmllic, "nonactive", **lic['non-active'])
      ElementTree.SubElement(xmllic, "total", **lic['total'])
      print '<?xml version="1.0" encoding="' + encoding + '"?>\n' + ElementTree.tostring(xml, encoding=encoding, method="xml")
    else:
      if error:
        sys.stderr.write( str(error) + "\n" )
      elif lic:
        if args['output'] == 'json': 
          print json.dumps(lic, indent=2, sort_keys=True)

        elif args['output'] == 'csv':
          print args['delimiter'].join(['Type','Used','Available','Allowed','Users','Rooms','Equipment'])
          print args['delimiter'].join(['active',lic['active']['used'],lic['active']['available'],lic['active']['allowed'],
                                                 lic['active']['users'],lic['active']['rooms'],lic['active']['equipment']])
          print args['delimiter'].join(['non-active',lic['non-active']['used'],lic['non-active']['available'],lic['non-active']['allowed'],
                                                     lic['non-active']['users'],lic['non-active']['rooms'],lic['non-active']['equipment']])
          print args['delimiter'].join(['total',lic['total']['used'],lic['total']['available'],lic['total']['allowed'],
                                                lic['total']['users'],lic['total']['rooms'],lic['total']['equipment']])
          if error:  sys.stderr.write( str(error) + "\n" )      

        else:
          allowed   = max([7, len(lic['active']['allowed']), len(lic['non-active']['allowed'])]) + 2
          used      = max([7, len(lic['active']['used']), len(lic['non-active']['used']), len(lic['total']['used'])]) + 2
          available = max([9, len(lic['active']['available']), len(lic['non-active']['available'])]) + 2
          print "Zarafa Licensing Info:"
          print "           " + "Allowed".rjust(allowed) + "Used".rjust(used) + "Available".rjust(available)
          print "-----------" + "-" * (allowed + used + available + 2)
          print "Active     " + str(lic['active']['allowed']).rjust(allowed) + str(lic['active']['used']).rjust(used) + str(lic['active']['available']).rjust(available)
          print "Non-active " + str(lic['non-active']['allowed']).rjust(allowed) + str(lic['non-active']['used']).rjust(used) + str(lic['non-active']['available']).rjust(available)
          print "  Users    " + str(lic['non-active']['users']).rjust(allowed + used)
          print "  Rooms    " + str(lic['non-active']['rooms']).rjust(allowed + used)
          print "  Equipment" + str(lic['non-active']['equipment']).rjust(allowed + used)
          print "Total      " + str(lic['total']['used']).rjust(allowed + used)
    sys.exit(exitcode)
