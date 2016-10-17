#!/usr/bin/env python
"""
Python script to replicate kopano-admin for user information. 
"""
import kopano
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

k = kopano.Server()

for user in k.users():
    print user.name


