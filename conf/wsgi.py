#!/usr/bin/env python3.4
import os
import sys
import site
import re

from colorama import init as color_init
from termcolor import colored
from pathlib import Path


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
        error_msg = "Error: The {variable_name} environment variable is not set!\n".format(variable_name=name)
        color_init()
        sys.stderr.write(colored(text=error_msg, color='red', attrs=['bold']))
        sys.exit(1)


def activate_env():
    """ Activates the virtual environment for this project."""

    virtualenv_home = Path(get_env_variable("WORKON_HOME"))
    project_home = Path(get_env_variable("PROJECT_HOME"))

    filepath = Path(__file__).resolve()
    repo_name = filepath.parents[1].name
    project_name = repo_name.split("_project")[0]
    repo_parent = filepath.parents[2]

    # Add the site-packages of the chosen virtualenv to work with
    site.addsitedir(str(virtualenv_home.joinpath(repo_name, "Lib", "site-packages")))

    # Add the app's directory to the PYTHONPATH
    sys.path.append(str(filepath.parents[1]))
    sys.path.append(str(filepath.parents[1].joinpath(project_name)))

    # Add environment variables
    try:
        if repo_parent == project_home:
            env_path = str(Path(project_home, repo_name, '.env').resolve())
        else:
            env_path = str(Path(project_home, repo_parent.name, repo_name, '.env').resolve())
        with open(env_path) as f:
            content = f.read()
    except IOError:
        content = ''

    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))
            os.environ.setdefault(key, val)

    # Activate the virtual env
    # Check for Windows directory, otherwise use Linux directory
    activate_env = virtualenv_home.joinpath(repo_name, "Scripts", "activate_this.py")

    if not activate_env.exists():
        activate_env = virtualenv_home.joinpath(repo_name, "bin", "activate_this.py")

    exec(compile(open(str(activate_env)).read(), str(activate_env), 'exec'), dict(__file__=str(activate_env)))

activate_env()

import django
from django.core.handlers.wsgi import WSGIHandler
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
django.setup()

# Send any wsgi errors to Sentry
application = Sentry(WSGIHandler())
