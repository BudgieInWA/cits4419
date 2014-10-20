sqlite3 preferences.sqlite < preferences.schema.sql && echo "Created preferences.sqlite" &&
sqlite3 sensor.sqlite < sensor.schema.sql && echo "Created sensor.sqlite" &&
echo "All done creating databases :)"

