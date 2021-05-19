"""
mode of operation is defined in the .conf file for the different components
"""
import enum


class ConverseMode(str, enum.Enum):
    ACCEPT_ALL = "accept_all"  # default mycroft-core behavior
    WHITELIST = "whitelist"  # only call converse for skills in whitelist
                             # "whitelist": [skill_id]
    BLACKLIST = "blacklist"  # only call converse for skills NOT in blacklist
                             # "blacklist": [skill_id]


class FallbackMode(str, enum.Enum):
    ACCEPT_ALL = "accept_all"  # default mycroft-core behavior
    WHITELIST = "whitelist"  # only call fallback for skills in whitelist
                             # "whitelist": [skill_id]
    BLACKLIST = "blacklist"  # only call fallback for skills NOT in blacklist
                             # "blacklist": [skill_id]
