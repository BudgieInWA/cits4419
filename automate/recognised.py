"""Responds to a person being recognised and stores the event in the database."""

import os
import sqlite3
import datetime
import requests
import json


DB_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
DB_NAME = {
    "prefs": "preferences.sqlite",
    "sensor": "sensor.sqlite"
}

SWITCH_URL = 'TODO'

def get_database(db):
    """Loads the 'prefs' or the 'sensor' database and returns the sqlite connection object."""
    ret = sqlite3.connect(os.path.join(DB_PATH, DB_NAME[db]));
    ret.row_factory = sqlite3.Row
    return ret

def record_recognition(person):
	sensor = get_database('sensor')
	time = datetime.datetime.now()

	sensor.execute("INSERT INTO recognition_events VALUES (?, ?)",
			(person, time))
        sensor.commit()

def send_json_put(url, payload):
	headers = {'content-type': 'application/json'}
	print "only pretending to send %s" % json.dumps(payload)
	return #TODO
	requests.put(url,
				 data=json.dumps(payload),
				 headers=headers)


def recognition_action(person):
	prefs = get_database('prefs')
	actions = prefs.execute("SELECT * FROM person_to_switch WHERE person=?",
			(person,))
	for a in actions:
		payload = {'switch': a['switch'], 'state':a['state']}
		send_json_put(SWITCH_URL+"/"+str(a['switch']), payload)
	
def usage(script):
	print "Usage: %s <person>" % script
	print "\tRespond to a person being recognised."
	print "\t<person>\tthe id of the person recognised."

def main(script, person=None):
	if not person:
		return usage(script)

	record_recognition(person)
	recognition_action(person)

if __name__ == '__main__':
	import sys
	main(*sys.argv)
