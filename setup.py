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
import os
import os.path

from setuptools import setup, find_packages

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def get_version():
    """ Find the version of mycroft-core"""
    version = None
    version_file = os.path.join(BASEDIR, 'mycroft', 'version', '__init__.py')
    major, minor, build, date, patch = (None, None, None, None, None)
    with open(version_file) as f:
        for line in f:
            if 'CORE_VERSION_MAJOR' in line:
                major = line.split('=')[1].strip()
            elif 'CORE_VERSION_MINOR' in line:
                minor = line.split('=')[1].strip()
            elif 'CORE_VERSION_BUILD' in line:
                build = line.split('=')[1].strip()
            elif 'SYNC_DATE' in line:
                date = line.split('=')[1].split("#")[0].strip()
            elif 'PATCH_VERSION' in line:
                patch = line.split('=')[1].split("#")[0].strip()

            if ((major and minor and build and patch and date) or
                    '# END_VERSION_BLOCK' in line):
                break
    mycroft_version = '.'.join([major, minor, build])
    version = f'{date[:4]}.{date[4:6]}.{date[-2:]}.a{patch}'
    return version


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


setup(
    name='HolmesV',
    version=get_version(),
    license='Apache-2.0',
    url='https://github.com/HelloChatterbox/HolmesV',
    description='mycroft-core packaged as a library you can rely on',
    install_requires=required('requirements/minimal.txt'),
    extras_require={
        'audio-backend': required('requirements/extra-audiobackend.txt'),
        'mark1': required('requirements/extra-mark1.txt'),
        'stt': required('requirements/extra-stt.txt'),
        'tts': required('requirements/extra-tts.txt'),
        "skills_minimal": required('requirements/extra-skills-minimal.txt'),
        'skills': required('requirements/extra-skills.txt'),
        'default_skills': required('requirements/extra-default-skills.txt'),
        'enclosure': required('requirements/extra-enclosure.txt'),
        'bus': required('requirements/extra-bus.txt'),
        'all': required('requirements/requirements.txt'),
        'mycroft': required('requirements/extra-mycroft.txt')
    },
    packages=find_packages(include=['mycroft*']),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'mycroft-speech-client=mycroft.client.speech.__main__:main',
            'mycroft-messagebus=mycroft.messagebus.service.__main__:main',
            'mycroft-skills=mycroft.skills.__main__:main',
            'mycroft-audio=mycroft.audio.__main__:main',
            'mycroft-echo-observer=mycroft.messagebus.client.ws:echo',
            'mycroft-audio-test=mycroft.util.audio_test:main',
            'mycroft-enclosure-client=mycroft.client.enclosure.__main__:main',
            'mycroft-cli-client=mycroft.client.text.__main__:main'
        ]
    }
)
