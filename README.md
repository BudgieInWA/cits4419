We use OpenCV to perform facial recognition to identify users. When a user is recognised, switches
are turned on or off using the switches api depending on the user inputted preferences.

Code Overview
=============

The .schema.sql files in this directory describe the databases that are used to store preferences
and recognition events.

The code in sensor/ reads camera data and every time it recognises a user, it calls the
automate/event.py script with details of the recognition event.

The code in automate/ uses the user specified preferences from the database to toggles some
switches, using a remote API (provided by other devices on the network). The event is also written
to a database for further querying.

The code in server/ is a server that publishes the sensor data to through a REASful API and
publishes a web site that allows users to set preferences.


Instillation
============

TODO make this verbose and precise.

Set up Rasperry Pi with camera, verify with raspicam.

Set the time on your pi. You can do this using the `date` command line tool:

	$ date --set="23 June 2010 10:00:00" 

Clone this repo onto the pi.

	$ git clone <url of this repo>

Install sqlite3 if it's not installed: sudo apt-get install sqlite3.

Set up the database:

	$ ./init-db.sh

Set up the preferences database to reflect the house / users (or run init-db-testdata.sh).

Follow the instructions in each each of the three subdirectories mentioned above.
