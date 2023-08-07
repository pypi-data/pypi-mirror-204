import json
from logging.handlers import TimedRotatingFileHandler
import logging
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os
import bz2
from random import randint
from time import sleep
from datetime import datetime
import atexit

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


class ArLogger():
    def __init__(self, logAtExit=True):
        self.url = None
        self.projectName = None
        self.logger = None
        self.HTTPHandler = None
        self.localLogHandler = None
        self.localLogLevel = INFO
        self.HTTPLogLevel = ERROR
        if logAtExit:
            atexit.register(self.on_exit)

    # same as __del__
    def on_exit(self):
        self.logger.critical(self.projectName + " is crashed or exited.")

    def setLevel(self, httpLevel=None, localLevel=None):

        if httpLevel is not None:
            self.HTTPLogLevel = httpLevel
            self.HTTPHandler.setLevel(self.HTTPLogLevel)

        if localLevel is not None:
            self.localLogLevel = localLevel
            self.localLogHandler.setLevel(self.localLogLevel)

        return self.logger

    def setUrl(self, url, projectName):
        self.url = url
        self.projectName = projectName

        local_format = "%(levelname)s:%(asctime)s:%(name)s:%(message)s"
        http_format = logging.Formatter(json.dumps({
            'projectname': projectName,
            'pathname': '%(pathname)s',
            'line': '%(lineno)d',
            'levelname': '%(levelname)s',
            'message': '%(message)s',
            'func': '%(funcName)s',
        }))

        os.mkdir("./logs") if not os.path.exists("./logs") else None

        self.localLogHandler = TimedRotatingFileHandler(filename="./logs/"+projectName+".log",
                                                        when="midnight",
                                                        backupCount=14
                                                        )

        self.localLogHandler.rotator = self.__bzip_rotator__
        self.localLogHandler.namer = self.__bz2namer__
        self.localLogHandler.setFormatter(logging.Formatter(local_format))

        self.HTTPHandler = CustomHttpHandler(
            url=url
        )
        self.HTTPHandler.setLevel(self.HTTPLogLevel)
        self.HTTPHandler.setFormatter(http_format)

        self.logger = logging.getLogger()

        self.logger.addHandler(self.localLogHandler)
        self.logger.addHandler(self.HTTPHandler)

        self.logger.setLevel(self.localLogLevel)

        # do rollover when logger is created
        # self.localLogHandler.doRollover()

        return self

    def __bzip_rotator__(self, source, dest):
        with open(source, "rb") as sf:
            data = sf.read()
            compressed = bz2.compress(data, 9)
            with open(dest, "wb") as df:
                df.write(compressed)

        with open(dest, "rb") as sf:
            data = {"file_name": str(source)}
            daily_log_url = self.url + "/daily"
            sleep_time = randint(0, 10)
            sleep(sleep_time)
            resp = requests.post(daily_log_url, files={"file": sf})
            if resp.status_code == 200:
                os.remove(source)

    def __bz2namer__(self, name):
        return name + ".bz2"


class CustomHttpHandler(logging.Handler):
    def __init__(self, url: str):
        self.url = url
        self.MAX_POOLSIZE = 100
        self.session = requests.Session()
        self.session.mount('', HTTPAdapter(
            max_retries=Retry(
                total=5,
                backoff_factor=0.5,
                status_forcelist=[403, 500]
            ),
            pool_connections=self.MAX_POOLSIZE,
            pool_maxsize=self.MAX_POOLSIZE
        ))
        super().__init__()

    def emit(self, record):

        logEntry = record.__dict__

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S.%f")

        logEntry["func"] = logEntry["funcName"]
        logEntry["line"] = logEntry["lineno"]
        logEntry["fields.time"] = dt_string
        logEntry["fields.levelname"] = logEntry["levelname"]

        urgent_log_url = self.url + "/log"
        self.session.headers = {'Content-Type': 'application/json'}
        resp = self.session.post(urgent_log_url, json=logEntry)

        if resp.status_code != 200:
            print("Error in sending log to server")
