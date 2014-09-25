import os
import sys
import site

from colorama import init as color_init
from colorama import Fore, Style
from unipath import Path


def get_env_variable(name):
    """ Gets the specified environment variable.

    :param name: The name of the variable.
    :type name: str
    :returns: The value of the specified variable.
    :raises: **ImproperlyConfigured** when the specified variable does not exist.

    """

    try:
        return os.environ[name]
    except KeyError:
        error_msg = "Error: The %s environment variable is not set!" % name
        color_init()
        sys.stderr.write(Fore.RED + Style.BRIGHT + error_msg + "\n")
        sys.exit(1)


source_dir = Path(get_env_variable('PROJECT_HOME'))
virtualenv_dir = Path(get_env_variable('WORKON_HOME'))

filepath = Path(__file__).absolute()
repo_dir = filepath.ancestor(3).components()[-1]
project_dir = filepath.ancestor(2).components()[-1]

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir(virtualenv_dir.child(repo_dir, "Lib", "site-packages"))

# Add the app's directory to the PYTHONPATH
sys.path.append(filepath.ancestor(2))
sys.path.append(filepath.ancestor(2).child(project_dir))

# Set manually in environment
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

# Activate the virtual env
activate_env = virtualenv_dir.child(repo_dir, "Scripts", "activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django
from django.core.handlers.wsgi import WSGIHandler
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

django.setup()

# Send any wsgi errors to Sentry
application = Sentry(WSGIHandler())
