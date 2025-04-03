from datetime import datetime
from decimal import Decimal
from typing import Optional, Union, List, Any

from dateutil import parser


def get_decimal(value: Union[dict, int, str, None]) -> Optional[Decimal]:
    value_clean = value
    if isinstance(value, dict):
        value_clean = value.get('$numberLong', 0)
    try:
        return Decimal(str(value_clean))
    except (ValueError, TypeError):
        return None


def get_datetime(value: Union[dict, str, None]) -> Optional[datetime]:
    if isinstance(value, dict):
        date_str = value.get('$date')
    else:
        date_str = value
    if not date_str:
        return None
    try:
        dt = parser.parse(date_str)
        return dt.replace(tzinfo=None)  # Ignore timezone for now
    except ValueError as e:
        raise ValueError(f"Could not parse date: '{date_str}'") from e
    except Exception as e:
        raise Exception(f"Error processing date: {str(e)}") from e


def get_list(data: Union[dict, list], key: str = 'list') -> List:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get(key, list())
    return list()


def get_headless_list(data: list or dict) -> list:
    flat_list = list()
    for item in get_list(data):
        if not isinstance(item, dict):
            raise TypeError('Cannot flatten non dict type lists')
        item_keys = list(item.keys())
        if len(item_keys) != 1:
            raise TypeError('Headed list items must contains only one key')
        head = item_keys[0]
        flat_list.append(dict(
            **item[head], __head=head
        ))
    return flat_list


def get_index_safe(lst: list, index: int) -> Any:
    return lst[index] if 0 <= index < len(lst) else None
