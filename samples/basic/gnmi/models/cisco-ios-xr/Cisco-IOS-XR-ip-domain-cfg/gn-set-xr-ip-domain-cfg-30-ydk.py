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
Set configuration for model Cisco-IOS-XR-ip-domain-cfg.

usage: gn-set-xr-ip-domain-cfg-30-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ip_domain_cfg \
    as xr_ip_domain_cfg
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")

def config_ip_domain(ip_domain):
    """Add config data to ip_domain object."""
    vrf = ip_domain.vrfs.Vrf()
    vrf.vrf_name = "RED"
    # host name "ruby"
    ipv4_host = vrf.ipv4_hosts.Ipv4Host()
    ipv4_host.host_name = "ruby"
    ipv4_host.address.append("192.168.0.1")
    vrf.ipv4_hosts.ipv4_host.append(ipv4_host)
    # host name "flame"
    ipv4_host = vrf.ipv4_hosts.Ipv4Host()
    ipv4_host.host_name = "flame"
    ipv4_host.address.append("192.168.0.2")
    vrf.ipv4_hosts.ipv4_host.append(ipv4_host)
    # host name "crimson"
    ipv4_host = vrf.ipv4_hosts.Ipv4Host()
    ipv4_host.host_name = "crimson"
    ipv4_host.address.append("192.168.0.3")
    ipv4_host.address.append("192.168.0.4")
    vrf.ipv4_hosts.ipv4_host.append(ipv4_host)
    # host name "raspberry"
    ipv4_host = vrf.ipv4_hosts.Ipv4Host()
    ipv4_host.host_name = "raspberry"
    ipv4_host.address.append("192.168.0.5")
    ipv4_host.address.append("192.168.0.6")
    vrf.ipv4_hosts.ipv4_host.append(ipv4_host)
    ip_domain.vrfs.vrf.append(vrf)


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

    ip_domain = xr_ip_domain_cfg.IpDomain()  # create object
    config_ip_domain(ip_domain)  # add object configuration

    # set configuration on gNMI device
    ip_domain.yfilter = YFilter.replace
    gnmi.set(provider, ip_domain)

    exit()
# End of script
