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
"""Common logic for instantiating the Mycroft Skills Manager.

The Mycroft Skills Manager (MSM) does a lot of interactions with git.  The
more skills that are installed on a device, the longer these interactions
take.  This is especially true at boot time when MSM is instantiated
frequently.  To improve performance, the MSM instance is cached.
"""
from collections import namedtuple
from functools import lru_cache
from os import path, makedirs
from xdg import BaseDirectory as XDG

from combo_lock import ComboLock
from mycroft.util.log import LOG
from mycroft.configuration import get_xdg_base, Configuration
from mock_msm import \
    MycroftSkillsManager as MockMSM, \
    SkillRepo as MockSkillRepo

try:
    from msm.exceptions import MsmException
    from msm import MycroftSkillsManager, SkillRepo
except ImportError:
    MycroftSkillsManager = MockMSM
    SkillRepo = MockSkillRepo
    from mock_msm.exceptions import MsmException


MsmConfig = namedtuple(
    'MsmConfig',
    [
        'platform',
        'repo_branch',
        'repo_url',
        'old_skills_dir',
        'versioned',
        'disabled'
    ]
)


def get_skills_directory():
    conf = Configuration.get(remote=False)
    path_override = conf["skills"].get("directory_override")
    # if .conf wants to use a specific path, use it!
    if path_override:
        skills_folder = path_override
    # if xdg is enabled, respect it!
    elif conf.get("disable_xdg"):
        skills_folder = None
    else:
        # create folder if needed
        skills_folder = XDG.save_data_path(get_xdg_base() + '/skills')
    return skills_folder


def _init_msm_lock():
    msm_lock = None
    try:
        msm_lock = ComboLock('/tmp/mycroft-msm.lck')
        LOG.debug('mycroft-msm combo lock instantiated')
    except Exception:
        LOG.exception('Failed to create msm lock!')

    return msm_lock


def build_msm_config(device_config: dict) -> MsmConfig:
    """Extract from the device configs values needed to instantiate MSM

    Why not just pass the device_config to the create_msm function, you ask?
    Rationale is that the create_msm function is cached.  The lru_cached
    decorator will instantiate MSM anew each time it is called with a different
    configuration argument.  Calling this function before create_msm will
    ensure that changes to configs not related to MSM will not result in new
    instances of MSM being created.
    """
    msm_config = device_config['skills']['msm']
    msm_repo_config = msm_config['repo']
    enclosure_config = device_config['enclosure']
    data_dir = path.expanduser(device_config['data_dir'])

    return MsmConfig(
        platform=enclosure_config.get('platform', 'default'),
        repo_branch=msm_repo_config['branch'],
        repo_url=msm_repo_config['url'],
        old_skills_dir=path.join(data_dir, msm_config['directory']),
        versioned=msm_config['versioned'],
        disabled=msm_config.get("disabled", False)
    )


@lru_cache()
def create_msm(msm_config: MsmConfig) -> MycroftSkillsManager:
    """Returns an instantiated MSM object.

    This function is cached because it can take as long as 15 seconds to
    instantiate MSM.  Caching the instance improves performance significantly,
    especially during the boot sequence when this function is called multiple
    times.
    """
    if msm_config.disabled:
        LOG.info("MSM is disabled, using mock_msm")
        repo_clazz = MockSkillRepo
        msm_clazz = MockMSM
    else:
        repo_clazz = SkillRepo
        msm_clazz = MycroftSkillsManager

    if msm_config.repo_url != "https://github.com/MycroftAI/mycroft-skills":
        LOG.warning("You have enabled a third-party skill store.\n"
                    "Unable to guarantee the safety of skills from "
                    "sources other than the Mycroft Marketplace.\n"
                    "Proceed with caution.")
    msm_lock = _init_msm_lock()
    LOG.info('Acquiring lock to instantiate MSM')
    with msm_lock:

        skills_folder = get_skills_directory()

        msm_skill_repo = repo_clazz(
            msm_config.repo_url,
            msm_config.repo_branch
        )
        # NOTE older versions of msm do not have old_skills_dir param
        # let's support that just in case, mycroft did a mess with msm,
        # it supports XDG but core doesnt, so there was a release of msm
        # after the xdg release that removes it???
        try:
            msm_instance = msm_clazz(
                platform=msm_config.platform,
                old_skills_dir=msm_config.old_skills_dir,
                repo=msm_skill_repo,
                skills_dir=skills_folder,
                versioned=msm_config.versioned
            )
        except:
            msm_instance = msm_clazz(
                platform=msm_config.platform,
                repo=msm_skill_repo,
                skills_dir=skills_folder,
                versioned=msm_config.versioned
            )
    LOG.info('Releasing MSM instantiation lock.')

    return msm_instance
