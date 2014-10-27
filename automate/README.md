Overview
========
This is responsible for reacting to sensor recognition events and performing the automation.

Setup
=====

Python2.7
---------
If you are using python2.7 you need some dependencies:

Install the python package manager pip if needed:

	$ sudo apt-get install python-pip

Required Python packages are listed in requirements.txt. Install them using pip like so:

	$ pip install -r requirements.txt

Running
=======
This Script does not constantly run, but instead should be called whenever a person is recognised:

	$ python recognised.py bob
