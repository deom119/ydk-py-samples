#!/usr/bin/env python
#
# Copyright 2016 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Set configuration for model Cisco-IOS-XR-ipv4-acl-cfg.

usage: gn-set-xr-ipv4-acl-cfg-32-ydk.py [-h] [-v] device

positional arguments:
  device         gNMI device (http://user:password@host:port)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.path import Repository
from ydk.filters import YFilter
from ydk.gnmi.services import gNMIService
from ydk.gnmi.providers import gNMIServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_acl_cfg \
    as xr_ipv4_acl_cfg
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_acl_datatypes \
    as xr_ipv4_acl_datatypes
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")

def config_ipv4_acl_and_prefix_list(ipv4_acl_and_prefix_list):
    """Add config data to ipv4_acl_and_prefix_list object."""
    access = ipv4_acl_and_prefix_list.accesses.Access()
    access.access_list_name = "ACL2"
    access.access_list_entries = access.AccessListEntries()

    # access-list with sequence number 10
    access_list_entry = access.access_list_entries.AccessListEntry()
    access_list_entry.sequence_number = 10
    access_list_entry.remark = "allow multiple hosts"
    access.access_list_entries.access_list_entry.append(access_list_entry)

    # access-list with sequence number 20
    access_list_entry = access.access_list_entries.AccessListEntry()
    access_list_entry.sequence_number = 20
    access_list_entry.grant = xr_ipv4_acl_datatypes.Ipv4AclGrantEnum.permit
    access_list_entry.source_network.source_address = "172.31.255.1"
    access_list_entry.source_network.source_wild_card_bits = "0.0.0.0"
    access.access_list_entries.access_list_entry.append(access_list_entry)
    
    # access-list with sequence number 30
    access_list_entry = access.access_list_entries.AccessListEntry()
    access_list_entry.sequence_number = 30
    access_list_entry.grant = xr_ipv4_acl_datatypes.Ipv4AclGrantEnum.permit
    access_list_entry.source_network.source_address = "172.31.255.33"
    access_list_entry.source_network.source_wild_card_bits = "0.0.0.0"
    access.access_list_entries.access_list_entry.append(access_list_entry)

    # access-list with sequence number 40
    access_list_entry = access.access_list_entries.AccessListEntry()
    access_list_entry.sequence_number = 40
    access_list_entry.grant = xr_ipv4_acl_datatypes.Ipv4AclGrantEnum.permit
    access_list_entry.source_network.source_address = "172.31.255.65"
    access_list_entry.source_network.source_wild_card_bits = "0.0.0.0"
    access.access_list_entries.access_list_entry.append(access_list_entry)

    # access-list with sequence number 50
    access_list_entry = access.access_list_entries.AccessListEntry()
    access_list_entry.sequence_number = 50
    access_list_entry.grant = xr_ipv4_acl_datatypes.Ipv4AclGrantEnum.deny
    access.access_list_entries.access_list_entry.append(access_list_entry)
    ipv4_acl_and_prefix_list.accesses.access.append(access) 


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("device",
                        help="gNMI device (http://user:password@host:port)")
    args = parser.parse_args()
    device = urlparse(args.device)

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create gNMI provider
    repository = Repository(YDK_REPO_DIR+device.hostname)
    provider = gNMIServiceProvider(repo=repository,
                                   address=device.hostname,
                                   port=device.port,
                                   username=device.username,
                                   password=device.password)
    # create gNMI service
    gnmi = gNMIService()

    ipv4_acl_and_prefix_list = xr_ipv4_acl_cfg.Ipv4AclAndPrefixList()  # create object
    config_ipv4_acl_and_prefix_list(ipv4_acl_and_prefix_list)  # add object configuration

    # set configuration on gNMI device
    ipv4_acl_and_prefix_list.yfilter = YFilter.replace
    gnmi.set(provider, ipv4_acl_and_prefix_list)

    exit()
# End of script
