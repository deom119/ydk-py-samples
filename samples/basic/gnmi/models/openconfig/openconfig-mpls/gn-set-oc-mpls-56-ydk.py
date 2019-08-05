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
Set configuration for model openconfig-mpls.

usage: gn-set-oc-mpls-56-ydk.py [-h] [-v] device

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
from ydk.models.openconfig import openconfig_network_instance \
    as oc_network_instance
from ydk.models.openconfig import openconfig_mpls_types \
    as oc_mpls_types
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")


def config_mpls(network_instances):
    """Add config data to mpls object."""
    # configure default network instance
    network_instance = network_instances.NetworkInstance()
    network_instance.name = "default"
    network_instance.config.name = "default"

    # tunnel with affinity and priority 5/5
    tunnel = network_instance.mpls.lsps.constrained_path.tunnels.Tunnel()
    tunnel.name = "LER1-LER2-t56"
    tunnel.config.name = "LER1-LER2-t56"
    tunnel.config.setup_priority = 5
    tunnel.config.hold_priority = 5
    tunnel.config.type = oc_mpls_types.P2P()
    #tunnel.type = oc_mpls_types.P2P()
    p2p_primary_path = tunnel.p2p_tunnel_attributes.p2p_primary_path.P2pPrimaryPath_()
    p2p_primary_path.name = "DYNAMIC"
    p2p_primary_path.config.name = "DYNAMIC"
    p2p_primary_path.config.preference = 10
    path_computation_method = oc_mpls_types.LOCALLYCOMPUTED()
    p2p_primary_path.config.path_computation_method = path_computation_method
    p2p_primary_path.admin_groups.config.exclude_group.append("RED")
    tunnel.p2p_tunnel_attributes.p2p_primary_path.p2p_primary_path.append(p2p_primary_path)
    tunnel.p2p_tunnel_attributes.config.destination = "172.16.255.2"
    tunnel.bandwidth.config.set_bandwidth = 100000

    network_instance.mpls.lsps.constrained_path.tunnels.tunnel.append(tunnel)
    network_instances.network_instance.append(network_instance)


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

    network_instances = oc_network_instance.NetworkInstances()
    config_mpls(network_instances)  # add object configuration

    # set configuration on gNMI device
    network_instances.yfilter = YFilter.replace
    gnmi.set(provider, network_instances)

    exit()
# End of script
