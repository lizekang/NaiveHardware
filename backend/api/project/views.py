import json
import string
import random

import tornado.httpclient
from tornado import gen
from tornado.httpclient import (
    AsyncHTTPClient,
    HTTPError,
)
from sqlalchemy import func

from ... import util
from ... import models
from .. import base
from . import forms


__all__ = [
    "ProjectHandler",
    "ProjectsHandler",
    "ProjectLikesHandler",
    "ProjectCountHandler",
    "UserProjectHandler",
    "UserProjectsHandler",
]


class ProjectHandler(base.APIBaseHandler):
    """
    URL: /project/(?P<uuid>[0-9a-fA-F]{32})
    Allowed methods: GET
    """
    def get(self, uuid):
        self.finish_object(models.Project,
                           uuid)


class ProjectsHandler(base.APIBaseHandler):
    """
    URL: /community/projects
    Allowed methods: POST
    """


