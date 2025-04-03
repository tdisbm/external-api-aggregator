from datetime import datetime


def earliest(*args: datetime or None) -> datetime or None:
    try:
        return min(list(_datetime for _datetime in args if _datetime))
    except ValueError:  # In case when all the values are bool(value) == False
        return None


def latest(*args: datetime or None) -> datetime or None:
    try:
        return max(list(_datetime for _datetime in args if _datetime))
    except ValueError:  # In case when all the values are bool(value) == False
        return None
