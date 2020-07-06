#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Copyright (c) 2020 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Engine connection helper for SDK examples, such as parsing command line arguments
and create connection to engine server.
"""

import getpass
import logging
import ovirtsdk4 as sdk
import time


def add_engine_arguments(parser):
    parser.add_argument(
        "--engine-url",
        required=True,
        help="oVirt engine URL (e.g. https://engine_fqdn:port)")

    parser.add_argument(
        "--username",
        required=True,
        help="username of engine API")

    parser.add_argument(
        "--password-file",
        help="file containing password of the specified by user (if file is "
             "not specified, read from standard input)")

    parser.add_argument(
        "-c", "--cafile",
        help="path to oVirt engine certificate for verifying server.")

    parser.add_argument(
        "--insecure",
        dest="secure",
        action="store_false",
        default=False,
        help=("do not verify server certificates and host name (not "
              "recommended)."))

    parser.add_argument(
        "--debug",
        action="store_true",
        help="log debug level messages to log file specified in logger")


def create_connection(args):
    """
    Usage:
        connection = common.create_connection(args)
        with closing(connection):
            # use the connection. It will be closed when
            # exiting this block.
    """
    return sdk.Connection(
        url=args.engine_url + '/ovirt-engine/api',
        username=args.username,
        password=read_password(args),
        ca_file=args.cafile,
        debug=args.debug,
        log=logging.getLogger(),
    )

def read_password(args):
    if args.password_file:
        with open(args.password_file) as f:
            return f.read().rstrip('\n') # oVirt doesn't support empty lines in password
    else:
        return getpass.getpass()


def progress(msg, start_time=time.monotonic()):
    print("[ %5.1f ] %s" % (time.monotonic() - start_time, msg))


def configure_logging(level=logging.WARNING, filename="example.log"):
    logging.basicConfig(
        level=level,
        filename=filename,
        format="%(asctime)s %(levelname)-7s (%(threadName)s) [%(name)s] %(message)s")
