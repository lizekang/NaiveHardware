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
    "SensorAddHandler",
    "SensorDeleteHandler",
    "SensorHandler"
]


class SensorHandler(base.APIBaseHandler):
    """
    URL: /user/sensors
    """