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

try:
    # chatterbox bus client is a drop in replacement, it adds functionality
    # to encrypt payloads, this is done transparently from the .conf
    from chatterbox_bus_client.conf import get_bus_config
except ImportError:
    def get_bus_config():
        try:
            config = Configuration.get(remote=False)
            return config['websocket']
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
    websocket_configs = get_bus_config()

    mb_config = MessageBusConfig(
        host=overrides.get('host') or websocket_configs.get('host'),
        port=overrides.get('port') or websocket_configs.get('port'),
        route=overrides.get('route') or websocket_configs.get('route'),
        ssl=overrides.get('ssl') or websocket_configs.get('ssl')
    )
    if not all([mb_config.host, mb_config.port, mb_config.route]):
        error_msg = 'Missing one or more websocket configs'
        LOG.error(error_msg)
        raise ValueError(error_msg)

    return mb_config
