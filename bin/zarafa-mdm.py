#!/usr/bin/env python
"""
Python wrapper for z-push-admin.php
"""
import argparse, textwrap, fnmatch, datetime
import xml.etree.cElementTree as ElementTree
import subprocess

# Import Brandt Common Utilities
import sys, os
sys.path.append( os.path.realpath( os.path.join( os.path.dirname(__file__), "/opt/brandt/common" ) ) )
import brandt
sys.path.pop()

args = {}
args['cache'] = 120
args['output'] = 'text'
args['filter'] = ''
args['user'] = ''
args['device'] = ''
args['delimiter'] = ''

version = 0.3
encoding = 'utf-8'

headers = ['deviceid','username','lastsync']
fieldmapping = (("synchronizedbyuser", "Synchronized by user"),("deviceid", "Device ID"),
                ("devicetype", "Device Type"),("devicemodel", "Device Model"),
                ("useragent", "User Agent"),("devicefriendlyname", "Device Friendly Name"),
                ("deviceimei", "Device IMEI"),("deviceos", "Device OS"),
                ("activesyncversion", "ActiveSync Version"),("deviceoperator", "Device Operator"),
                ("deviceoslanguage", "Device Language"),("deviceoutboundsms", "Device Outbound SMS"),
                ("firstsync", "First Sync"),("lastsync", "Last Sync"),
                ("totalfolders", "Total Folders"),("synchronizedfolders", "Synchronized Folders"),
                ("synchronizeddata", "Synchronized Data"),("status", "Status"),
                ("wiperequeston", "Wipe Request On"),("wiperequestby", "Wipe Request By"),
                ("wipedon", "Wiped On"),("attentionneeded", "Attention Needed"))
errormapping = (("brokenobject", "Broken object"),("information", "Information"),
                ("reason", "Reason"),("itemparentid", "Item/Parent id"))

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
      print "Usage: " + self.__prog + " [options] [-d|-u] [FILTER]"
      print "Script used to find details about Zarafa users.\n"
      print "Options:"
      options = []
      options.append(("-h, --help",              "Show this help message and exit"))
      options.append(("-v, --version",           "Show program's version number and exit"))
      options.append(("-o, --output OUTPUT",     "Type of output {text | csv | xml}"))
      options.append(("-c, --cache MINUTES",     "Cache time. (in minutes)"))
      options.append(("    --delimiter DELIM",   "Character to use instead of TAB for field delimiter"))
      options.append(("-d, --device FILTER",     "Apply filter to Device IDs only"))
      options.append(("-u, --user FILTER",       "Apply filter to Usernames only"))
      options.append(("FILTER",                  "Filter to apply to Usernames or Device IDs."))
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
  parser.add_argument('--delimiter',
          required=False,
          default=args['delimiter'],
          type=str,
          help="Character to use instead of TAB for field delimiter")
  parser.add_argument('-o', '--output',
          required=False,
          default=args['output'],
          choices=['text', 'csv', 'xml'],
          help="Display output type.")
  parser.add_argument('-d', '--device',
          required=False,
          default=args['device'],
          type=str,
          help="Apply filter to Device IDs only")
  parser.add_argument('-u', '--user',
          required=False,
          default=args['user'],
          type=str,
          help="Apply filter to Usernames only")            
  parser.add_argument('filter',
          nargs='?',
          default=args['filter'],
          action='store',
          help="Filter to apply to Usernames and Device IDs.")
  args.update(vars(parser.parse_args()))
  if args['delimiter']: args['delimiter'] = args['delimiter'][0]
  if not args['delimiter'] and args['output'] == "csv": args['delimiter'] = ","
  if args['filter']: args['user'] = args['device'] = args['filter']

def get_data():
  global args
  command = '/usr/share/z-push/z-push-admin.php -a lastsync'
  cachefile = '/tmp/zarafa-mdm.cache'    

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

    out = out.split('\n')[5:]
    tmp =[]
    for c in reversed(range(len(out))):
      if out[c]:
        try:
          deviceID, username = out[c].split(" ",1)
          username, lastSync = username.strip().split(" ",1)
          lastSync = lastSync.strip()
          if deviceID and username and lastSync:
            tmp.append(";".join([deviceID, username, lastSync]))
        except:
          pass     
    out = tmp[:]

    f = open(cachefile, 'w')
    f.write("\n".join(out))
    f.close()
  else:
    f = open(cachefile, 'r')
    out = f.read().split('\n')
    f.close()

  # Apply username filter
  if args['device'] or args['user']:
    for c in reversed(range(len(out))):
      if out[c]:
        deviceID, username, lastSync = out[c].split(";")
        if args['device'] and not args['user']:
          if fnmatch.fnmatch(deviceID.lower(), args['device'].lower()): continue
        if not args['device'] and args['user']:
          if fnmatch.fnmatch(username.lower(), args['user'].lower()): continue
        if args['device'] and args['user']:
          if args['device'] == args['user']:
            if fnmatch.fnmatch(deviceID.lower(), args['device'].lower()): continue
            if fnmatch.fnmatch(username.lower(), args['user'].lower()): continue
          else:
            if fnmatch.fnmatch(deviceID.lower(), args['device'].lower()) and fnmatch.fnmatch(username.lower(), args['user'].lower()): continue
      out.pop(c)

  return out

