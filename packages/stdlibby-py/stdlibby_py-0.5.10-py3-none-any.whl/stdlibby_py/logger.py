import ndjson
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from functools import partial
from typing import Callable
import os
from utils import del_key
import json

LogLevel = Enum("LogLevel", ["DEBUG", "INFO", "WARNING", "ERROR", "FATAL"])

@dataclass
class Logger():
    appname: str

def log(mesg: str, level: LogLevel, logpath: str, is_accurate: bool, app_info: dict={}, extras: dict={}):
    if is_accurate:
        unix_time = round(datetime.timestamp(datetime.now()), 4)
    else:
        unix_time = int(datetime.timestamp(datetime.now()))

    line = {**{"ut": unix_time, "level": level, "mesg": mesg}, **app_info, **extras}
    print(line)
    ndjson.append(logpath, [line], create_if_not_exists=True)

def print_log(logpath: str):
    p = ndjson.load(logpath)
    print("\n".join([json.dumps(x) for x in p]))

def logger(app_info: dict={}, is_accurate: bool=False)->Callable:
    """
    Returns a partial function for logging
    """
    logpath = os.path.join("/shared/log", f"{os.path.basename(__file__)}.ndjson")
    if "log_level" in app_info:
        log_level = app_info["log_level"]
        del_key("log_level", app_info)
    else:
        log_level = LogLevel.INFO

    del_key("mesg", app_info)
    del_key("unix_time", app_info)
    return partial(log, logpath=logpath, level=log_level, app_info=app_info, is_accurate=is_accurate)

if __name__ == "__main__":
    l = logger({"TIMMY": "WAS HERE", "log_level": LogLevel.WARNING, "mesg": "SHOULD NOT SEE"})
    l("red", extras={"red": 1})
    print_log("/shared/log/logger.py.ndjson")
