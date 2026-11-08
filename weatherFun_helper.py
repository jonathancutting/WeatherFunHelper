#!/usr/bin/env python3

import utility  # for general utility functions and classes
from utility import sendRequest    # for sending REST requests
import requests # to establish an HTTP session for requests
import logging  # standard Python logging module
import plogger  # for enhanced logging
import json     # for interpreting received data

logger = logging.getLogger(__name__)
CFG_FILE_NAME = "config.json"
STATION_ID = "KCOF"
ADDY = f"https://api.weather.gov/stations/{STATION_ID}/observations/latest"

class Observation:
    def __init__(self) -> None:
        self.coords = [0,0]
        self.elevation = 0
        self.station_id = ""
        self.station_name = ""
        self.timestamp = ""
        self.metar = ""
        self.weather = ""
        self.temp = 0.0
        self.dewpoint = 0.0
        self.wind_dir = 0
        self.wind_speed = 0.0
        self.wind_gust = 0.0
        self.slp = 0.0
        self.visibility = 0
        self.relative_humidity = 0.0
        self.wind_chill = 0.0
        self.heat_index = 0.0

def main():
    # Attempt to load the config file.
    cfg = loadConfig()

    # Configure the logger.
    plogger.config_root_logger(cfg["plogger"])
    logger.info("Application started.")

    # Set requests session and get data.
    sesh = requests.Session()    

    # Get observation data.
    try:
        resp = getData(sesh)
    except Exception as err:
        resp = None

    # Parse received data.
    obs = None
    if not resp is None:
        obs = parseData(resp)

    # Do something with the data.
    if not obs is None:
        printObservation(obs)
    else:
        logger.warning("No observation data to print.")
        print("Cannot print current observation.")

    logger.info("Exiting application.")

def loadConfig() -> dict:
    ''' Attempts to load the application config from a file. If the file cannot
    be read or does not exist, an error message is sent to the console, and
    default config values are set.
    
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
    ''' Creates and sends GET request to NWS server for latest observation data.

    :param sesh: Request session
    :type sesh: requests.Session
    :return: Request response with observation data (hopefully).
    :rtype: requests.Response
    '''

    logger.debug("Entered function getData.")

    # Set up request headers.
    headers = {}
    headers["accept"] = "application/geo+json"
    headers["user-agent"] = "(WeatherFunHelper_v0.1, CuttingJ@USNavy.vet)"

    # Send the request.
    logger.info("Requesting data from NWS.")
    try:
        resp = sendRequest({"url":ADDY, "sess":sesh, "hdr":headers})
        logger.info("Data received from NWS.")
    except Exception as err:
        logger.exception("Could not get data from NWS.")
        raise

    logger.debug("Exiting function getData.")
    return resp

def parseData(response:requests.Response) -> Observation:
    logger.debug("Entered function parseData.")

    dataDict = json.loads(response.text)
    obs = Observation()
    obs.coords = dataDict["geometry"]["coordinates"]                # long, lat
    obs.elevation = dataDict["properties"]["elevation"]["value"]    # m
    obs.station_id = dataDict["properties"]["stationId"]
    obs.station_name = dataDict["properties"]["stationName"]
    obs.timestamp = dataDict["properties"]["timestamp"]             # ISO 8601
    obs.metar = dataDict["properties"]["rawMessage"]
    obs.weather = dataDict["properties"]["textDescription"]
    obs.temp = dataDict["properties"]["temperature"]["value"]       # degC
    obs.dewpoint = dataDict["properties"]["dewpoint"]["value"]      # degC
    obs.wind_dir = dataDict["properties"]["windDirection"]["value"] # deg
    obs.wind_speed = dataDict["properties"]["windSpeed"]["value"]   # kph
    obs.wind_gust = dataDict["properties"]["windGust"]["value"]     # kph
    obs.slp = dataDict["properties"]["seaLevelPressure"]["value"]   # mb
    obs.visibility = dataDict["properties"]["visibility"]["value"]  # m
    obs.relative_humidity = dataDict["properties"]["relativeHumidity"]["value"] # pct
    obs.wind_chill = dataDict["properties"]["windChill"]["value"]   # degC
    obs.heat_index = dataDict["properties"]["heatIndex"]["value"]   # degC

    logger.info("METAR received: %s", obs.metar)

    logger.debug("Exiting function parseData.")
    return obs

def printObservation(obs:Observation):
    logger.debug("Entering function printObservation.")

    print(f"Current temperature: {int(obs.temp)}°C")
    print(f"Current dewpoint:    {int(obs.dewpoint)}°C")
    print(f"Current heat index:  {int(obs.heat_index)}°C")

    logger.debug("Exiting function printObservation.")

if __name__ == "__main__":
    main()

# NWS API Documentation: https://www.weather.gov/documentation/services-web-API

''' Example of a standard function documentation block.

:param x: description of parameter variable x
:type x: str
:return: description of return value
:rtype: logging.Logger
'''
