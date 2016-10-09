from .base import *

import dj_database_url

ALLOWED_HOSTS = [
            '.herokuapp.com',
            '.dutytogodapp.org',
            '.d2gapp.com',
        ]

DEBUG = True

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)



