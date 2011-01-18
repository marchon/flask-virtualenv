from __future__ import absolute_import

import os
import subprocess

from flaskext import script
import string


__all__ = ['install_commands']

DEFAULT_REQUIREMENTS = """### Required Packages ###
Flask
Flask-Script
# Flask-Virtualenv
-e git+https://github.com/imlucas/flask-virtualenv.git#egg=Flask-Virtualenv
"""


def _local(cmd, cwd=os.getcwd()):
    """Simple helper for executing shell."""
    print 'Execute: `%s` from `%s`' % (cmd, cwd)
    p = subprocess.Popen(cmd, shell=True, cwd=cwd, stderr=subprocess.STDOUT)
    if (p.wait() != 0):
        raise Exception()


def _ensure_requirements_file():
    """Make sure we have a requirements.txt file in our project.  If not,
    make one with the contents of DEFAULT_REQUIREMENTS"""
    if not os.path.exists('requirements.text'):
        fp = open('requirements.txt', 'w')
        fp.write(DEFAULT_REQUIREMENTS)
        fp.close()
        print 'Created default requirements file.'

class VirtualenvCommand(script.Command):
    """Easily manage this app's virtualenv."""
    def __init__(self, manager=None):
        self._env_name = "env"
        self._app_name = "app" if not manager else manager.app.logger_name

    def get_options(self):
        return [
            script.Option(dest='action', default='create', nargs=1,
                help="./manage.py env (create|reqs|buildreqs|destroy|activate)")
        ]

    def run(self, action):
        a = action[0]
        if hasattr(self, a):
            return getattr(self, a)()
        else:
            print "Unknown action %s" % a
    
    def create(self):
        """Create new virtual environment and install all required packages.

        If a .gitignore is present, an entry will be added so the env in ignored.
        """
        _ensure_requirements_file()
        if not os.path.exists('_env_name'):
            _local('virtualenv --no-site-packages --distribute --prompt="%s>" %s'
                % (self._app_name, self._env_name))

        if not os.path.exists('./%s/bin/pip' % self._env_name):
            _local('./%s/bin/easy_install pip' % (self._env_name))

        _local('./%s/bin/pip install -r requirements.txt' % self._env_name)

        # Add env to .gitignore
        if os.path.exists('.gitignore'):
            fp = open('.gitignore', 'a+')
            contents = fp.read()
            if not _env_name in contents:
                fp.write('## Ignore virtual environment\n%s/\n' % (self._env_name))
                print 'Added %s/ to your .gitignore' % self._env_name
            fp.close()
        self.activate()
    
    def reqs(self):
        """Print required packages and versions"""
        _ensure_requirements_file()
        _local('cat requirements.txt')

    def buildsreqs(self):
        """Generate new requirements file"""
        _ensure_requirements_file()
        _local('./%s/bin/pip freeze > requirements.txt' % self._env_name)
    
    def activate(self):
        print 'Run: source %s' % './%s/bin/activate' % self._env_name
    
    def destroy(self):
        _local('rm -rf %s' % self._env_name)
    

def install_commands(manager):
    manager.add_command('env', VirtualenvCommand(manager))