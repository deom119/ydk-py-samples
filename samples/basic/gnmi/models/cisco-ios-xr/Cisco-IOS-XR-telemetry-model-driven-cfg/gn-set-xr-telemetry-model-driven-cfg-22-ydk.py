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
Set configuration for model Cisco-IOS-XR-telemetry-model-driven-cfg.

usage: gn-set-xr-telemetry-model-driven-cfg-22-ydk.py [-h] [-v] device

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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_telemetry_model_driven_cfg \
    as xr_telemetry_model_driven_cfg
from ydk.types import Empty
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")

def config_telemetry_model_driven(telemetry_model_driven):
    """Add config data to telemetry_model_driven object."""
    # destination group
    destination_group = telemetry_model_driven.destination_groups.DestinationGroup()
    destination_group.destination_id = "DGROUP1"
    ipv4_destination = destination_group.ipv4_destinations.Ipv4Destination()
    ipv4_destination.destination_port = 5432
    ipv4_destination.ipv4_address = "172.30.8.4"
    ipv4_destination.encoding = xr_telemetry_model_driven_cfg.EncodeType.self_describing_gpb
    protocol = ipv4_destination.Protocol()
    protocol.protocol = xr_telemetry_model_driven_cfg.ProtoType.grpc
    protocol.no_tls = Empty()
    ipv4_destination.protocol = protocol
    destination_group.ipv4_destinations.ipv4_destination.append(ipv4_destination)
    telemetry_model_driven.destination_groups.destination_group.append(destination_group)

    # sensor group
    sensor_group = telemetry_model_driven.sensor_groups.SensorGroup()
    sensor_group.sensor_group_identifier = "SGROUP1"
    sensor_path = sensor_group.sensor_paths.SensorPath()
    sensor_path.telemetry_sensor_path = "Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters" 
    sensor_group.sensor_paths.sensor_path.append(sensor_path)
    sensor_path = sensor_group.sensor_paths.SensorPath()
    sensor_path.telemetry_sensor_path = "Cisco-IOS-XR-nto-misc-oper:memory-summary/nodes/node/summary"
    sensor_group.sensor_paths.sensor_path.append(sensor_path)
    telemetry_model_driven.sensor_groups.sensor_group.append(sensor_group)

    # subscription
    subscription = telemetry_model_driven.subscriptions.Subscription()
    subscription.subscription_identifier = "SUB1"
    sensor_profile = subscription.sensor_profiles.SensorProfile()
    sensor_profile.sensorgroupid = "SGROUP1"
    sensor_profile.sample_interval = 30000
    subscription.sensor_profiles.sensor_profile.append(sensor_profile) 
    destination_profile = subscription.destination_profiles.DestinationProfile()
    destination_profile.destination_id = "DGROUP1"
    subscription.destination_profiles.destination_profile.append(destination_profile) 
    telemetry_model_driven.subscriptions.subscription.append(subscription)


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

    telemetry_model_driven = xr_telemetry_model_driven_cfg.TelemetryModelDriven()  # create object
    config_telemetry_model_driven(telemetry_model_driven)  # add object configuration

    # set configuration on gNMI device
    telemetry_model_driven.yfilter = YFilter.replace
    gnmi.set(provider, telemetry_model_driven)

    exit()
# End of script
