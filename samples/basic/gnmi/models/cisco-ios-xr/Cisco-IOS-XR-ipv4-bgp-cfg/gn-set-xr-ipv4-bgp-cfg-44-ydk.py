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
Set configuration for model Cisco-IOS-XR-ipv4-bgp-cfg.

usage: gn-set-xr-ipv4-bgp-cfg-44-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_bgp_cfg \
    as xr_ipv4_bgp_cfg
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_bgp_datatypes \
    as xr_ipv4_bgp_datatypes
from ydk.types import Empty
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")

def config_bgp(bgp):
    """Add config data to bgp object."""
    # global configuration
    instance = bgp.Instance()
    instance.instance_name = "default"
    instance_as = instance.InstanceAs()
    instance_as.as_ = 0
    four_byte_as = instance_as.FourByteAs()
    four_byte_as.as_ = 65001
    four_byte_as.bgp_running = Empty()
    # global address family
    global_af = four_byte_as.default_vrf.global_.global_afs.GlobalAf()
    global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamily.ipv4_unicast
    global_af.enable = Empty()
    four_byte_as.default_vrf.global_.global_afs.global_af.append(global_af)
    instance_as.four_byte_as.append(four_byte_as)
    instance.instance_as.append(instance_as)
    bgp.instance.append(instance)

    # configure IBGP neighbor group
    neighbor_groups = four_byte_as.default_vrf.bgp_entity.neighbor_groups
    neighbor_group = neighbor_groups.NeighborGroup()
    neighbor_group.neighbor_group_name = "EBGP"
    neighbor_group.create = Empty()
    # remote AS
    neighbor_group.remote_as.as_xx = 0
    neighbor_group.remote_as.as_yy = 65002
    neighbor_groups.neighbor_group.append(neighbor_group)
    # ipv4-unicast address family
    neighbor_group_af = neighbor_group.neighbor_group_afs.NeighborGroupAf()
    neighbor_group_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamily.ipv4_unicast
    neighbor_group_af.activate = Empty()
    neighbor_group_af.route_policy_in = "POLICY3"  # must be pre-configured
    neighbor_group_af.route_policy_out = "POLICY1"  # must be pre-configured
    neighbor_group_afs = neighbor_group.neighbor_group_afs
    neighbor_group_afs.neighbor_group_af.append(neighbor_group_af)

    # configure IBGP neighbor
    neighbor = four_byte_as.default_vrf.bgp_entity.neighbors.Neighbor()
    neighbor.neighbor_address = "192.168.1.1"
    neighbor.neighbor_group_add_member = "EBGP"
    four_byte_as.default_vrf.bgp_entity.neighbors.neighbor.append(neighbor)


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

    bgp = xr_ipv4_bgp_cfg.Bgp()  # create object
    config_bgp(bgp)  # add object configuration

    # set configuration on gNMI device
    bgp.yfilter = YFilter.replace
    gnmi.set(provider, bgp)

    exit()
# End of script
