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
Set configuration for model Cisco-IOS-XR-segment-routing-ms-cfg.

usage: gn-set-xr-segment-routing-ms-cfg-22-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_segment_routing_ms_cfg \
    as xr_segment_routing_ms_cfg
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")

def config_sr(sr):
    """Add config data to sr object."""
    # first set of mappings
    mapping = sr.mappings.Mapping()
    mapping.af = xr_segment_routing_ms_cfg.SrmsAddressFamily.ipv4
    mapping.ip = "172.16.255.1"
    mapping.mask = 32
    mapping.sid_start = 4041
    mapping.sid_range = 1
    sr.mappings.mapping.append(mapping)
    # second set of mappings
    mapping = sr.mappings.Mapping()
    mapping.af = xr_segment_routing_ms_cfg.SrmsAddressFamily.ipv4
    mapping.ip = "172.17.255.1"
    mapping.mask = 32
    mapping.sid_start = 5041
    mapping.sid_range = 8
    sr.mappings.mapping.append(mapping)


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

    sr = xr_segment_routing_ms_cfg.Sr()  # create object
    config_sr(sr)  # add object configuration

    # set configuration on gNMI device
    sr.yfilter = YFilter.replace
    gnmi.set(provider, sr)

    exit()
# End of script
