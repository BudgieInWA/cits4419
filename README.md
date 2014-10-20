We use OpenCV to perform facial recognition to identify users.

Code Overview
=============

The .schema.sql files in this directory describe the databases that are used to communicate between
the components.

The code in sensor/ reads camera data and every time it recognises a user, it writes to the shared
database.

The code in server/ is a server that publishes the sensor data to through a REASful API and
publishes a web site that allows users to set preferences.

The code in automate/ listens for new sensor outputs and, using the user specified preferences,
toggles some switches, using a remote API (provided by other devices on the network).

Instillation
============

1. Set up Rasperry Pi with camera, verify with raspicam.
2. Clone this repo onto the pi.
3. Install sqlite3 if it's not installed: sudo apt-get install sqlite3.
3. Run init-db.sh.
4. Set up the preferences database to reflect the house / users (or run init-db-testdata.sh).
4. Follow the instructions in each each of the three subdirectories mentioned above.
