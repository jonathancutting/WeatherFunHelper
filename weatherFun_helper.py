#!/usr/bin/env python3

import utility  # for general utility functions and classes
from restRequests import sendRequest    # for sending REST requests
import requests # to establish an HTTP session for requests
import logging  # standard Python logging module
import plogger  # for enhanced logging
import json     # for interpreting received data
import utility  # for various utility functions and classes

logger = logging.getLogger(__name__)
CFG_FILE_NAME = "config.json"
STATION_ID = "KCOF"
ADDY = f"https://api.weather.gov/stations/{STATION_ID}/observations/latest"

def main():
    # Attempt to load the config file.
    cfg = loadConfig()

    # Configure the logger.
    plogger.config_root_logger(cfg["plogger"])
    logger.info("Application started.")

    # Set requests session and get data.
    sesh = requests.Session()    

    # Get observation data.
    resp = getData(sesh)

    print(resp.text)

    logger.info("Exiting application.")

def loadConfig() -> dict:
    '''
    Attempts to load the application config from a file. If the file cannot be
    read or does not exist, an error message is sent to the console, and default
    config values are set.
    
    :return: Dictionary containing application config choices.
    :rtype: dict[str, Any]
    '''

    # Set defaults.
    config = {}

    try:
        with open(CFG_FILE_NAME, 'r') as f:
            config = json.load(f)
    except OSError as e:
        print(f"Error while reading config file: {e}. Using defaults.")

    if not "plogger" in config:
        config["plogger"] = {}

    return config

def getData(sesh:requests.Session) -> requests.Response:
    '''
    Creates and sends GET request to NWS servers for latest observation data.

    :param sesh: Request session
    :type sesh: requests.Session
    :return: Request response with observation data (hopefully).
    :rtype: requests.Response
    '''

    # Set up request headers.
    headers = {}
    headers["accept"] = "application/geo+json"
    headers["user-agent"] = "(WeatherFunHelper_v0.1, CuttingJ@USNavy.vet)"

    # Send the request.
    logger.info("Requesting data from NWS.")
    try:
        resp = sendRequest({"url":ADDY, "sess":sesh, "hdr":headers})
    except Exception as err:
        logger.exception("Could not get data from NWS.")
        resp = requests.Response()  # Create an empty response object.

    return resp

if __name__ == "__main__":
    main()

# NWS API Documentation: https://www.weather.gov/documentation/services-web-API

'''
Example of a standard function documentation block.

:param x: description of parameter variable x
:type x: str
:return: description of return value
:rtype: logging.Logger
'''