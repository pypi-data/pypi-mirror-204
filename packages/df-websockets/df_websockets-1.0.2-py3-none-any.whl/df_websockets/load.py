#  Copyright (c) 2023.
#
#  This file load.py is part of cookiecutter-django.
#  Please check the LICENSE file for sharing or distribution permissions.
#


def load_celery():
    """Import Celery application unless Celery is disabled.
    Allow to automatically load tasks
    """
    from df_websockets.celery import app

    return app
