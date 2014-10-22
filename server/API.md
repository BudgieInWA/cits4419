Introduction
============

This API allows clients to request recongnition events and last seen times of
people in a RESTful manner. See the sections below for the request types that
can be made.

All requests should be GET requests and all responses are in the form of a JSON
object.

Parameters are provided in the query string.

People
======

The people that the sensor can recognise.

apiv1/people
------------

List the people that the sensor can recognise.

If a person hasn't ever been recognised by the sensor, the last_seen field will
be "0000-00-00 00:00:00".

Example Response:
```json
{
  "people": [
	{
	  "id": "alice",
	  "last_seen": "2014-04-04 9:00:00",
	  "name": "Alice"
	},
	{
	  "id": "bob",
	  "last_seen": "2014-04-05 10:00:00",
	  "name": "Bob"
	},
	{
	  "id": "cyril",
	  "last_seen": "0000-00-00 00:00:00",
	  "name": "Cyril"
	}
  ]
}	
```

apiv1/people/<string:id>
------------------------

Get the details of a specific person.

Example Response for `apiv1/people/bob`:

```json
{
  "id": "bob",
  "last_seen": "2014-04-05 10:00:00",
  "name": "Bob"
}
```

Events
======

The sensor emits a recognition event whenever it recognises someone.

apiv1/events
------------

List recognition events, newest first.

Parameters:

* person (optional): list events relating to this person only.
* after (optional): list events after the given timestamp. The timestamp may be
  incomplete.

New events will never have a timestamp earlier than the timestamp on any
previously returned event. Because of this, it is recommended that any
subsequent requests you make include the timestamp of the most recent event you
have recieved.

Example Response for `apiv1/events`:

```json
{
  "events": [
    {
      "datetime": "2014-04-05 10:00:00",
      "person": "bob"
    },
    {
      "datetime": "2014-04-04 9:00:00",
      "person": "alice"
    },
    {
      "datetime": "2014-04-04 10:00:00",
      "person": "alice"
    },
    {
      "datetime": "2014-04-02 10:00:00",
      "person": "bob"
    },
    {
      "datetime": "2014-04-01 10:00:00",
      "person": "bob"
    }
  ]
}
```

Example Response for `apiv1/events?after=2014-04-04%2010:00:00`:
```json
{
  "events": [
    {
      "datetime": "2014-04-05 10:00:00",
      "person": "bob"
    },
    {
      "datetime": "2014-04-04 9:00:00",
      "person": "alice"
    }
  ]
}
```

Errors
======

Errors will be in the form of a JSON object with an "error" field and a human
readable "message" field.

Example Response for `apiv1/wally`
```json
{
  "error": "Not Found",
  "message": "The url you are requesting isn't a valid api url."
}
```
