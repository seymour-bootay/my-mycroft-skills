# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.


# Visit https://docs.mycroft.ai/skill.creation for more detailed information
# on the structure of this skill and its containing folder, as well as
# instructions for designing your own skill based on this template.


# Import statements: the list of outside modules you'll be using in your
# skills, whether from other files in mycroft-core or from external libraries
# ********************************************************************************************************
# *WARNING* This skill is not secure and bypasses login authentication.  Use with protection and caution.*
# ********************************************************************************************************

from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

import subprocess
import time

__author__ = 'seymour-bootay'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)


class LoginctlSkill(MycroftSkill):
    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(LoginctlSkill, self).__init__(name="LoginctlSkill")

    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        self.load_data_files(dirname(__file__))

        unlocker_intent = IntentBuilder("UnlockerIntent"). \
            require("UnlockKeyword").build()
        self.register_intent(unlocker_intent,
                             self.handle_unlocker_intent)

        locker_intent = IntentBuilder("LockerIntent"). \
            require("LockKeyword").build()
        self.register_intent(locker_intent,
                             self.handle_locker_intent)

    def handle_unlocker_intent(self, message):
        p = subprocess.Popen(['loginctl', 'unlock-session'], shell=False, stdout=subprocess.PIPE)

        # Wait until process terminates
        while p.poll() is None:
            time.sleep(0.5)

        if p.poll() == 0:
            self.speak_dialog("unlocked")
        else:
            self.speak_dialog("unlock.error")

    def handle_locker_intent(self, message):
        p = subprocess.Popen(['loginctl', 'lock-session'], shell=False, stdout=subprocess.PIPE)

        # Wait until process terminates
        while p.poll() is None:
            time.sleep(0.5)

        if p.poll() == 0:
            self.speak_dialog("locked")
        else:
            self.speak_dialog("lock.error")

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, the method just contains the keyword "pass", which
    # does nothing.
    def stop(self):
        pass


# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return LoginctlSkill()
