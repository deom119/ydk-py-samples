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
Set configuration for model Cisco-IOS-XR-ipv4-ospf-cfg.

usage: gn-set-xr-ipv4-ospf-cfg-30-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_ospf_cfg \
    as xr_ipv4_ospf_cfg
from ydk.types import Empty
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")

def config_ospf(ospf):
    """Add config data to ospf object."""
    # OSPF process
    process = ospf.processes.Process()
    process.process_name = "DEFAULT"
    process.default_vrf.router_id = "172.16.255.1"

    # Area 0
    area_area_id = process.default_vrf.area_addresses.AreaAreaId()
    area_area_id.area_id = 0

    # loopback interface passive
    name_scope = area_area_id.name_scopes.NameScope()
    name_scope.interface_name = "Loopback0"
    name_scope.passive = True
    area_area_id.name_scopes.name_scope.append(name_scope)

    # gi0/0/0/0 interface
    name_scope = area_area_id.name_scopes.NameScope()
    name_scope.interface_name = "GigabitEthernet0/0/0/0"
    name_scope.network_type = xr_ipv4_ospf_cfg.OspfNetwork.point_to_point
    area_area_id.name_scopes.name_scope.append(name_scope)
    process.default_vrf.area_addresses.area_area_id.append(area_area_id)

    # Area 1
    area_area_id = process.default_vrf.area_addresses.AreaAreaId()
    area_area_id.area_id = 1

    # gi0/0/0/1 interface
    name_scope = area_area_id.name_scopes.NameScope()
    name_scope.interface_name = "GigabitEthernet0/0/0/1"
    name_scope.network_type = xr_ipv4_ospf_cfg.OspfNetwork.point_to_point
    area_area_id.name_scopes.name_scope.append(name_scope)
    process.default_vrf.area_addresses.area_area_id.append(area_area_id)

    # append process config
    ospf.processes.process.append(process)


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

    ospf = xr_ipv4_ospf_cfg.Ospf()  # create object
    config_ospf(ospf)  # add object configuration

    # set configuration on gNMI device
    ospf.yfilter = YFilter.replace
    gnmi.set(provider, ospf)

    exit()
# End of script
