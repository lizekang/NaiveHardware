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

import util
import models
from .. import base
from . import forms

__all__ = [
    "FunctionSensorHandler",
    "FunctionEffectorHandler"
]


class FunctionSensorHandler(base.APIBaseHandler):
    """
    URL: /user/project/(?P<project_uuid>[0-9a-fA-F]{32})/sensor/(?P<sensor_uuid>[0-9a-fA-F]{32})/function
    Allowed methods: POST GET
    """
    @base.authenticated()
    def get(self, project_uuid):
        project = self.get_or_404(self.current_user.projects,
                                  uid=project_uuid)
        # TODO: many todos

    @base.authenticated()
    def post(self, project_uuid, sensor_uuid):
        # TODO: how to create more functions one time
        form = forms.FunctionForm(self.json_args,
                                  locale_code=self.locale.code)
        if form.validate():
            function = self.create_function(form,
                                            project_uuid,
                                            sensor_uuid)
            self.finish(json.dumps(
                function.format_detail(),
                cls=util.AdvEncoder
            ))
        else:
            self.validation_error(form)

    @base.db_success_or_pass
    def create_function(self, form, project_uuid, sensor_uuid):
        function = models.SensorAndEffectorFunction(function_name=form.function_name.data,
                                                    args=form.args.data)
        current_project = self.get_or_404(self.current_user.projects,
                                          uid=project_uuid)
        sensor = self.get_or_404(current_project.sensor,
                                 uid=sensor_uuid)
        function.sensor = sensor
        self.session.add(function)
        return function


class FunctionEffectorHandler(base.APIBaseHandler):
    """
    URL: /user/effector/(?P<uuid>[0-9a-fA-f]{32})/function
    Allowed method: POST
    """

