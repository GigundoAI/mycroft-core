# Copyright 2018 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from time import sleep
from os.path import join, dirname, expanduser, exists
from xdg import BaseDirectory as XDG

# for downstream support, all XDG paths should respect this
BASE_FOLDER = "mycroft"
CONFIG_FILE_NAME = "mycroft.conf"


def set_xdg_base(folder_name):
    global BASE_FOLDER, WEB_CONFIG_CACHE
    from mycroft.util.log import LOG
    LOG.info(f"XDG base folder set to: '{folder_name}'")
    BASE_FOLDER = folder_name
    WEB_CONFIG_CACHE = join(XDG.xdg_config_home, BASE_FOLDER, 'web_cache.json')
    __ensure_folder_exists(WEB_CONFIG_CACHE)


def set_config_filename(file_name, core_folder=None):
    global CONFIG_FILE_NAME, SYSTEM_CONFIG, OLD_USER_CONFIG, USER_CONFIG, \
        BASE_FOLDER
    from mycroft.util.log import LOG
    if core_folder:
        BASE_FOLDER = core_folder
        set_xdg_base(core_folder)
    LOG.info(f"config filename set to: '{file_name}'")
    CONFIG_FILE_NAME = file_name
    SYSTEM_CONFIG = os.environ.get('MYCROFT_SYSTEM_CONFIG',
                                   f'/etc/{BASE_FOLDER}/{CONFIG_FILE_NAME}')
    # Make sure we support the old location still
    # Deprecated and will be removed eventually
    OLD_USER_CONFIG = join(expanduser('~'), '.' + BASE_FOLDER,
                           CONFIG_FILE_NAME)
    USER_CONFIG = join(XDG.xdg_config_home, BASE_FOLDER, CONFIG_FILE_NAME)
    __ensure_folder_exists(USER_CONFIG)


def set_default_config(file_path):
    global DEFAULT_CONFIG
    from mycroft.util.log import LOG
    DEFAULT_CONFIG = file_path
    LOG.info(f"default config file changed to: {file_path}")


def get_xdg_base():
    global BASE_FOLDER
    return BASE_FOLDER


def get_config_locations(default=True, web_cache=True, system=True,
                         old_user=True, user=True):
    locs = []
    if default:
        locs.append(DEFAULT_CONFIG)
    if system:
        locs.append(SYSTEM_CONFIG)
    if web_cache:
        locs.append(WEB_CONFIG_CACHE)
    if old_user:
        locs.append(OLD_USER_CONFIG)
    if user:
        locs.append(USER_CONFIG)

    return locs


def get_webcache_location():
    return join(XDG.xdg_config_home, BASE_FOLDER, CONFIG_FILE_NAME)


def get_xdg_config_locations():
    # This includes both the user config and
    # /etc/xdg/mycroft/mycroft.conf
    xdg_paths = list(reversed(
        [join(p, get_config_filename())
         for p in XDG.load_config_paths(get_xdg_base())]
    ))
    return xdg_paths


def get_config_filename():
    return CONFIG_FILE_NAME


DEFAULT_CONFIG = join(dirname(__file__), CONFIG_FILE_NAME)
SYSTEM_CONFIG = os.environ.get('MYCROFT_SYSTEM_CONFIG',
                               f'/etc/{BASE_FOLDER}/{CONFIG_FILE_NAME}')
# Make sure we support the old location still
# Deprecated and will be removed eventually
OLD_USER_CONFIG = join(expanduser('~'), '.' + BASE_FOLDER, CONFIG_FILE_NAME)
USER_CONFIG = join(XDG.xdg_config_home, BASE_FOLDER, CONFIG_FILE_NAME)
REMOTE_CONFIG = "mycroft.ai"
WEB_CONFIG_CACHE = join(XDG.xdg_config_home, BASE_FOLDER, 'web_cache.json')


def __ensure_folder_exists(path):
    """ Make sure the directory for the specified path exists.

        Arguments:
            path (str): path to config file
     """
    directory = dirname(path)
    if not exists(directory):
        try:
            os.makedirs(directory)
        except:
            sleep(0.2)
            if not exists(directory):
                try:
                    os.makedirs(directory)
                except Exception as e:
                    from mycroft.util.log import LOG
                    LOG.exception(e)


__ensure_folder_exists(WEB_CONFIG_CACHE)
__ensure_folder_exists(USER_CONFIG)
