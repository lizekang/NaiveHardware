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
    "UserSensorHandler",
    "ProjectSensorHandler",
    "SensorHandler",
]


class UserSensorHandler(base.APIBaseHandler):
    """
    URL: /user/sensors
    Allowed methods: GET
    """
    @base.authenticated()
    def get(self):
        """
        get sensors under a user, using when send data to ruff
        """
        query = self.current_user.sensors
        self.finish_objects(forms.SensorsForm,
                            query=query)


class ProjectSensorHandler(base.APIBaseHandler):
    """
    URL: /user/project/(?P<uuid>[0-9a-fA-F]{32})/sensors
    Allowed methods: GET POST
    """
    @base.authenticated()
    def get(self, uuid):
        """
        get sensors under a project
        """
        project = self.get_or_404(self.current_user.projects,
                                  uid=uuid)
        query = project.sensors
        self.finish_objects(forms.SensorsForm,
                            query=query)

    @base.authenticated()
    def post(self, uuid):
        form = forms.SensorForm(self.json_args,
                                locale_code=self.locale.code)
        if form.validate():
            sensor = self.create_sensor(form)
            self.finish(json.dumps(
                sensor.format_detail(),
                cls=util.AdvEncoder
            ))
        else:
            self.validation_error(form)

    @base.db_success_or_pass
    def create_sensor(self, form, uuid):
        sensor = models.Sensor(id=form.id.data,
                               type=form.type.data)
        sensor.user = self.current_user
        sensor.project = self.get_or_404(self.current_user.projects,
                                         uid=uuid)
        self.session.add(sensor)
        return sensor


class SensorHandler(base.APIBaseHandler):
    """
    URL: /user/project/(?P<project_uuid>[0-9a-fA-F]{32})/sensor/(?P<sensor_uuid>[0-9a-fA-F]{32})
    Allowed methods: GET PATCH DELETE
    """
    @base.authenticated()
    def get(self, project_uuid, sensor_uuid):
        project = self.get_or_404(self.current_user.projects,
                                  uid=project_uuid)
        sensor = self.get_or_404(project.sensors,
                                 uid=sensor_uuid)
        self.finish(json.dumps(
            sensor.format_detail(),
            cls=util.AdvEncoder
        ))

    @base.authenticated()
    def patch(self, project_uuid, sensor_uuid):
        project = self.get_or_404(self.current_user.projects,
                                  uid=project_uuid)
        sensor = self.get_or_404(project.sensors,
                                 uid=sensor_uuid)
        form = forms.SensorForm(self.json_args,
                                locale_code=self.locale.code)
        if form.validate():
            sensor = self.edit_sensor(sensor, form)
            self.finish(json.dumps(
                sensor.format_detail(),
                cls=util.AdvEncoder
            ))
        else:
            self.validation_error(form)

    @base.authenticated()
    def delete(self, project_uuid, sensor_uuid):
        project = self.get_or_404(self.current_user.projects,
                                  uid=project_uuid)
        sensor = self.get_or_404(project.sensors,
                                 uid=sensor_uuid)
        self.delete_sensor(sensor)
        self.set_status(204)
        self.finish()

    @base.db_success_or_500
    def edit_sensor(self, sensor, form):
        attr_list = ['id', 'type']
        self.apply_edit(sensor, form, attr_list)
        return sensor

    @base.db_success_or_500
    def delete_sensor(self, sensor):
        self.session.delete(sensor)