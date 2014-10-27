Overview
========
This directory holds a flask app to provide a web interface and a REST interface to our camera functionality.

Read about flaskl at flask.pocoo.org

Setup
=====
Python 2.7 or 3.4 is required (Raspbian Wheezy comes with 2.7 and 3.2).

Python3.4
---------
Install the python package manager pip3:

	$ sudo apt-get install python3-pip

Once installed the command should be named pip3.

Required Python packages are listed in requirements.txt. Install them using pip3 like so:

	$ pip3 install -r requirements.txt

Python2.7
---------
Install the python package manager pip:

	$ sudo apt-get install python-pip

Required Python packages are listed in requirements.txt. Install them using pip like so:

	$ pip install -r requirements.txt

Running
=======
Run server.py:

	$ python server.py

