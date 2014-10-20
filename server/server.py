"""This module implements a flask app that serves a website for viewing and configuring the
recognition automation and a REASTful API for reading the detection sensor."""

import flask
import sqlite3

DB_PATH   = "../"
DB_NAME = {
    "prefs": "preferences.sqlite",
    "sensor": "sensor.sqlite"
}

def get_database(db):
    ret = sqlite3.connect(DB_PATH + DB_NAME[db]);
    ret.row_factory = sqlite3.Row
    return ret

API_BASE = "/apiv0/"

app = flask.Flask(__name__)


# Website routes.
@app.route("/")
def hello_world():
    people = get_database("prefs").execute("SELECT * FROM people");
    return "Hello World!<br/>" + "<br/>".join(p["name"] for p in people)


# RESTful API stuff
def dict_from_row(row):
    return dict(zip(row.keys(), row))       

def not_found_json(message="The resource you requested doesn't exist."):
    """Returns stuff that flask will render as a json not found error response."""
    return json_error("Not Found", message, 404);

def json_error(code, error, message):
    """Returns stuff thta flask will render as a json error response."""
    return flask.jsonify({"error": error, "message": message}), code

# API routes.
@app.route(API_BASE + "people", methods=['GET'])
def list_people():
    people = get_database("prefs").execute("SELECT people.id, people.name FROM people");
    return flask.jsonify({"people": [dict_from_row(p) for p in people]})

@app.route(API_BASE + "people/<string:person>", methods=['GET'])
def get_person(person):
    people = get_database("prefs").execute("SELECT * FROM people WHERE id=?", (person,));
    p = people.fetchone()
    if not p: return not_found_json("The person '%s' doesn't exist." % person);
    return flask.jsonify(dict_from_row(p))



if __name__ == "__main__":
    app.run(debug=True)

