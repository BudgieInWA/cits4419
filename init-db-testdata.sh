
sqlite3 preferences.sqlite < preferences-test.sql && echo "Preferences test data added."
sqlite3 sensor.sqlite < sensor-test.sql && echo "Sensor test data added."

echo "All done adding test data :)"
