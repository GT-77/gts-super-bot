"""
module dedicated to text formatting
"""


class Formatting:
    "i use this class for easy discord text formatting"



    def __init__(self, core_formats):
        self._core_formats = core_formats



    def __getattr__(self, attr):
        parsed = attr.split("_")

        marking = list()
        for format_ in parsed:
            if format_ in self._core_formats:
                marking.append(self._core_formats[format_])
            else:
                raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attr}'")

        marking = "".join(marking)
        return lambda string: f"{marking}{string}{marking[::-1]}" if string else ""



# all the basic fundamental markings for discord text formatting
fundamental_discord_formats = dict (

    codeblock = "```",
    code = "`",
    italics = "*",
    bold = "**",
    underline = "__",
    strikethru = "~~", # xd
    spoiler = '||',

)



formatting = Formatting(fundamental_discord_formats)
# usage examples:
# formatting.italics("abc") returns "*abc*"
# formatting.strikethru_bold_italics("bling bling $$$") returns "~~***bling bling $$$***~~"
# formatting.strikethru_underline_bold_italics_codeblock("a") returns "~~__***```a```***__~~"
