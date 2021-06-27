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
from mycroft.configuration import Configuration
from mycroft.messagebus.load_config import get_bus_config
from mycroft.util.log import LOG
from mycroft.util.process_utils import create_echo_function
from mycroft_bus_client import MessageBusClient as _MessageBusClient
from mycroft_bus_client.client import MessageWaiter


class MessageBusClient(_MessageBusClient):
    def __new__(cls, *args, **kwargs):
        # get default arguments from config
        bus_config = get_bus_config(**kwargs)
        kwargs["host"] = kwargs.get("host") or bus_config.get("host",
                                                              "0.0.0.0")
        kwargs["port"] = kwargs.get("port") or bus_config.get("port", 8181)
        kwargs["route"] = kwargs.get("route") or bus_config.get("route",
                                                                "/core")
        kwargs["ssl"] = kwargs.get("ssl") or bus_config.get("ssl", False)

        if bus_config.get("use_chatterbox"):
            LOG.info("Using chatterbox_bus_client")
            # chatterbox bus client is a drop in replacement, it adds functionality
            # to encrypt payloads, this is done transparently from the .conf
            from chatterbox_bus_client import \
                MessageBusClient as ChatterboxMessageBusClient
            return ChatterboxMessageBusClient(*args, **kwargs)
        return super().__new__(cls)


def echo():
    message_bus_client = MessageBusClient()

    def repeat_utterance(message):
        message.msg_type = 'speak'
        message_bus_client.emit(message)

    message_bus_client.on('message', create_echo_function(None))
    message_bus_client.on('recognizer_loop:utterance', repeat_utterance)
    message_bus_client.run_forever()


if __name__ == "__main__":
    echo()
