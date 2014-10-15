We use OpenCV to perferm facial recognition to identify users. The code in sensor/ reads camera data
and every time it recognises a user, it writes to an SQLite database.

The code in server/ is a server that publishes the sensor data to through a REASful API and
publishes a web site that allows users to set preferences.

The code in automate/ listens for new sensor outputs and, using the user specified preferences,
toggles some switches, using a remote API (provided by other devices on the network).
