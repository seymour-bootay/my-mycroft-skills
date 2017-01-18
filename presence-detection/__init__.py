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
from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

import json
import requests

__author__ = 'seymour-bootay'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)


class PresenceDetectionSkill(MycroftSkill):
    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(PresenceDetectionSkill, self).__init__(name="PresenceDetectionSkill")
        self.presence_system = self.config['presence_system']
        self.presence_url = self.config['presence_url']

    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        self.load_data_files(dirname(__file__))

        presence_detection_intent = IntentBuilder("PresenceDetectionIntent"). \
            require("LocateBeaconKeyword").require("Beacon").build()
        self.register_intent(presence_detection_intent,
                             self.handle_presence_detection_intent)

    def handle_presence_detection_intent(self, message):

        beacon_name = message.data.get("Beacon").lower()

        where = self.get_location(beacon_name)

        data = {
            "beacon_name": beacon_name,
            "where": where
        }

        if where is not None:
            self.speak_dialog("located", data)
        else:
            self.speak_dialog("could.not.locate", data)

    def process_beacons_happy_bubbles(self):
        beacon_dict = {}
        response = requests.get(self.presence_url)
        json_data = json.loads(response.text)
        for key, value in json_data['beacons'].iteritems():
            beacon_name = str(value['name']).lower()
            location = value['incoming_json']['hostname']

            beacon_dict[beacon_name] = location

        return beacon_dict

    def get_location(self, beacon_name):
        if self.presence_system is None:
            self.speak_dialog("presence.system.not.configured")
        elif self.presence_system == 'happy-bubbles':
            beacon_dict = self.process_beacons_happy_bubbles()
        else:
            # the configured presence system is not supported.
            data = {
                "presence_system": self.presence_system
            }

            self.speak_dialog("presence.system.not.supported", data)

        return beacon_dict.get(beacon_name)

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, the method just contains the keyword "pass", which
    # does nothing.
    def stop(self):
        pass


# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return PresenceDetectionSkill()
