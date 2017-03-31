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
    "EffectorAddHandler",
    "EffectorDeleteHandler"
]


class EffectorAddHandler(base.APIBaseHandler):
    """
    URL: /effector/add
    Allowed methods: POST
    """
    def post(self):
        """
        create a new effector
        """
