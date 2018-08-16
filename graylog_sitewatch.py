#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Name             : Simple Python Script to check status of web url and log result to GrayLog
Created By       : Peter Matkovski
License          :
Documentation    : https://github.com/petermat/graylog_sitewatch
"""

import os, sys, argparse
from pygelf import GelfTlsHandler
import json, re
#import urllib.request
import requests

import logging
import logging.handlers
from logging.handlers import RotatingFileHandler



def read_config(file='config.json'):
    """
    :param file: str()
    :return: dict()
    """

    json1_file = open(file)
    json1_str = json1_file.read()
    return  json.loads(json1_str)

def check_lookup(web_lookup):
    """
    :param web_lookup:
    :return:
    """

    url = web_lookup['url']
    patterns = web_lookup['patterns']
    size_min = web_lookup['size_min']

    session = requests.session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
    })
    response = session.get(url)

    lookup_status = "OK"
    lookup_message = ""

    if response.status_code != 200:
        lookup_status = "ERROR"
        lookup_message += "retrieved code: {}".format(response.status_code)

    else:
        if response.elapsed.total_seconds() > 30:
            lookup_status = "WARNING"
            lookup_message += "slow load: {}s ".format(response.elapsed.total_seconds())

        if len(response.content) < size_min:
            lookup_status = "WARNING"
            lookup_message += "small content: {}b ".format(len(response.content))

        for pttrn in patterns:
            if not re.search(pttrn, response.text, re.DOTALL):
                lookup_status = "WARNING"
                lookup_message += "no match: {} ".format(pttrn)

    return lookup_status, lookup_message


def main(args, loglevel):
    """

    :param args: see main
    :param loglevel:
    :return:
    """

    # config file loader
    config_dict = read_config(file=args.config)

    ### Loggers ###
    # graylog logger
    logging.basicConfig(level=loglevel)
    logger = logging.getLogger()
    logger.addHandler(GelfTlsHandler(host=config_dict['graylog_server'], port=config_dict['gralog_port'],
                                     include_extra_fields=True))

    format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # console logger not needed, GELF handler writes to console by default
    #ch = logging.StreamHandler(sys.stdout)
    #ch.setFormatter(format)
    #logger.addHandler(ch)

    fh = RotatingFileHandler('backlog.txt', maxBytes=(1048576 * 5), backupCount=7)
    fh.setFormatter(format)
    logger.addHandler(fh)
    ### Loggers END ###


    logger.debug('Graylog site monitor activated with config file {}'.format(args.config))
    logger.debug('Contains {} websites'.format(len(config_dict['websites'])))

    for website in config_dict['websites']:
        web_domain = website['domain']
        web_lookups = website['lookups']

        logger.debug("Starting check of website: {}, has {} lookups".format(web_domain,len(web_lookups)))

        if website.get("login"):
            logger.debug("Website has login procedure")


        for counter, web_lookup in enumerate(web_lookups):
            web_url = web_lookup['url']
            lookup_status, lookup_message = check_lookup(web_lookup)
            lookup_description = web_lookup['description']

            if lookup_status == "OK":
                logger.debug("Lookup n.{}: OK, url: {}".format(counter, web_lookup['url']),
                             extra={'url': web_url, 'domain': web_domain, 'lookup_message': lookup_message})
            elif lookup_status == "WARNING":
                logger.warning("Warning in {} ({}), {}, url: {}".format(web_domain,lookup_description,lookup_message, web_url),
                               extra={'url':web_url,'domain': web_domain, 'lookup_message':lookup_message})
            elif lookup_status == "ERROR":
                logger.error("Error in {} ({}), {}, url: {}".format(web_domain,lookup_description,lookup_message, web_url),
                               extra={'url':web_url,'domain': web_domain, 'lookup_message':lookup_message})
            else:
                logger.critical("Malfunction in {} ({}): lookup_status not recognized: {}, type:".format(web_url, lookup_description,type(lookup_status)),
                                extra={'url': web_url, 'domain': web_domain, 'lookup_message': lookup_message})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                                    description = "Does a thing to some stuff.",
                                    epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
                                    fromfile_prefix_chars = '@' )

    parser.add_argument(
                        "-c",
                        "--config",
                        help = "Define costom config file or leave blank to use config.json",
                        default="config.json")
    parser.add_argument(
                        "-v",
                        "--verbose",
                        help="increase output verbosity",
                        action="store_true",
                        )
    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)
