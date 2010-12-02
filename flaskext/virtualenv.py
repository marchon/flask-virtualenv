import os
import subprocess

__all__ = ['install_commands']

def _local(cmd, cwd=os.getcwd()):
    print "Execute: `%s` from `%s`" % (cmd, cwd)
    p = subprocess.Popen(cmd, shell=True, cwd=cwd, stderr=subprocess.STDOUT)
    if (p.wait() != 0):
        raise Exception()
    
def _ensure_requirements_file():
    # if not os.path.exists('requirements.text'):
    #         print "No requirements.txt file found.  See http://pip.openplans.org/requirement-format.html"
    #         sys.exit(1)
    if not os.path.exists('requirements.text'):
        _local('echo "### Required Packages ###\nFlask\nFlask-Script" > requirements.txt')
        print "Created requirements file."

def install_commands(manager):
    _app_name = manager.app.logger_name
    _env_name = ".%senv" % _app_name
    
    @manager.command
    def requirements():
        """Print required packages and versions"""
        _ensure_requirements_file()
        _local("cat requirements.txt")

    @manager.command
    def make_requirements_file():
        """Generate new requirements file"""
        _ensure_requirements_file()
        _local("./%s/bin/pip freeze > requirements.txt" % _env_name)

    @manager.command
    def install_virtualenv():
        """Create new virtual environment and install all required packages"""
        _ensure_requirements_file()
        
        if not os.path.exists('_env_name'):
            _local("virtualenv --no-site-packages --verbose --distribute --prompt=%s %s" % (_app_name, _env_name))
        if not os.path.exists('./%s/bin/pip' % _env_name):
            _local("./%s/bin/easy_install pip" % (_env_name))

        _local("./%s/bin/pip install -r requirements.txt" % _env_name)
        
        # Add env to .gitignore
        if os.path.exists('.gitignore'):
            fp = open('.gitignore', 'a+')
            contents = fp.read()
            if not _env_name in contents:
                fp.write('## Ignore virtual environment\n%s/\n' % (_env_name))
                print "Added %s/ to your .gitignore" % _env_name
            fp.close()
        
        activate_virtualenv()
        
    @manager.command
    def destroy_virtualenv():
        _local("virtualenv --clear %s")
        
    @manager.command
    def activate_virtualenv():
        _local('source %s' % './%s/bin/activate' % _env_name)        