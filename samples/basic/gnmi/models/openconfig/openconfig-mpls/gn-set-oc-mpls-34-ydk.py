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

usage: gn-set-oc-mpls-34-ydk.py [-h] [-v] device

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
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")


def config_mpls(network_instances):
    """Add config data to mpls object."""
    # configure default network instance
    network_instance = network_instances.NetworkInstance()
    network_instance.name = "default"
    network_instance.config.name = "default"
    # interface attributes gi0/0/0/0
    interface = network_instance.mpls.te_interface_attributes.Interface()
    interface.interface_id = "GigabitEthernet0/0/0/1"
    interface.config.interface_id = "GigabitEthernet0/0/0/1"
    interface.config.admin_group.append("RED")
    interface.config.admin_group.append("BLUE")
    network_instance.mpls.te_interface_attributes.interface.append(interface)

    # TE global attributes
    admin_group = network_instance.mpls.te_global_attributes.mpls_admin_groups.AdminGroup()
    admin_group.admin_group_name = "RED"
    admin_group.config.admin_group_name = "RED"
    admin_group.config.bit_position = 0
    network_instance.mpls.te_global_attributes.mpls_admin_groups.admin_group.append(admin_group)
    admin_group = network_instance.mpls.te_global_attributes.mpls_admin_groups.AdminGroup()
    admin_group.admin_group_name = "BLUE"
    admin_group.config.admin_group_name = "BLUE"
    admin_group.config.bit_position = 1
    network_instance.mpls.te_global_attributes.mpls_admin_groups.admin_group.append(admin_group)

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

