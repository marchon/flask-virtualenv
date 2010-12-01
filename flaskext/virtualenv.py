import subprocess
import os
import sys

app = None
env_name = '.%senv'

def _local(cmd, cwd=os.getcwd()):
    p = subprocess.Popen(cmd, shell=True, cwd=cwd, stderr=subprocess.STDOUT)
    if (p.wait() != 0):
        raise Exception()

def _pip(cmd=''):
    _local("./%s/bin/pip %s" % (env_name, cmd))

def _add_env_to_gitignore():
    if os.path.exists('.gitignore'):
        fp = open('.gitignore', 'a+')
        contents = fp.read()
        if not env_name in contents:
            fp.write('## Ignore virtual environment\n%s/\n' % (env_name))
            print "Added %s/ to your .gitignore" % env_name
        fp.close()
    
def _ensure_requirements_file():
    if not os.path.exists('requirements.text'):
        print "No requirements.txt file found.  See http://pip.openplans.org/requirement-format.html"
        sys.exit(1)

@manager.command
def requirements():
    """Print required packages and versions"""
    _ensure_requirements_file()
    _local("cat requirements.txt")

@manager.command
def make_requirements_file():
    """Generate new requirements file"""
    _ensure_requirements_file()
    _pip("freeze > requirements.txt")

@manager.command
def install():
    """Create new virtual environment and install all required packages"""
    _ensure_requirements_file()
    if not os.path.exists('env'):
        _local("virtualenv --no-site-packages --verbose --distribute --prompt=%s " % (app.name, env_name))
    if not os.path.exists('./%s/bin/pip' % env_name):
        _local("./%s/bin/easy_install pip" % (env_name))

    _pip("install -r requirements.txt")
    _add_env_to_gitignore()