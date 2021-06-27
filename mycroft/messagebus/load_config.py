# Copyright 2019 Mycroft AI Inc.
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
#
"""Message bus configuration loader.

The message bus event handler and client use basically the same configuration.
This code is re-used in both to load config values.
"""
from collections import namedtuple

from mycroft.configuration import Configuration
from mycroft.util.log import LOG
from mycroft.util.json_helper import merge_dict


def get_bus_config(overrides=None):
    overrides = overrides or {}
    try:
        config = Configuration.get(remote=False)
        cfg = config['websocket']
        if cfg.get("use_chatterbox"):
            # chatterbox bus client is a drop in replacement,
            # it adds functionality to encrypt payloads
            from chatterbox_bus_client.conf import get_bus_config as \
                _cb_bus_cfg
            cfg = _cb_bus_cfg()
        merge_dict(cfg, overrides)
        return cfg
    except KeyError as ke:
        LOG.error('No websocket configs found ({})'.format(repr(ke)))
        raise


MessageBusConfig = namedtuple(
    'MessageBusConfig',
    ['host', 'port', 'route', 'ssl']
)


def load_message_bus_config(**overrides):
    """Load the bits of device configuration needed to run the message bus."""
    LOG.info('Loading message bus configs')
    websocket_configs = get_bus_config(overrides)
    mb_config = MessageBusConfig(
        host=websocket_configs.get('host'),
        port=websocket_configs.get('port'),
        route=websocket_configs.get('route'),
        ssl=websocket_configs.get('ssl')
    )
    if not all([mb_config.host, mb_config.port, mb_config.route]):
        error_msg = 'Missing one or more websocket configs'
        LOG.error(error_msg)
        raise ValueError(error_msg)

    return mb_config
