from datetime import datetime
from zoneinfo import ZoneInfo

def get_unix_time()->int:
    return int(datetime.now().replace(microsecond=0).timestamp())

def get_current_tz()->ZoneInfo:
    tz_str = str(datetime.utcnow().astimezone().tzname())
    if tz_str.lower() in ["pdt", "pst"]:
        tz = ZoneInfo("America/Los_Angeles")
    elif tz_str.lower() in ["utc"]:
        tz = ZoneInfo("Zulu")
    else:
        tz = ZoneInfo(tz_str)
    return tz

def localize_dt(dt: datetime|str|int,
                return_format: str="iso",
                tz: ZoneInfo=get_current_tz()
                ) -> str|int|None:

    if isinstance(dt, datetime):
        res = dt.astimezone(tz)
    elif isinstance(dt, str):
        res =  datetime.fromisoformat(dt).astimezone(tz)
    elif isinstance(dt, int) and len(str(dt)) == 10:
        res = datetime.fromtimestamp(dt).astimezone(tz)
    else:
        raise Exception(f"{dt} is not a valid date format")

    if return_format == "iso":
        return res.isoformat()
    elif return_format == "ts":
        return int(res.timestamp())
    else:
        return res.isoformat()

def str_to_secs(time_range: str) -> int:
    """
    Returns an int
    """
    if time_range == "decadely":
        secs = int(86400 * (365.25 * 10))
    elif time_range == "yearly":
        secs = int(86400 * 365.25)
    elif time_range == "monthly":
        secs = int(86400 * 30.5)
    elif time_range == "weekly":
        secs = (86400 * 7)
    elif time_range == "daily":
        secs = 86400
    elif time_range == "hourly":
        secs = 3600
    elif time_range == "minutely":
        secs = 60
    elif time_range == "secondly":
        secs = 1
    else:
        raise Exception(f"{time_range}\nIs not a known time string")
    return secs
