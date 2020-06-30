import re


def replace_cdata(raw_text):
    """
    Replace CDATA String
    :param raw_text:
    :return:
    """
    cdata_regex = '(<!\[CDATA\[)([\s\S]*?)(\]\]>)'
    pattern = re.compile(cdata_regex)
    match = pattern.search(raw_text)
    if match:
        cdata_text = match.group(2)
        cdata_text = convert_cdata(cdata_text, reverse=True)
        raw_text = raw_text.replace(match.group(), cdata_text)
    return raw_text


def convert_cdata(string, reverse=False):
    """
    Replace CDATA String
    :param string:
    :param reverse:
    :return:
    """
    if reverse:
        string = string.replace('&', '&amp;')
        string = string.replace('<', '&lt;')
        string = string.replace('>', '&gt;')
        string = string.replace('"', '&quot;')
    else:
        string = string.replace('&amp;', '&')
        string = string.replace('&lt;', '<')
        string = string.replace('&gt;', '>', )
        string = string.replace('&quot;', '"')
    return string


def sql_string_format(sql_str_value: str):
    if not sql_str_value.startswith('\''):
        sql_str_value = '\'' + sql_str_value
    if not sql_str_value.endswith('\''):
        sql_str_value = sql_str_value + '\''
    return sql_str_value


def param_str(param_value):
    if not param_value:
        return 'null'
    if type(param_value) == str:
        return sql_string_format(param_value)
    return str(param_value)
