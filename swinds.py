#!/usr/bin/env python


'''
Custom dynamic inventory script for Ansible and Solar Winds, in Python.
This was tested on Python 2.7.6 and Ansible  2.3.0.0.

(c) 2017, Chris Babcock (chris@bluegreenit.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

NOTE:  This software is free to use for any reason or purpose. That said, the
author request that improvements be submitted back to the repo or forked
to something public.  The author reserves the right to chastise, mock,
chide or tease any person or company that does not abide by the spirit of
public sharing.  The author encourages others to do the same within the 
boundaries of good taste of course.

'''
import simplejson
import os
import sys
import argparse
import requests

try:
    import json
except ImportError:
    import simplejson as json


#Orion Server IP or DNS/hostname
server = '10.150.199.44'
#Orion Username
user = 'ansible'
#Orion Password
password = 'akj39.dfjhSHS1poWNMSj8387123h'
#Field for groups
groupField = 'Vendor'
#Field for host
hostField = 'IPAddress'


payload = "query=SELECT+" + hostField + "+," + groupField + "+FROM+Orion.Nodes"
url = "https://" + server + ":17778/SolarWinds/InformationService/v3/Json/Query"
req = requests.get(url, params=payload, verify=False, auth=(user, password))

jsonget = req.json()
#json_resp = json.loads(req)


class SwInventory(object):

    def read_cli(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--host')
        parser.add_argument('--list', action='store_true')
        self.options = parser.parse_args()

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.get_list()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print (json.dumps(self.inventory, indent=2));

    def get_list(self):
        hostsData = jsonget
        dumped = eval(simplejson.dumps(jsonget))


        final_dict= {}

        for m in dumped['results']:
            if m[groupField] in final_dict:
                final_dict[ m[groupField] ]['hosts'].append(m[hostField])
            else:
                final_dict[ m[groupField] ]={'hosts':[m[hostField]]}

        return final_dict

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()

# Get the inventory.
SwInventory()