def zarafa_devices(devices):
  global args

  if args['output'] != 'xml':
    if not args['delimiter']: args['delimiter'] = "\t"
    print args['delimiter'].join(headers)
    for device in devices:
      deviceID, username, lastSync = device.split(';')
      print args['delimiter'].join([deviceID, username, lastSync])
    sys.exit(0)

  else:
    xml = ElementTree.Element('devices')
    today = datetime.datetime.today()
    for device in devices:
      deviceID, username, lastSyncText = device.split(';')
      xmldevice = ElementTree.SubElement(xml, "device", deviceid=brandt.strXML(deviceID), username=brandt.strXML(username))
      try:
        lastSync = datetime.datetime.strptime(lastSyncText.decode('unicode_escape'),'%Y-%m-%d %H:%M')
      except:
        lastSync = datetime.datetime.strptime("0001-01-01 00:00".decode('unicode_escape'),'%Y-%m-%d %H:%M')
      child = ElementTree.SubElement(xmldevice, "lastsync", date=brandt.strXML(lastSyncText), lag=brandt.strXML((today - lastSync).days) + '.' + brandt.strXML((today - lastSync).seconds/60) )
    return xml

def parseData(data):
  tmp = {}
  for line in data:
    line = line.lstrip("-")
    if line and ":" in line:
      tag, value = line.split(":",1)
      tag = tag.strip().lower().replace(" ","").replace("/","")
      tmp[tag] = value.strip()
  return tmp

def zarafa_device(deviceID, username):
  global args
  command = '/usr/share/z-push/z-push-admin.php -a list -d "' + deviceID + '" -u "' + username + '"'

  p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = p.communicate()
  if err: raise IOError(err)

  out = out.strip().split("\n")
  error = []
  errors = []

  for c in reversed(range(len(out))):
    line = out[c].lstrip("-")
    if line and line[:17] == 'Attention needed:':
      error = out[c+1:]
      del out[c+1:]
      break

  data = parseData(out)
  for i in reversed(range(len(error))):
    if not error[i]:
      errors.append( parseData(error[i:]) )
      del error[i:]
  if error:
      errors.append( parseData(error[i:]) )

  if args['output'] == 'text':
    width = max( [ len(i[1]) for i in fieldmapping ] ) + 2
    for key, text in fieldmapping:
      if data.has_key(key):
        print (text + ":").rjust(width), data[key]
        if key == "synchronizedbyuser": print "-" * 55
    if errors:
      for error in errors:
        for key, text in errormapping:
          if error.has_key(key):
            print (text + ":").rjust(width), " ", error[key]
        print
    sys.exit(0)
  elif args['output'] == 'csv':
    print args['delimiter'].join( [ i[1] for i in fieldmapping ] )
    print args['delimiter'].join( [ data.get(i[0],"") for i in fieldmapping ] )
    sys.exit(0)
  else:
    xml = ElementTree.Element('devices')
    today = datetime.datetime.today()
    firstsyncText = data.pop("firstsync","never")
    lastsyncText = data.pop("lastsync","never")
    device = ElementTree.SubElement(xml, 'device', **{k:brandt.strXML(v) for k,v in data.items()})

    if firstsyncText:
      try:
        firstsync = datetime.datetime.strptime(firstsyncText.decode('unicode_escape'),'%Y-%m-%d %H:%M')
      except:
        firstsync = datetime.datetime.strptime("0001-01-01 00:00".decode('unicode_escape'),'%Y-%m-%d %H:%M')
      ElementTree.SubElement(device, "firstsync", date=brandt.strXML(firstsyncText), lag=brandt.strXML((today - firstsync).days) + '.' + brandt.strXML((today - firstsync).seconds/60) )
    if lastsyncText:
      try:
        lastsync = datetime.datetime.strptime(lastsyncText.decode('unicode_escape'),'%Y-%m-%d %H:%M')
      except:
        lastsync = datetime.datetime.strptime("0001-01-01 00:00".decode('unicode_escape'),'%Y-%m-%d %H:%M')
      ElementTree.SubElement(device, "lastsync", date=brandt.strXML(lastsyncText), lag=brandt.strXML((today - lastsync).days) + '.' + brandt.strXML((today - lastsync).seconds/60) )

    for error in errors:
      ElementTree.SubElement(device, 'error', **{k:brandt.strXML(v) for k,v in error.items()})
    return xml

# Start program
if __name__ == "__main__":
  try:
    output = ""
    error = ""
    xmldata = ElementTree.Element('error', code="-1", msg="Unknown Error", cmd=brandt.strXML(" ".join(sys.argv)))
    exitcode = 0

    command_line_args()  

    devices = get_data()
    if len(devices) == 1:
      deviceID, username, lastSync = devices[0].split(";")
      xmldata = zarafa_device(deviceID, username)
    else:
      xmldata = zarafa_devices(devices)

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
