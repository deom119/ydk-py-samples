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
Set configuration for model Cisco-IOS-XR-infra-syslog-cfg.

usage: gn-set-xr-infra-syslog-cfg-52-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_infra_syslog_cfg \
    as xr_infra_syslog_cfg
from ydk.types import Empty
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")

def config_syslog(syslog):
    """Add config data to syslog object."""
    #ipv4 TOS bit
    syslog.ipv4.tos.type = xr_infra_syslog_cfg.LoggingTos.dscp
    syslog.ipv4.tos.dscp = xr_infra_syslog_cfg.LoggingDscpValue.cs2

    #Facility
    syslog.logging_facilities.facility_level = xr_infra_syslog_cfg.Facility.local0

    #Hostserver
    vrf = syslog.host_server.vrfs.Vrf()
    vrf.vrf_name = "default"
    ipv4_1 = vrf.ipv4s.Ipv4()
    ipv4_1.address = "10.0.0.1"
    ipv4_severity_port = ipv4_1.Ipv4SeverityPort()
    ipv4_severity_port.severity = 6
    ipv4_1.ipv4_severity_port = ipv4_severity_port
    ipv4_2 = vrf.ipv4s.Ipv4()
    ipv4_2.address = "10.0.0.2"
    ipv4_severity_port = ipv4_2.Ipv4SeverityPort()
    ipv4_severity_port.severity = 6
    ipv4_2.ipv4_severity_port = ipv4_severity_port
    vrf.ipv4s.ipv4.append(ipv4_1)
    vrf.ipv4s.ipv4.append(ipv4_2)
    syslog.host_server.vrfs.vrf.append(vrf)

    #Source-interface
    source_interface_value = syslog.source_interface_table.source_interface_values.SourceInterfaceValue()
    source_interface_value.src_interface_name_value = "Loopback0"
    source_interface_vrf = source_interface_value.source_interface_vrfs.SourceInterfaceVrf()
    source_interface_vrf.vrf_name = "default"
    source_interface_value.source_interface_vrfs.source_interface_vrf.append(source_interface_vrf)
    syslog.source_interface_table.source_interface_values.source_interface_value.append(source_interface_value)

    #Host Name Prefix
    syslog.host_name_prefix = "router"

    # Suppression
    syslog.suppress_duplicates = Empty()


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

    syslog = xr_infra_syslog_cfg.Syslog()  # create object
    config_syslog(syslog)  # add object configuration

    # set configuration on gNMI device
    syslog.yfilter = YFilter.replace
    gnmi.set(provider, syslog)

    exit()
# End of script
