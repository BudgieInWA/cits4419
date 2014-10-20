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

def get_person_last_seen(person):
    events = get_database("sensor").execute(
            "SELECT datetime FROM recognition_events WHERE person=? " +
            "ORDER BY datetime DESC LIMIT 1",
            (person,))
    event = events.fetchone()
    return event["datetime"] if event else "0000-00-00 00:00:00"

# API routes.
@app.route(API_BASE + "<path:garbage>")
def bad_api_call(garbage):
    return not_found_json("The url you are requesting isn't a valid api url.")

@app.route(API_BASE + "people", methods=['GET'])
def list_people():
    people = get_database("prefs").execute("SELECT people.id, people.name FROM people");
    resp = {"people": []}
    for p in people:
        d = dict_from_row(p)
        d["last_seen"] = get_person_last_seen(p["id"])
        resp["people"].append(d)
    return flask.jsonify(resp)

@app.route(API_BASE + "people/<string:person>", methods=['GET'])
def get_person(person):
    people = get_database("prefs").execute("SELECT * FROM people WHERE id=?", (person,));
    p = people.fetchone()
    if not p: return not_found_json("The person '%s' doesn't exist." % person);
    d = dict_from_row(p)
    d["last_seen"] = get_person_last_seen(p["id"])
    return flask.jsonify(d)

@app.route(API_BASE + "events", methods=['GET'])
def list_events():
    where = " WHERE datetime > :dt "
    params = {"dt": flask.request.args["after"] if "after" in flask.request.args else "0000-00-00 00:00:00"}
    if "person" in flask.request.args:
        where += " AND person = :person "
        params["person"] = flask.request.args["person"]

    events = get_database("sensor").execute(
        "SELECT * FROM recognition_events" + where + "ORDER BY datetime DESC",
        params);
    return flask.jsonify({"events": [dict_from_row(e) for e in events]})


if __name__ == "__main__":
    app.run(debug=True)

