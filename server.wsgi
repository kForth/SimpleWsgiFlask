#!/usr/bin/python
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/path/to/your/server/")  # replace this path with the root path of your server (the directory with server.py), same as line 7 in your conf file.

from server import app as application # server is the module name, app is the Flask object
application.secret_key = 'ThisIsASecretKeyAndItsASecretSoShhh' # give your flask app a good secrey key or some other information