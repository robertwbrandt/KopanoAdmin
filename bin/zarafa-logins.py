#!/usr/bin/env python
"""
Python program for Zarafa
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
args['cache'] = 15
args['output'] = "text"
args['delimiter'] = ""
args['scheme'] = 'ldaps'
args['server'] = 'opwdc2.i.opw.ie'
args['base']   = 'ou=opw,dc=i,dc=opw,dc=ie'
args['scope']  = 'sub'

version = 0.3
encoding = 'utf-8'

months = ('','jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec')

attrsTime = { 'm1':  {'min':1,           'label':'Last Minute'},
              'm5':  {'min':5,           'label':'Last 5 Minutes'},
              'm15': {'min':15,          'label':'Last 15 Minutes'},
              'h1':  {'min':1 * 60,      'label':'Last Hour'},
              'h4':  {'min':4 * 60,      'label':'Last 4 Hours'},
              'h8':  {'min':8 * 60,      'label':'Last 8 Hours'},
              'd1':  {'min':1 * 60 * 24, 'label':'Last Day'},
              'd3':  {'min':3 * 60 * 24, 'label':'Last 3 Days'} }

attrsLDAP = { 'cn':                 {'sort':0,  'label':'Windows Name'},
              'samAccountName':     {'sort':1,  'label':'Username'},
              'mail':               {'sort':2,  'label':'Email Address'},
              'badPwdCount':        {'sort':3,  'label':'Bad Password Count'},
              'badPasswordTime':    {'sort':4,  'label':'Bad Password Time'},
              'lastLogon':          {'sort':5,  'label':'Last Logon'},
              'lastlogoff':         {'sort':6,  'label':'Last Logoff'},
              'logonHours':         {'sort':7,  'label':'Logon Hours'},
              'pwdLastSet':         {'sort':8,  'label':'Password Last Set'},
              'accountExpires':     {'sort':9,  'label':'Account Expires'},
              'logonCount':         {'sort':10, 'label':'Logon Count'},
              'lastLogonTimestamp': {'sort':11, 'label':'Last Login Time'} }

class customUsageVersion(argparse.Action):
  def __init__(self, option_strings, dest, **kwargs):
    self.__version = str(kwargs.get('version', ''))
    self.__prog = str(kwargs.get('prog', os.path.basename(__file__)))
    self.__row = min(int(kwargs.get('max', 80)), brandt.getTerminalSize()[0])
    self.__exit = int(kwargs.get('exit', 0))
    super(customUsageVersion, self).__init__(option_strings, dest, nargs=0)
  def __call__(self, parser, namespace, values, option_string=None):
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
      print "Usage: " + self.__prog + " [options] "
      print "Script used to find number of login errors per user.\n"
      print "Options:"
      options = []
      options.append(("-h, --help",              "Show this help message and exit"))
      options.append(("-v, --version",           "Show program's version number and exit"))
      options.append(("-o, --output OUTPUT",     "Type of output {text | csv| xml}"))
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
  global args, attrsTime, attrsLDAP
  cachefile = '/tmp/zarafa-logins.cache'

  args['cache'] *= 60
  age = args['cache'] + 1
  try:
    age = (datetime.datetime.now() - datetime.datetime.fromtimestamp(os.stat(cachefile).st_mtime)).seconds
  except:
    pass

  if age > args['cache']:
    command = 'grep "Authentication by plugin failed for user" "/var/log/zarafa/server.log"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err: raise IOError(err)
    users = {}

    # Troll the logs to find users failed logins and count the occurances
    for line in out.split('\n'):
      try:
        now =  datetime.datetime.now()        
        tmp = line.replace("  "," ").replace(" ",":").split(":")
        tmpTime = datetime.datetime( int(tmp[6]), months.index(tmp[1].lower()), int(tmp[2]), int(tmp[3]), int(tmp[4]), int(tmp[5]) )
        tmpUser = tmp[-1].lower()
        if not users.has_key(tmpUser): users[tmpUser] = {'user':tmp[-1]}
        for attr in attrsTime.keys():
          if tmpTime > now - datetime.timedelta(minutes = attrsTime[attr]['min']): users[tmpUser].update( {attr: users[tmpUser].get(attr,0) + 1})
      except:
        pass

    # Remove users who's login failures occurred too long ago and convert integer values to strings
    for user in users.keys():
      if len(users[user]) == 1: 
        del users[user]
      else:
        for attr in attrsTime.keys():
          if users[user].has_key(attr): users[user][attr] = str(users[user][attr])

    # Retrieve LDAP values for remaining users
    for user in users.keys():
      try:
        ldapURI  = args['scheme'] + "://" + args['server'] + "/" 
        ldapURI += args['base'] + "?" + ",".join(attrsLDAP.keys()) + "?" + args['scope'] + "?sAMAccountName=" + user
        results = brandt.LDAPSearch(ldapURI).results
        if str(results[0][1]['sAMAccountName'][0]).lower() == user:
          for key in results[0][1]:
            try:
              value = results[0][1][key][0]
              key = key.lower()
              if key in ['badpasswordtime','lastlogoff','lastlogon','pwdlastset','lastlogontimestamp','accountexpires']:
                value = str(datetime.datetime(1601,1,1) + datetime.timedelta(microseconds=( int(value)/10) ))[:19]
                if value == '1601-01-01 00:00:00': value = 'never'
              elif key == 'logonhours':
                tmp = ""
                for char in value:
                  tmp += str(hex(ord(char))[2:]).upper()
                value = tmp
              users[user][key] = brandt.strXML(value)
            except:
              pass
      except:
        pass

    attrs = sorted(attrsTime, key = lambda x: attrsTime[x]['min']) + [ a.lower() for a in sorted(attrsLDAP, key = lambda x: attrsLDAP[x]['sort']) ]
    f = open(cachefile, 'w')
    for user in sorted(users.keys()):
      f.write(user)
      for attr in attrs:
        f.write( "," + str(users[user].get(attr,"")) )
      f.write("\n")
    f.close()
  else:
    f = open(cachefile, 'r')
    out = f.read().strip().split('\n')
    f.close()

    users = {}
    for line in out:
      if line:
        c=0
        line = line.split(",")
        user = str(line[c]).lower()
        tmp={"user":line[c]}
        attrs = sorted(attrsTime, key = lambda x: attrsTime[x]['min']) + [ a.lower() for a in sorted(attrsLDAP, key = lambda x: attrsLDAP[x]['sort']) ]
        for attr in attrs:
          c += 1
          if str(line[c]): tmp[attr] = str(line[c])
        users[user] = tmp.copy()

  return users

def format_users(users):
  global args
  output = ""
  error = ""
  xmldata = ""
  exitcode = 1

  if args['output'] == "text":
    usermaxlen = max( [ len(x) for x in users.keys() ] + [18] )

    for key, label in [ (k, attrsTime[k]['label']) for k in sorted(attrsTime.keys(),key = lambda x: int(attrsTime[x]['min'])) ]:
      tmp = sorted([ u for u in users.keys() if users[u].get(key, 0) > 0 ], key = lambda u: int(users[u][key]), reverse = True)
      if tmp:
        output = str(label).center(usermaxlen + 18) + "\n"
        output += "Username".ljust(usermaxlen) + "  Count" + "\n"
        output += "-" * (usermaxlen + 18) + "\n"
        for u in tmp:
          output += str(u).ljust(usermaxlen) + "  " + str(users[u][key]).rjust(5) + "\n"
        output += "\n"
        
    for user in sorted(users.keys()):
      if users[user].get('samaccountname','') and users[user].get('cn',''):
        output += "User information for " + users[user]['samaccountname'].lower() + " (" + users[user]['cn'] +"):\n" + ("-" * (usermaxlen + 18)) + "\n"
        for key, label in [ (str(k).lower(), attrsLDAP[k]['label']) for k in sorted(attrsLDAP.keys(),key = lambda x: attrsLDAP[x]['sort']) ]:
          if key not in ['cn','samaccountname']:
            output += str(label).rjust(18) + ": " + str(users[user].get(key,"")) + "\n"
        output += "\n"
    exitcode = 0

  elif args['output'] == "csv":
    output  = args['delimiter'].join([ attrsTime[k]['label'] for k in sorted(attrsTime.keys(), key = lambda x: attrsTime[x]['min']) ])
    output += args['delimiter']
    output += args['delimiter'].join([ attrsLDAP[k]['label'] for k in sorted(attrsLDAP.keys(), key = lambda x: attrsLDAP[x]['sort']) ])
    output += "\n"

    attrs = sorted(attrsTime, key = lambda x: attrsTime[x]['min']) + [ a.lower() for a in sorted(attrsLDAP, key = lambda x: attrsLDAP[x]['sort']) ]
    for user in sorted(users.keys()):
      output += user + args['delimiter']
      for attr in attrs:
        output += args['delimiter'] + str(users[user].get(attr,""))
      output += "\n"
    exitcode = 0

  else:

    xmldata = ElementTree.Element('log', log='Login Errors', filters='')
    for user in sorted(users.keys()):
      ElementTree.SubElement(xmldata, "user", **{ k:brandt.strXML(v) for k,v in users[user].items() })
    exitcode = 0

  return output, error, xmldata, exitcode

# Start program
if __name__ == "__main__":
  try:
    output = ""
    error = ""
    xmldata = ElementTree.Element('error', code="-1", msg="Unknown Error", cmd=brandt.strXML(" ".join(sys.argv)))
    exitcode = 0

    command_line_args()
    output, error, xmldata, exitcode = format_users(get_data())

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
      print output
      if exitcode or error: sys.stderr.write(error + "\n")
    else:
      xml = ElementTree.Element('zarafaadmin')
      if xmldata: xml.append(xmldata)
      print '<?xml version="1.0" encoding="' + encoding + '"?>\n' + ElementTree.tostring(xml, encoding=encoding, method="xml")
