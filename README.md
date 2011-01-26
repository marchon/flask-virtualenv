Flask-Virtualenv

# Flask-Virtualenv

Manage a virtualenv for your flask app.

## Setup

Create a manage.py file for your project if you don't have one already like so:

    #!/usr/bin/env python
    from __future__ import absolute_import

    from flaskext.script import Manager
    from yourapplication import create_app
    from flaskext.virtualenv import install_commands as install_virtualenv_commands

    app = create_app()
    manager = Manager(app)
    install_virtualenv_commands(app)

    if __name__ == "__main__":
        manager.run()

If you already have a manage.py, you can just add the following:
    
    from flaskext.virtualenv import install_commands as install_virtualenv_commands
    ## ... Create manager
    ## ... Create app
    install_virtualenv_commands(app) # Make virtualenv commands available


## Usage

Create a new environment for the current project:
    
    ./manage.py env create

List the current requirements for the current project:
    
    ./manage.py env reqs

Recreate the requirements.txt file with all packages in the projects virtualenv:
    
    ./manage.py env buildreqs
