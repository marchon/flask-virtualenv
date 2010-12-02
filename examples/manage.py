#!/usr/bin/env python
from __future__ import absolute_import
from flaskext.script import Manager
from flaskext.virtualenv import install_commands as install_virtualenv_commands
from flask import Flask

app = Flask("myapp")

manager = Manager(app)
install_virtualenv_commands(manager)

if __name__ == "__main__":
    manager.run()