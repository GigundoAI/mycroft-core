# Copyright 2017 Mycroft AI Inc.
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
from setuptools import setup, find_packages

setup(
    name='HolmesV',
    version="2021.5.6a11",
    license='Apache-2.0',
    url='https://github.com/HelloChatterbox/HolmesV',
    description='mycroft-core packaged as a library you can rely on',
    install_requires=["requests",
                      "pyee",
                      "pyxdg",
                      "mycroft-messagebus-client==0.9.1",
                      "inflection",
                      "psutil",
                      "combo_lock",
                      "mock_msm",
                      "python-dateutil==2.6.0",
                      "requests-futures"],
    extras_require={
        "lingua_franca": ["lingua_franca>=0.3.1"],
        "lingua_nostra": ["lingua-nostra>=0.4.2"],
        "bus": ["tornado==6.0.3"],
        "enclosure": ["tornado==6.0.3"],
        "skills_minimal": ["adapt-parser>=0.3.7", "padaos>=0.1.9",
                           "lingua-nostra>=0.4.2"],
        "skills": ["adapt-parser>=0.3.7",
                   "padatious==0.4.8",
                   "fann2==1.0.7",
                   "padaos==0.1.9",
                   "lingua-nostra>=0.4.0a4",
                   "mock_msm"],
        "stt": ["SpeechRecognition==3.8.1",
                "PyAudio==0.2.11",
                "pocketsphinx==0.1.0",
                "precise-runner==0.2.1"],
        "mark1": ["pyalsaaudio==0.8.2"],
        "audio": [],
        "audio_engines": ["pychromecast==3.2.2", "python-vlc==1.1.2"],
        "stt_engines": ["google-api-python-client==1.6.4"],
        "tts_engines": ["gTTS>=2.2.0"],
        "mycroft": ["tornado==6.0.3",
                    "adapt-parser==0.3.7",
                    "padatious==0.4.8",
                    "fann2==1.0.7",
                    "padaos==0.1.9",
                    "lingua_franca>=0.3.1",
                    "msm==0.9.0",
                    "SpeechRecognition==3.8.1",
                    "PyAudio==0.2.11",
                    "pocketsphinx==0.1.0",
                    "precise-runner==0.2.1",
                    "pyalsaaudio==0.8.2",
                    "python-vlc==1.1.2",
                    "pychromecast==3.2.2",
                    "google-api-python-client==1.6.4",
                    "gTTS>=2.2.0"],
        "all": ["tornado==6.0.3",
                "adapt-parser==0.3.7",
                "padatious==0.4.8",
                "fann2==1.0.7",
                "padaos==0.1.9",
                "lingua-nostra>=0.4.2",
                "mock_msm",
                "SpeechRecognition==3.8.1",
                "PyAudio==0.2.11",
                "pocketsphinx==0.1.0",
                "precise-runner==0.2.1",
                "pyalsaaudio==0.8.2",
                "python-vlc==1.1.2",
                "pychromecast==3.2.2",
                "google-api-python-client==1.6.4",
                "gTTS>=2.2.0"]

    },
    packages=find_packages(include=['mycroft*']),
    include_package_data=True
)
