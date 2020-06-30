import re


def replace_sql_first(string: str, prefix_overrides: str, replace: str):
    string = string.strip()
    regex = r'^[\s]*?({})'.format(prefix_overrides)
    return re.sub(regex, replace, string, count=1, flags=re.IGNORECASE)


def replace_sql_last(string: str, suffix_overrides: str, replace: str):
    string = string.strip()
    regex = r'({})(\s+--.+)?$'.format(suffix_overrides)
    return re.sub(regex, replace, string, count=1, flags=re.IGNORECASE)

