"""This module implements a flask app that serves a website for viewing and configuring the
recognition automation and a REASTful API for reading the detection sensor."""

from flask import Flask
import sqlite3

DB_PATH     = "../"
PREFERENCES_DB = DB_PATH + "preferences.sqlite"
EVENTS_DB   = DB_PATH + "events.sqlite"

app = Flask(__name__)

@app.route("/")
def hello_world():
    preferences = sqlite3.connect(PREFERENCES_DB);
    people = preferences.execute("SELECT * FROM people");
    return "Hello World!<br/>" + "<br/>".join(map(str, people))


if __name__ == "__main__":
    app.run(debug=True)

