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
    "FunctionEffectorHandler",
    "SensorFunctionHandler",
    "EffectorFunctionHandler"
]


class FunctionSensorHandler(base.APIBaseHandler):
    """
    URL: /user/project/(?P<project_uuid>[0-9a-fA-F]{32})/sensor/(?P<sensor_uuid>[0-9a-fA-F]{32})/function
    Allowed methods: POST GET
    """
    @base.authenticated()
    def get(self, project_uuid, sensor_uuid):
        project = self.get_or_404(self.current_user.projects,
                                  uid=project_uuid)
        sensor = self.get_or_404(project.sensors,
                                 uid=sensor_uuid)
        query = sensor.functions
        self.finish_objects(forms.FunctionForm,
                            query=query)

    @base.authenticated()
    def post(self, project_uuid, sensor_uuid):
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
        sensor = self.get_or_404(current_project.sensors,
                                 uid=sensor_uuid)
        function.sensor = sensor
        self.session.add(function)
        return function


class FunctionEffectorHandler(base.APIBaseHandler):
    """
    URL: /user/project/(?P<project_uuid>[0-9a-fA-F]{32})/effector/(?P<effector_uuid>[0-9a-fA-F]{32})/function
    Allowed method: POST GET
    """

    @base.authenticated()
    def get(self, project_uuid, effector_uuid):
        project = self.get_or_404(self.current_user.projects,
                                  uid=project_uuid)
        effector = self.get_or_404(project.sensors,
                                   uid=effector_uuid)
        query = effector.functions
        self.finish_objects(forms.FunctionForm,
                            query=query)

    @base.authenticated()
    def post(self, project_uuid, effector_uuid):
        form = forms.FunctionForm(self.json_args,
                                  locale_code=self.locale.code)
        if form.validate():
            function = self.create_function(form,
                                            project_uuid,
                                            effector_uuid)
            self.finish(json.dumps(
                function.format_detail(),
                cls=util.AdvEncoder
            ))
        else:
            self.validation_error(form)

    @base.db_success_or_pass
    def create_function(self, form, project_uuid, effector_uuid):
        function = models.SensorAndEffectorFunction(function_name=form.function_name.data,
                                                    args=form.args.data)
        current_project = self.get_or_404(self.current_user.projects,
                                          uid=project_uuid)
        effector = self.get_or_404(current_project.sensors,
                                   uid=effector_uuid)
        function.effector = effector
        self.session.add(function)
        return function


class SensorFunctionHandler(base.APIBaseHandler):
    """
    URL: /user/project/<project_uuid>/sensor/<sensor_uuid>/function/<function_uuid>
    Allowed methods: GET PATCH DELETE
    """
    @base.authenticated()
    def get(self, project_uuid, sensor_uuid, function_uuid):
        project = self.get_or_404(self.current_user.projects,
                                  uid=project_uuid)
        sensor = self.get_or_404(project.sensors,
                                 uid=sensor_uuid)
        function = self.get_or_404(sensor.functions,
                                   uid=function_uuid)
        self.finish(json.dumps(
            function.format_detail(),
            cls=util.AdvEncoder
        ))

    @base.authenticated()
    def patch(self, project_uuid, sensor_uuid, function_uuid):
        project = self.get_or_404(self.current_user.projects,
                                  uid=project_uuid)
        sensor = self.get_or_404(project.sensors,
                                 uid=sensor_uuid)
        function = self.get_or_404(sensor.functions,
                                   uid=function_uuid)
        form = forms.FunctionForm(self.json_args,
                                  locale_code=self.locale.code)
        if form.validate():
            function = self.edit_function(function, form)
            self.finish(json.dumps(
                function.format_detail(),
                cls=util.AdvEncoder
            ))
        else:
            self.validation_error(form)

    @base.db_success_or_500
    def edit_function(self, function, form):
        attr_list = ['function_name', 'args']
        self.apply_edit(function, form, attr_list)
        return function

    @base.db_success_or_500
    def delete_function(self, function):
        self.session.delete(function)


class EffectorFunctionHandler(base.APIBaseHandler):
    """
        URL: /user/project/<project_uuid>/effector/<effector_uuid>/function/<function_uuid>
        Allowed methods: GET PATCH DELETE
        """

    @base.authenticated()
    def get(self, project_uuid, effector_uuid, function_uuid):
        project = self.get_or_404(self.current_user.projects,
                                  uid=project_uuid)
        effector = self.get_or_404(project.sensors,
                                   uid=effector_uuid)
        function = self.get_or_404(effector.functions,
                                   uid=function_uuid)
        self.finish(json.dumps(
            function.format_detail(),
            cls=util.AdvEncoder
        ))

    @base.authenticated()
    def patch(self, project_uuid, effector_uuid, function_uuid):
        project = self.get_or_404(self.current_user.projects,
                                  uid=project_uuid)
        effector = self.get_or_404(project.sensors,
                                   uid=effector_uuid)
        function = self.get_or_404(effector.functions,
                                   uid=function_uuid)
        form = forms.FunctionForm(self.json_args,
                                  locale_code=self.locale.code)
        if form.validate():
            function = self.edit_function(function, form)
            self.finish(json.dumps(
                function.format_detail(),
                cls=util.AdvEncoder
            ))
        else:
            self.validation_error(form)

    @base.db_success_or_500
    def edit_function(self, function, form):
        attr_list = ['function_name', 'args']
        self.apply_edit(function, form, attr_list)
        return function

    @base.db_success_or_500
    def delete_function(self, function):
        self.session.delete(function)

