#!/usr/bin/env python
"""
Python wrapper for zarafa-stats --users and zarafa-admin --details user
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
args['output'] = 'text'
args['user'] = ''
args['delimiter'] = ""

version = 0.3
encoding = 'utf-8'

headers = ['company','username','fullname','emailaddress','active','admin','UNK0x67C1001E','size','quotawarn','quotasoft','quotahard','UNK0x67200040','UNK0x6760000B','logon','logoff']

ldapmapping = (("pr_ec_enabled_features","0x67b3101e"),("pr_ec_disabled_features","0x67b4101e"),
               ("pr_ec_archive_servers","0x67c4101e"),("pr_ec_archive_couplings","0x67c5101e"),
               ("pr_ec_exchange_dn","0x678001e"),("pr_business_telephone_number","0x3a08001e"),
               ("pr_business2_telephone_number","0x3a1b101e"),("pr_business_fax_number","0x3a24001e"),
               ("pr_mobile_telephone_number","0x3a1c001e"),("pr_home_telephone_number","0x3a09001e"),
               ("pr_home2_telephone_number","0x3a2f101e"),("pr_primary_fax_number","0x3a23001e"),
               ("pr_pager_telephone_number","0x3a21001e"),("pr_comment","0x3004001e"),
               ("pr_department_name","0x3a18001e"),("pr_office_location","0x3a19001e"),
               ("pr_given_name","0x3a06001e"),("pr_surname","0x3a11001e"),
               ("pr_childrens_names","0x3a58101e"),("pr_business_ddress_city","0x3a27001e"),
               ("pr_title","0x3a17001e"),("pr_user_certificate","0x3a220102"),("pr_initials","0x3a0a001e"),
               ("pr_language","0x3a0c001e"),("pr_organizational_id_number","0x3a10001e"),
               ("pr_postal_address","0x3a15001e"),("pr_company_name","0x3a16001e"),
               ("pr_country","0x3a26001e"),("pr_state_or_province","0x3a28001e"),("pr_street_address","0x3a29001e"),
               ("pr_postal_code","0x3a2a001e"),("pr_post_office_box","0x3a2b001e"),
               ("pr_assistant","0x3a30001e"),("pr_ems_ab_www_home_page","0x8175101e"),
               ("pr_business_home_page","0x3a51001e"),("pr_ems_ab_is_member_of_dl","0x80081102"),
               ("pr_ems_ab_reports","0x800e1102"),("pr_manager_name","0x8005001e"),
               ("pr_ems_ab_owner","0x800c001e"),("size","currentstoresize"),
               ("quotahard","hardlevel"),("quotasoft","softlevel"),("quotawarn","warninglevel"))

fieldmappings = (("username","Username"),("fullname","Fullname"),("emailaddress","Email Address"),
                 ("active","Active"),("administrator","Administrator"),("addressbook","Address Book"),
                 ("autoacceptmeetingreq","Auto-Accept Meeting Req"),("lastlogon","Last Logon"),("lastlogoff","Last Logoff"))

ldapfieldmappings = (("pr_given_name","Given Name"),("pr_initials","Initials"),("pr_surname","Surname"),
                     ("pr_company_name","Company Name"),("pr_title","Title"),("pr_department_name","Department Name"),
                     ("pr_office_location","Office Location"),("pr_business_telephone_number","Business Telephone Number"),
                     ("pr_business2_telephone_number","Business 2 Telephone Number"),("pr_home_telephone_number","Home Telephone Number"),
                     ("pr_home2_telephone_number","Home 2 Telephone Number"),("pr_pager_telephone_number","Pager Telephone Number"),
                     ("pr_primary_fax_number","Primary Fax Number"),("pr_business_fax_number","Business Fax Number"),
                     ("pr_country","Country"),("pr_state_or_province","State or Province"),
                     ("pr_ems_ab_is_member_of_dl","Distribution Lists"),("pr_ec_enabled_features","Enabled Features"),
                     ("pr_ec_disabled_features","Disabled Features"),("pr_assistant","Assistant"),
                     ("pr_business_address_city","Business Address City"),("pr_business_home_page","Business Homepage"),
                     ("pr_childrens_names","Children's Names"),("pr_comment","Comment"),("pr_ec_exchange_dn","Exchange DN"),
                     ("pr_ems_ab_owner","Distribution List Owner"),("pr_ems_ab_reports","Reports"),
                     ("pr_ems_ab_www_home_page","Homepage"),("pr_language","Language"),
                     ("pr_manager_name","Manager"),("pr_mobile_telephone_number","Mobile Telephone Number"),
                     ("pr_organizational_id_number","Organizational ID Number"),("pr_post_office_box","Post Office Box"),
                     ("pr_postal_address","Postal Address"),("pr_postal_code","Postal Code"),
                     ("pr_street_address","Street Address"),("pr_user_certificate","User Certificate"))

quotafieldmappings = (("quotaoverrides"," Quota overrides"),("warninglevel"," Warning level (MB)"),
                      ("softlevel"," Soft level (MB)"),("hardlevel"," Hard level (MB)"),
                      ("currentstoresize","Current store size (MB)"))

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
      print "Script used to find details about Zarafa users.\n"
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
  parser.add_argument('user',
          nargs='?',
          default= args['user'],
          action='store',
          help="User to retrieve details about.")
  args.update(vars(parser.parse_args()))
  if args['delimiter']: args['delimiter'] = args['delimiter'][0]
  if not args['delimiter'] and args['output'] == "csv": args['delimiter'] = ","

def get_data():
  global args
  command = '/usr/bin/zarafa-stats --users --dump'
  cachefile = '/tmp/zarafa-users.cache'    

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
        if headers.index("username") < headers.index("fullname") < len(tmp): 
          if tmp[headers.index("username")] != "SYSTEM":
            if tmp[headers.index("fullname")] != "SYSTEM": continue
      out.pop(c)

    f = open(cachefile, 'w')
    f.write("\n".join(out))
    f.close()
  else:
    f = open(cachefile, 'r')
    out = f.read().split('\n')
    f.close()

  # Apply username filter    
  users = {}
  for line in out:
    if line:
      tmp = line.split(";")
      if args['user']:
        if not fnmatch.fnmatch(tmp[headers.index("username")].lower(), args['user'].lower()): continue
      users[tmp[headers.index("username")].lower()] = line
  out = []
  for user in sorted(users.keys()):
    out.append(users[user])

  return out

def zarafa_users(users):
  global args, output

  if args['output'] == 'text': output +=  out + '\n'
  if args['output'] != 'xml':
    if not args['delimiter']: args['delimiter'] = "\t"
    output += args['delimiter'].join(headers) + '\n'
    output += "\n".join( [ user.replace(";",args['delimiter']) for user in users ] )
  else:
    data = {}
    xml = ElementTree.Element('users')
    today = datetime.datetime.today()

    for user in users:
      tmp = user.split(';')
      attribs = {}
      logon = None
      logoff = None
      for i in range(len(tmp)):
        if tmp[i]:
          if headers[i] == 'logon':
            logon = datetime.datetime.strptime(tmp[i].decode('unicode_escape'),'%a %b %d %H:%M:%S %Y')
          elif headers[i] == 'logoff':
            logoff = datetime.datetime.strptime(tmp[i].decode('unicode_escape'),'%a %b %d %H:%M:%S %Y')
          else:
            attribs[headers[i]] = brandt.strXML(tmp[i])

      xmluser = ElementTree.SubElement(xml, "user", **attribs)
      if logon:  child = ElementTree.SubElement(xmluser, "logon", lag=brandt.strXML((today - logon).days), date=brandt.strXML(logon))
      if logoff: child = ElementTree.SubElement(xmluser, "logoff", lag=brandt.strXML((today - logoff).days), date=brandt.strXML(logoff))
    return xml

def zarafa_user(username):
  global args, ldapmapping, output
  command = '/usr/sbin/zarafa-admin --type user --details "' + str(username) + '"'

  p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = p.communicate()
  if err: raise IOError(err)

  data = str(out).split("\n")
  groups = []
  quotas = []
  props = []
  output = ""  
  for i in reversed(range(len(data))):
    if not data[i]: 
      del data[i]
    else:
      if data[i][:8] == "Groups (":
        groups = data[i:]
        del data[i:]
      elif data[i] == "Current user store quota settings:":
        quotas = data[i:]
        del data[i:]
      elif data[i] == "Mapped properties:":
        props = data[i:]
        del data[i:]

  del groups[0]
  groups = [ str(x).lower().strip() for x in groups ]
  groups.remove("everyone")

  props = [ (str(str(x).split('\t')[1]).lower(), ''.join(str(x).split('\t')[2:])) for x in props[1:] ]
  props = { x[0]:x[1] for x in props }

  data += quotas[1:]
  data = [ str(x).replace(":",":\t",1) for x in data ]
  data = [ ( str(str(x).split('\t')[0]).lower().replace(" ","").replace(":","").replace("-",""), ''.join(str(x).split('\t')[1:]) ) for x in data ]
  data = { x[0]:x[1] for x in data }
  data.update(props)

  data["username"] = data.get("username","").lower()
  data["emailaddress"] = data.get("emailaddress","").lower()
  if data.has_key("warninglevel"): data["warninglevel"] = "{:.0f}".format(float(data.get("warninglevel","").split(" ")[0]) * 1024)
  if data.has_key("softlevel"): data["softlevel"] = "{:.0f}".format(float(data.get("softlevel","").split(" ")[0]) * 1024)
  if data.has_key("hardlevel"): data["hardlevel"] = "{:.0f}".format(float(data.get("hardlevel","").split(" ")[0]) * 1024)
  if data.has_key("currentstoresize"): data["currentstoresize"] = "{:.0f}".format(float(data.get("currentstoresize","").split(" ")[0]) * 1048576)
  logon = None
  if data.has_key("lastlogon"):
    try:
      logon = datetime.datetime.strptime(data.get("lastlogon").decode('unicode_escape'),'%d/%m/%y %H:%M:%S')
    except:
      logon = datetime.datetime.strptime(data.get("lastlogon").decode('unicode_escape'),'%m/%d/%y %H:%M:%S')
    finally:
      data["lastlogon"] = str(logon)
  logoff = None
  if data.has_key("lastlogoff"):
    try:
      logoff = datetime.datetime.strptime(data.get("lastlogoff").decode('unicode_escape'),'%d/%m/%y %H:%M:%S')
    except:
      logoff = datetime.datetime.strptime(data.get("lastlogoff").decode('unicode_escape'),'%m/%d/%y %H:%M:%S')
    finally:
      data["lastlogoff"] = str(logoff)

  for good,bad in ldapmapping:
    if data.has_key(bad):
      data[good] = data[bad]
      del data[bad]

  command = '/usr/sbin/zarafa-admin --type user --list-sendas "' + str(username) + '"'
  p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = p.communicate()
  if err: raise IOError(err)
  sendas = [ str(x).split("\t") for x in str(out).split("\n")[3:] if x ]
 
  mdmCMD = '/opt/brandt/ZarafaAdmin/bin/zarafa-mdm.py --user "' + str(username) + '"'
  if args['output'] == "text":
    maxlen = max([ len(f[1]) for f in fieldmappings ] + [ len(f[1]) for f in quotafieldmappings ] + [ len(f[1]) for f in ldapfieldmappings if data.has_key(f[0]) ] )
    maxlen += 2
    for key,text in fieldmappings:
      output += (text + ":").ljust(maxlen), data.get(key,"") + '\n'

    output += 'Mapped properties:\n'
    for key,text in ldapfieldmappings:
      if data.has_key(key):
        output +=  (" " + text + ":").ljust(maxlen), data[key] + '\n'

    output +=  "Current user store quota settings:\n"
    for key,text in quotafieldmappings:
      output +=  (text + ":").ljust(maxlen), data.get(key,"") + '\n'

    if sendas:
      tmp = [ x[1] + "(" + x[2] + ")" for x in sendas ]
      output +=  "\nSend As Rights (" + str(len(sendas)) + "):" + '\n'
      output +=  '-' * (maxlen + 10) + '\n'
      brandt.printTable(sorted(tmp),2)
      
    if groups:
      output += "\nGroups (" + str(len(groups)) + "):" + '\n'
      output += '-' * (maxlen + 10) + '\n'
      brandt.printTable(sorted(groups),2)

    p = subprocess.Popen(mdmCMD + " --output text", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    mdmSTR, err = p.communicate()
    if err: raise IOError(err)
    mdmLEN = len(mdmSTR.split("\n")) - 2
    if mdmLEN < 0: mdmLEN = 0
    output += "\nMobile Devices (" + str(mdmLEN) + "):" + '\n'
    output += '-' * (maxlen + 10) + '\n'
    output += mdmSTR + '\n'

    sys.exit(0)

  elif args['output'] == "csv":
    tmp = []
    if sendas:
      tmp.append("Send As Rights")
      for i in range(1,len(sendas)): tmp.append('')
    if groups:
      tmp.append("Groups")
      for i in range(1,len(groups)): tmp.append('')
    output += args['delimiter'].join([ f[1] for f in (fieldmappings + quotafieldmappings) ] + tmp) + '\n'

    tmp = []
    if sendas: tmp += sorted([ x[1] + "(" + x[2] + ")" for x in sendas ])
    if groups: tmp += sorted(groups)
    output += args['delimiter'].join([ data.get(f[0],"") for f in (fieldmappings + quotafieldmappings ) ] + tmp ) + '\n'

    sys.exit(0)

  else:
    if data.has_key("lastlogon"): del data["lastlogon"]
    if data.has_key("lastlogoff"): del data["lastlogoff"]

    xml = ElementTree.Element('users')
    today = datetime.datetime.today()
    xmluser = ElementTree.SubElement(xml, "user", **{k:brandt.strXML(v) for k,v in data.items()})
    if logon:  child = ElementTree.SubElement(xmluser, "logon", lag=brandt.strXML((today - logon).days), date=brandt.strXML(logon))
    if logoff: child = ElementTree.SubElement(xmluser, "logoff", lag=brandt.strXML((today - logoff).days), date=brandt.strXML(logoff))
    for send in sendas:
      ElementTree.SubElement(xmluser, 'sendas', username = brandt.strXML(send[1]), fullname = brandt.strXML(send[2]))
    for group in groups:
      ElementTree.SubElement(xmluser, 'group', groupname = brandt.strXML(group))

    try:
      p = subprocess.Popen(mdmCMD + " --output xml", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      mdmSTR, err = p.communicate()
      if err: raise IOError(err)
      xmluser.append(ElementTree.fromstring(mdmSTR).find('devices'))
    except:
      pass

    return xml

# Start program
if __name__ == "__main__":
  try:
    output = ""
    error = ""
    xmldata = ElementTree.Element('error', code="-1", msg="Unknown Error", cmd=brandt.strXML(" ".join(sys.argv)))
    exitcode = 0

    command_line_args()  
    users = get_data()
    if len(users) == 1:
      xmldata = zarafa_user(users[0].split(";")[headers.index("username")])
    else:
      xmldata = zarafa_users(users)

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
