#
# Copyright 2020 Mycroft AI Inc.
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

"""
The mycroft.util.lang module provides the main interface for setting up the
lingua-franca (https://github.com/mycroftai/lingua-franca) selected language
"""
try:
    from lingua_franca import set_default_lang, get_default_lang, load_languages
except ImportError:
    _lang = "en-us"

    def get_default_lang():
        return _lang

    def set_default_lang(lang):
        global _lang
        _lang = lang

    def load_languages(*args, **kwargs):
        pass


