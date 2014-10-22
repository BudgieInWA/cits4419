"""This module implements a flask app that serves a website for viewing and configuring the
recognition automation and a REASTful API for reading the detection sensor."""

import flask
import sqlite3
import re

API_BASE = "/apiv0/"

DB_PATH   = "../"
DB_NAME = {
    "prefs": "preferences.sqlite",
    "sensor": "sensor.sqlite"
}

def get_database(db):
    """Loads the 'prefs' or the 'sensor' database and returns the sqlite connection object."""
    ret = sqlite3.connect(DB_PATH + DB_NAME[db]);
    ret.row_factory = sqlite3.Row
    return ret


app = flask.Flask(__name__)


pattern = re.compile("pts\[([a-z]+)\]\[([0-9]+)\]")
def save_prefs(prefs, data):
    for k in data:
        res = pattern.match(k) 
        if res:
            p = res.group(1)
            s = int(res.group(2))

            if data[k] == 'notset':
                prefs.execute("DELETE FROM person_to_switch WHERE person=? AND switch=?",
                        (p, s))
            else:
                if data[k] == 'on': v = 1
                elif data[k] == 'off': v = 0
                else: continue;
                prefs.execute("REPLACE INTO person_to_switch VALUES(?,?,?)",
                        (p,s,v))

# Website routes.
@app.route("/")
def hello_world():
    people = get_database("prefs").execute("SELECT * FROM people");
    return "Hello World!<br/>" + "<br/>".join(p["name"] for p in people)

@app.route("/people", methods=["GET"])
def site_list_people():
    people = get_database("prefs").execute("SELECT * FROM people");
    return "List of people:<br/>" + "<br/>".join(p["name"] for p in people)

@app.route("/people/<string:person>", methods=["GET", "POST"])
def site_person_settings(person):
    prefs = get_database("prefs")
    
    if flask.request.method == 'POST':
        save_prefs(prefs, flask.request.form)

    people = prefs.execute("SELECT * FROM people WHERE id=?",
            (person,));
    p = people.fetchone()
    if not p: abort(404, "Person %s couldn't be found"%person)
    
    entries = prefs.execute("SELECT * FROM person_to_switch WHERE person=?",
            (person,))
    vals = {}
    for e in entries:
        vals[e['switch']] = e['state']

    out = [p['name'] + " Settings"]

    switches = prefs.execute("SELECT * FROM switches")
    for s in switches:
        state = "not set"
        if s['id'] in vals:
            state = "on" if vals[s['id']] else "off"
        out.append("switch %d is %s" % (s['id'], state))

    return "<br/>".join(out)

@app.route("/switches", methods=["GET"])
def site_list_switches():
    switches = get_database("prefs").execute("SELECT * FROM switches");
    return "List of switches:<br/>" + "<br/>".join(s["description"] for s in switches)

@app.route("/switches/<int:switch>", methods=["GET", "POST"])
def site_switch_details(switch):
    prefs = get_database("prefs")

    if flask.request.method == 'POST':
        save_prefs(prefs, flask.request.form)

    switches = prefs.execute("SELECT * FROM switches WHERE id=?",
            (switch,));
    s = switches.fetchone()
    if not s: abort(404, "Switch %s couldn't be found"%switch)
    
    entries = prefs.execute("SELECT * FROM person_to_switch WHERE switch=?",
            (switch,))
    vals = {}
    for e in entries:
        vals[e['person']] = e['state']

    out = [s['description'] + " Settings"]

    people = prefs.execute("SELECT * FROM people")
    for p in people:
        state = "not set"
        if p['id'] in vals:
            state = "on" if vals[p['id']] else "off"
        out.append("person %s makes this %s" % (p['name'], state))

    return "<br/>".join(out)

# RESTful API stuff
def dict_from_row(row):
    """Converts an sqlite3.Row into a python dict."""
    return dict(zip(row.keys(), row))       

def not_found_json(message="The resource you requested doesn't exist."):
    """Returns stuff that flask will render as a 'not found' error response in json."""
    return json_error("Not Found", message, 404);

def json_error(error, message, code):
    """Returns stuff that flask will render as an error response in json."""
    return flask.jsonify({"error": error, "message": message}), code

def get_last_seen(person):
    """Returns the last time the person was recognised, or '0000-00-00 00:00:00' for 'never'."""
    events = get_database("sensor").execute(
            "SELECT datetime FROM recognition_events WHERE person=? " +
            "ORDER BY datetime DESC LIMIT 1",
            (person,))
    event = events.fetchone()
    return event["datetime"] if event else "0000-00-00 00:00:00"

# API routes.
@app.route(API_BASE + "<path:garbage>")
def bad_api_call(garbage):
    """Catches unknown urls under the API "dir" to render a json 404."""
    return not_found_json("The url you are requesting isn't a valid api url.")

@app.route(API_BASE + "people", methods=['GET'])
def list_people():
    people = get_database("prefs").execute("SELECT people.id, people.name FROM people");
    resp = {"people": []}
    for p in people:
        d = dict_from_row(p)
        d["last_seen"] = get_last_seen(p["id"])
        resp["people"].append(d)
    return flask.jsonify(resp)

@app.route(API_BASE + "people/<string:person>", methods=['GET'])
def get_person(person):
    people = get_database("prefs").execute("SELECT * FROM people WHERE id=?", (person,));
    p = people.fetchone()
    if not p: return not_found_json("The person '%s' doesn't exist." % person);
    d = dict_from_row(p)
    d["last_seen"] = get_last_seen(p["id"])
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

