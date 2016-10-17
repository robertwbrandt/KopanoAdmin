#!/usr/bin/env python
"""
Python wrapper for zarafa-admin --type group --details group
"""
import argparse, textwrap, fnmatch, datetime
import xml.etree.cElementTree as ElementTree
import subprocess
from multiprocessing import Process, Queue

# Import Brandt Common Utilities
import sys, os
sys.path.append( os.path.realpath( os.path.join( os.path.dirname(__file__), "/opt/brandt/common" ) ) )
import brandt
sys.path.pop()

args = {}
args['cache'] = 15
args['output'] = 'text'
args['group'] = ''
args['delimiter'] = ""

version = 0.3
encoding = 'utf-8'

fieldmappings = (("groupname","Group Name"),("fullname","Fullname"),
                 ("emailaddress","Email Address"),("addressbook","Address Book"))

ldapfieldmappings = (("pr_ec_enabled_features","Enabled Features"),("pr_ec_disabled_features","Disabled Features"))


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
      print "Script used to find details about Zarafa user perissions.\n"
      print "Options:"
      options = []
      options.append(("-h, --help",              "Show this help message and exit"))
      options.append(("-v, --version",           "Show program's version number and exit"))
      options.append(("-o, --output OUTPUT",     "Type of output {text | csv | xml}"))
      options.append(("-c, --cache MINUTES",     "Cache time. (in minutes)"))
      options.append(("-d, --delimiter DELIM",   "Character to use instead of TAB for field delimiter"))
      options.append(("username",                "Filter to apply to usernames."))
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
  parser.add_argument('group',
          nargs='?',
          default= args['group'],
          action='store',
          help="Group to retrieve details about.")
  args.update(vars(parser.parse_args()))
  if args['delimiter']: args['delimiter'] = args['delimiter'][0]
  if not args['delimiter'] and args['output'] == "csv": args['delimiter'] = ","

def get_data():
  global args
  command = 'zarafa-mailbox-permissions --list-permissions-per-folder brandtb'
  cachefile = '/tmp/zarafa-mailbox-permissions.cache'    

  args['cache'] *= 60
  age = args['cache'] + 1
  try:
    age = (datetime.datetime.now() - datetime.datetime.fromtimestamp(os.stat(cachefile).st_mtime)).seconds
  except:
    pass

  if age > args['cache']:
    p = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err: raise IOError(err)

  out = out.split("\n")

  permissions = []
  SendMeetingRequest = ""
  delegate = []
  for c in reversed(range(len(out))):
    if out[c]:
      if out[c] == "Folder permissions:":
        permissions = out[c:]
        del out[c:]
      elif out[c][:83] == "Send meeting requests and response only to the delegator, not to the mailbox owner.":
        SendMeetingRequest = out[c]
        out.pop(c)
      elif out[c] == "Delegate information:":
        delegate = out[c:]
        del out[c:]
    else:
      out.pop(c)

  delegate = delegate[4:-1]
  permissions = permissions[4:-1]


  print "\n".join(delegate)
  print SendMeetingRequest
  print "\n".join(permissions)


  # print out



















  #   out = out.strip().split('\n')[3:]
  #   for c in reversed(range(len(out))):
  #     if out[c]:
  #       out[c] = out[c].strip()
  #       if out[c] != "Everyone": continue
  #     out.pop(c)
  #   out = sorted(out, key=lambda s: s.lower())

  #   f = open(cachefile, 'w')
  #   f.write("\n".join(out))
  #   f.close()
  # else:
  #   f = open(cachefile, 'r')
  #   out = f.read().split('\n')
  #   f.close()

  # # Apply groupname filter
  # if args['group']:  
  #   for c in reversed(range(len(out))):
  #     if out[c] and fnmatch.fnmatch(out[c].lower(), args['group'].lower()): continue
  #     out.pop(c)

  return out






# Start program
if __name__ == "__main__":
    command_line_args()

    exitcode = 0
  # try:
    permissions = get_data()
    # if len(groups) == 1:
    #   xmldata = zarafa_group(groups[0])
    # else:
    #   xmldata = zarafa_groups(groups)

    # if args['output'] == 'xml': 
    #   xml = ElementTree.Element('zarafaadmin')
    #   xml.append(xmldata)
    #   print '<?xml version="1.0" encoding="' + encoding + '"?>\n' + ElementTree.tostring(xml, encoding=encoding, method="xml")

  # except ( Exception, SystemExit ) as err:
  #   try:
  #     exitcode = int(err[0])
  #     errmsg = str(" ".join(err[1:]))
  #   except:
  #     exitcode = -1
  #     errmsg = str(" ".join(err))

  #   if args['output'] != 'xml': 
  #     if exitcode != 0: sys.stderr.write( str(err) +'\n' )
  #   else:
  #     xml = ElementTree.Element('zarafaadmin')      
  #     xmldata = ElementTree.SubElement(xml, 'error', errorcode = str(exitcode) )
  #     xmldata.text = errmsg
  #     print '<?xml version="1.0" encoding="' + encoding + '"?>\n' + ElementTree.tostring(xml, encoding=encoding, method="xml")

  # sys.exit(exitcode)