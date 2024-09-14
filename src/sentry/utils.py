import re


def clean_output(func):
    """Replaces all symbols, that could rase telegram error or create unnecessary markup with safe one"""

    def wrapper(self, *args, **kwargs):

        result = func(self, *args, **kwargs)
        if result and isinstance(result, str):
            replace = {
                "&": "&amp;",
                "\xa0": " ",
                "`": "'",
                "#": "-",
                "+": "*",
                "\r\n": "\n",
                "<": "&lt;",
                ">": "&gt;",
            }
            pattern = re.compile("|".join(map(re.escape, replace.keys())))
            result = pattern.sub(lambda match: replace[match.group(0)], result)
        return result

    return wrapper
