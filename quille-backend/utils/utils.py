import datetime


def now() -> str:
    """Returns the current UTC timestamp in ISOFORMAT"""
    return datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
