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
Set configuration for model Cisco-IOS-XR-ipv6-ospfv3-cfg.

usage: gn-set-xr-ipv6-ospfv3-cfg-30-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv6_ospfv3_cfg \
    as xr_ipv6_ospfv3_cfg
from ydk.types import Empty
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")

def config_ospfv3(ospfv3):
    """Add config data to ospfv3 object."""
    # OSPFv3 process
    process = ospfv3.processes.Process()
    process.process_name = "DEFAULT"
    process.default_vrf.router_id = "172.16.255.101"

    # Area 0
    area_area_id = process.default_vrf.area_addresses.AreaAreaId()
    area_area_id.area_id = 0
    area_area_id.enable = Empty()

    # loopback interface passive
    interface = area_area_id.interfaces.Interface()
    interface.interface_name = "Loopback0"
    interface.enable = Empty()
    interface.passive = True
    area_area_id.interfaces.interface.append(interface)

    # gi0/0/0/0 interface
    interface = area_area_id.interfaces.Interface()
    interface.interface_name = "GigabitEthernet0/0/0/0"
    interface.enable = Empty()
    interface.network = xr_ipv6_ospfv3_cfg.Ospfv3Network.point_to_point
    area_area_id.interfaces.interface.append(interface)
    process.default_vrf.area_addresses.area_area_id.append(area_area_id)

    # Area 1
    area_area_id = process.default_vrf.area_addresses.AreaAreaId()
    area_area_id.area_id = 1
    area_area_id.enable = Empty()

    # gi0/0/0/0 interface
    interface = area_area_id.interfaces.Interface()
    interface.interface_name = "GigabitEthernet0/0/0/1"
    interface.enable = Empty()
    interface.network = xr_ipv6_ospfv3_cfg.Ospfv3Network.point_to_point
    area_area_id.interfaces.interface.append(interface)
    process.default_vrf.area_addresses.area_area_id.append(area_area_id)

    # append process config
    ospfv3.processes.process.append(process)


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

    ospfv3 = xr_ipv6_ospfv3_cfg.Ospfv3()  # create object
    config_ospfv3(ospfv3)  # add object configuration

    # set configuration on gNMI device
    ospfv3.yfilter = YFilter.replace
    gnmi.set(provider, ospfv3)

    exit()
# End of script
