#!/usr/bin/env python
"""
Python wrapper for zarafa-admin actions
"""
import argparse, textwrap, fnmatch, datetime, getpass
import xml.etree.cElementTree as ElementTree
import subprocess

# Import Brandt Common Utilities
import sys, os
sys.path.append( os.path.realpath( os.path.join( os.path.dirname(__file__), "/opt/brandt/common" ) ) )
import brandt
sys.path.pop()

args = {}
args['output'] = 'text'
args['user'] = ''
args['pass'] = ''
args['action'] = ''
args['actions'] = ['ooo','ooo-enable','ooo-disable','hook','unhook']

args['username'] = ''
args['fullname'] = ''
args['email'] = ''
args['from'] = ''
args['until'] = ''
args['subject'] = ''
args['message'] = ''
args['referer'] = ''

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
      print "Usage: " + self.__prog + " [options] action"
      print "Script used to find details about Zarafa users.\n"
      options = []
      options.append(("-h, --help",           "Show this help message and exit"))
      options.append(("-v, --version",        "Show program's version number and exit"))
      options.append(("-o, --output OUTPUT",  "Type of output {text | xml}"))
      options.append(("-u, --user USER",      "Administrator's username"))
      options.append(("-p, --pass PASSWORD",  "Administrator's password"))
      options.append(("action",               "Action to perform (" + " | ".join(args['actions']) + ")"))
      ooo_options = []      
      ooo_options.append(("    --username USERNAME", "Username of the user to perform action on"))
      ooo_options.append(("    --fullname FULLNAME", "Fullname of the user to perform action on"))
      ooo_options.append(("    --email EMAIL",       "Email of the user to perform action on"))
      ooo_options.append(("    --from DD-MM-YY",     "Date to start Out of Office messages."))
      ooo_options.append(("    --until DD-MM-YY",    "Date to stop Out of Office messages."))
      ooo_options.append(("    --subject SUBJECT",   "Subject of Out of Office messages."))
      ooo_options.append(("    --message MESSAGE",   "Message of Out of Office messages."))
      ooo_options.append(("    --referer REFERER",   "Referer Page."))
      length = max( [ len(option[0]) for option in options ] + [ len(option[0]) for option in ooo_options ] )
      print "Options:"
      for option in options:
        description = textwrap.wrap(option[1], (self.__row - length - 5))
        print "  " + option[0].ljust(length) + "   " + description[0]
      for n in range(1,len(description)): print " " * (length + 5) + description[n]
      print "Out of Office Options:"
      for option in ooo_options:
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
  parser.add_argument('action',
          nargs="*",
          default= args['action'],
          choices= args['actions'],
          help="Action to perform.")

  parser.add_argument('-u', '--user',
          required=False,
          default=args['user'],
          type=str,
          help="Administrator's username")

  parser.add_argument('-p', '--pass',
          required=False,
          default=args['pass'],
          type=str,
          help="Administrator's password")

  parser.add_argument('--username',
          required=False,
          default=args['username'],
          type=str,
          help="Username of the user to perform action on")

  parser.add_argument('--fullname',
          required=False,
          default=args['fullname'],
          type=str,
          help="Fullname of the user to perform action on")

  parser.add_argument('--email',
          required=False,
          default=args['email'],
          type=str,
          help="Email of the user to perform action on")

  parser.add_argument('--from',
          required=False,
          default=args['from'],
          type=str,
          help="Date to start Out of Office messages.")

  parser.add_argument('--until',
          required=False,
          default=args['until'],
          type=str,
          help="Date to stop Out of Office messages.")

  parser.add_argument('--subject',
          required=False,
          default=args['subject'],
          type=str,
          help="Subject of Out of Office messages.")

  parser.add_argument('--message',
          required=False,
          default=args['message'],
          type=str,
          help="Message of Out of Office messages.")

  parser.add_argument('--referer',
          required=False,
          default=args['referer'],
          type=str,
          help="Referer Page.")

  args.update(vars(parser.parse_args()))
  if args['action']: args['action'] = args['action'][0]

def get_input(prompt, type_format = str, stream = sys.stdout.write):
  if str(type(type_format)) == "<type 'str'>" and type_format.lower() == "password":
    tmp = getpass.getpass(prompt)
  else:
    tmp = type_format(raw_input(prompt, stream))
  return tmp

def process_ooo():
  # if not args['username']: args['username'] = get_input("Enter user name: ")

  # if not args['fullname']: args['fullname'] = get_input("Enter " + args['username'] + "'s full name: ")
  # if not args['email']: args['email'] = get_input("Enter " + args['username'] + "'s email: ")
  # if not args['from']: args['from'] = get_input("Enter start date (DD-MM-YYYY): ")
  # if not args['until']: args['until'] = get_input("Enter end date (DD-MM-YYYY): ")
  # if not args['subject']: args['subject'] = get_input("Enter subject: ")
  # if not args['message']: args['message'] = get_input("Enter message: ")

  # if not args['user']: args['user'] = get_input("Enter your user name: ")
  if not args['pass']: args['pass'] = get_input("Enter your password: ", "password")


# Start program
if __name__ == "__main__":
  # try:
    output = ""
    error = ""
    xmldata = ElementTree.Element('error', code="-1", msg="Unknown Error", cmd=brandt.strXML(" ".join(sys.argv)))
    exitcode = 0

    command_line_args()

    if args['action'] == "ooo":
      process_ooo()
    elif args['action'] == "ooo-enable":
      process_ooo_enable()
    elif args['action'] == "ooo-disable":
      process_ooo_disable()
    elif args['action'] == "hook":
      process_hook()
    elif args['action'] == "unhook":
      process_unhook()


  # except SystemExit as err:
  #   pass
  # except Exception as err:
  #   try:
  #     exitcode = int(err[0])
  #     errmsg = str(" ".join(err[1:]))
  #   except:
  #     exitcode = -1
  #     errmsg = str(err)

  #   if args['output'] != 'xml': 
  #     error = "(" + str(exitcode) + ") " + str(errmsg) + "\nCommand: " + " ".join(sys.argv)
  #   else:
  #     xmldata = ElementTree.Element('error', code=brandt.strXML(exitcode), 
  #                                            msg=brandt.strXML(errmsg), 
  #                                            cmd=brandt.strXML(" ".join(sys.argv)))
  # finally:
  #   if args['output'] != 'xml': 
  #     if output: print str(output)
  #     if error:  sys.stderr.write( str(error) + "\n" )
  #   else:
  #     xml = ElementTree.Element('zarafaadmin')
  #     xml.append(xmldata)
  #     print '<?xml version="1.0" encoding="' + encoding + '"?>\n' + ElementTree.tostring(xml, encoding=encoding, method="xml")
  #   sys.exit(exitcode)
