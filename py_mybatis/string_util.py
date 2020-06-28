
def replace_first(string: str, prefix: str):
    if string.startswith(prefix):
        return string.replace(prefix, count=1)
    temp = string.strip()
    if temp.startswith(prefix):
        return temp.replace(prefix, count=1)


def replace_last(string: str, suffix: str):
    if string.endswith(suffix):
        return string[0:-len(suffix)]
    temp = string.strip()
    if temp.endswith(suffix):
        return temp[0:-len(suffix)]

