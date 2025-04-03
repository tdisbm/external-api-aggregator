def merge_dicts_priority(dict1: dict, dict2: dict):
    """Merge dict by keys. If both dicts has the same key, as value will be chosen first non bool False value"""
    keys = list(dict1.keys()) + list(dict2.keys())
    return {
        key: ((dict1.get(key, None) or None) or (dict2.get(key, None) or None))
        for key in keys
    }
