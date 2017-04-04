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
    "UserProjectsHandler",
    "UserProjectHandler"
]


class UserProjectsHandler(base.APIBaseHandler):
    """
    URL: /user/projects
    ALlowed methods: GET
    """
    @base.authenticated()
    def get(self):
        self.finish(json.dumps(
            self.current_user.format_detail(),
            cls=util.AdvEncoder
            ))


class UserProjectHandler(base.APIBaseHandler):
    """
    URL: /user/project
    Allowed methods: POST PATCH DELETE
    """

    @base.db_success_or_pass
    def create_project(self, project_json):
        project_form = forms.ProjectForm(project_json,
                                         locale_code=self.locale.code)
        if project_form.validate():
            project = models.Project(projectname=project_form.project_name.data,
                                     description=project_form.description.data,
                                     authority=project_form.authority.data)
            project.user = self.current_user
            self.session.add(project)
            return project
        else:
            self.validation_error(project_form)

    @base.db_success_or_pass
    def create_sensor(self, sensor_json, project):
        id = sensor_json['id']
        type = sensor_json['type']
        sensor_json['id'] = [id]
        sensor_json['type'] = [type]
        sensor_form = forms.SensorAndEffectorForm(sensor_json,
                                                  locale_code=self.locale.code)

        if sensor_form.validate():
            sensor = models.Sensor(id=sensor_form.id.data,
                                   type=sensor_form.type.data)
            sensor.user = self.current_user
            sensor.project = project
            self.session.add(sensor)
            return sensor
        else:
            self.validation_error(sensor_form)

    @base.db_success_or_pass
    def create_effector(self, effector_json, project):
        id = effector_json['id']
        type = effector_json['type']
        effector_json['id'] = [id]
        effector_json['type'] = [type]
        effector_form = forms.SensorAndEffectorForm(effector_json,
                                                    locale_code=self.locale.code)

        if effector_form.validate():
            effector = models.Effector(id=effector_form.id.data,
                                       type=effector_form.type.data)
            effector.user = self.current_user
            effector.project = project
            self.session.add(effector)
            return effector
        else:
            self.validation_error(effector_form)

    @base.db_success_or_pass
    def create_sensor_function(self, sensor_function_json, sensor):
        function_name = sensor_function_json['function_name']
        args = sensor_function_json['args']
        sensor_function_json['function_name'] = [function_name]
        sensor_function_json['args'] = [args]
        form = forms.FunctionForm(sensor_function_json,
                                  locale_code=self.locale.code)
        if form.validate():
            function = models.SensorAndEffectorFunction(function_name=form.function_name.data,
                                                        args=form.args.data)
            function.sensor = sensor
            self.session.add(function)
            return function
        else:
            self.validation_error(form)

    @base.db_success_or_pass
    def create_effector_function(self, effector_function_json, effector):
        function_name = effector_function_json['function_name']
        args = effector_function_json['args']
        effector_function_json['function_name'] = [function_name]
        effector_function_json['args'] = [args]
        form = forms.FunctionForm(effector_function_json,
                                  locale_code=self.locale.code)
        if form.validate():
            function = models.SensorAndEffectorFunction(function_name=form.function_name.data,
                                                        args=form.args.data)
            function.effector = effector
            self.session.add(function)
            return function
        else:
            self.validation_error(form)

    @base.db_success_or_pass
    def edit_project(self, project_json):
        project = self.get_or_404(self.current_user.projects,
                                  uid=project_json['uid'][0])
        form = forms.ProjectForm(project_json,
                                 locale_code=self.locale.code)
        if form.validate():
            attr_list = ['project_name', 'description', 'authority']
            self.apply_edit(project, form, attr_list)
            return project
        else:
            self.validation_error(form)

    @base.db_success_or_pass
    def edit_sensor(self, sensor_json, project):
        id = sensor_json['id']
        type = sensor_json['type']
        sensor_json['id'] = [id]
        sensor_json['type'] = [type]
        sensor = self.get_or_404(project.sensors,
                                 uid=sensor_json['uid'])
        form = forms.SensorAndEffectorForm(sensor_json,
                                           locale_code=self.locale.code)
        if form.validate():
            attr_list = ['id', 'type']
            self.apply_edit(sensor, form, attr_list)
            return sensor
        else:
            self.validation_error(form)

    @base.db_success_or_pass
    def edit_effector(self, effector_json, project):
        id = effector_json['id']
        type = effector_json['type']
        effector_json['id'] = [id]
        effector_json['type'] = [type]
        effector = self.get_or_404(project.effectors,
                                   uid=effector_json['uid'])
        form = forms.SensorAndEffectorForm(effector_json,
                                           locale_code=self.locale.code)
        if form.validate():
            attr_list = ['id', 'type']
            self.apply_edit(effector, form, attr_list)
            return effector
        else:
            self.validation_error(form)

    @base.db_success_or_pass
    def edit_function(self, function_json, obj):
        function_name = function_json['function_name']
        args = function_json['args']
        function_json['function_name'] = [function_name]
        function_json['args'] = [args]
        function = self.get_or_404(obj.functions,
                                   uid=function_json['uid'])
        form = forms.FunctionForm(function_json,
                                  locale_code=self.locale.code)
        if form.validate():
            attr_list = ['function_name', 'args']
            self.apply_edit(function, form, attr_list)
            return function
        else:
            self.validation_error(form)

    @base.db_success_or_pass
    def delete_obj(self, obj):
        self.session.delete(obj)

    @staticmethod
    def split_json_args(json_args):
        project_json = {
            "project_name": json_args['project_name'],
            "description": json_args['description'],
            "authority": json_args['authority'],
            # "change_time": util.get_utc_time(),
            'uid': ""
        }
        if 'uid' in json_args:
            project_json['uid'] = json_args['uid']
        sensor_json = {
            'sensors': json_args['sensors'],
            'project_uid': ""
        }
        if 'uid' in json_args:
            sensor_json['project_uid'] = json_args['uid']
        effector_json = {
            'effectors': json_args['effectors'],
            'project_uid': ""
        }
        if 'uid' in json_args:
            effector_json['project_uid'] = json_args['uid']
        # sensor_functions_json = {
        #     'functions': json_args['sensors']['functions'],
        #     'sensor_uid': "",
        # }
        # if 'uid' in json_args['sensors']:
        #     sensor_functions_json['sensor_uid'] = json_args['sensors']['uid']
        # effector_functions_json = {
        #     'functions': json_args['effectors']['functions'],
        #     'effector_uid': ""
        # }
        # if 'uid' in json_args['effectors']:
        #     effector_functions_json['effector_uid'] = json_args['effectors']['uid']
        return_json = {
            "project_json": project_json,
            "sensor_json": sensor_json,
            "effector_json": effector_json
        }
        return return_json

    @base.authenticated()
    def patch(self):
        format_json = self.split_json_args(self.json_args)
        project = self.edit_project(format_json['project_json'])
        project.change_time = util.get_utc_time()
        response = {
            'uid': project.uid.hex,
            'project_name': project.project_name,
            'description': project.description,
            'authority': project.authority,
            'is_run': project.is_run,
            'change_time': project.change_time,
            'create_time': project.create_time
        }
        sensors = []
        for sensor_json in format_json['sensor_json']['sensors'][0]:
            sensor = self.edit_sensor(sensor_json, project)
            functions = []
            for sensor_function_json in sensor_json['functions']:
                function = self.edit_function(sensor_function_json, sensor)
                functions.append(function.format_detail())
            sensors.append(sensor.format_detail())
        effectors = []
        for effector_json in format_json['effector_json']['effectors'][0]:
            effector = self.edit_effector(effector_json, project)
            functions = []
            for effector_function_json in effector_json['functions']:
                function = self.edit_function(effector_function_json, effector)
                functions.append(function.format_detail())
            effectors.append(effector.format_detail())
        response['sensors'] = sensors
        response['effectors'] = effectors
        self.finish(json.dumps(
            response,
            cls=util.AdvEncoder
        ))

    @base.authenticated()
    def post(self):
        format_json = self.split_json_args(self.json_args)
        project = self.create_project(format_json['project_json'])
        project.change_time = util.get_utc_time()
        response = {
            'uid': project.uid.hex,
            'project_name': project.project_name,
            'description': project.description,
            'authority': project.authority,
            'is_run': project.is_run,
            'change_time': project.change_time,
            'create_time': project.create_time
        }
        sensors = []
        for sensor_json in format_json['sensor_json']['sensors'][0]:
            sensor = self.create_sensor(sensor_json, project)
            functions = []
            for sensor_function_json in sensor_json['functions']:
                function = self.create_sensor_function(sensor_function_json, sensor)
                functions.append(function.format_detail())
            sensors.append(sensor.format_detail())
        effectors = []
        for effector_json in format_json['effector_json']['effectors'][0]:
            effector = self.create_effector(effector_json, project)
            functions = []
            for effector_function_json in effector_json['functions']:
                function = self.create_effector_function(effector_function_json, effector)
                functions.append(function.format_detail())
            effectors.append(effector.format_detail())
        response['sensors'] = sensors
        response['effectors'] = effectors
        self.finish(json.dumps(
            response,
            cls=util.AdvEncoder
        ))

    @base.authenticated()
    def delete(self):
        uuid = self.json_args['uid'][0]
        project = self.get_or_404(self.current_user.projects,
                                  uid=uuid)
        for sensor in project.sensors:
            for function in sensor.functions:
                self.delete_obj(function)
            self.delete_obj(sensor)
        for effector in project.effectors:
            for function in effector.functions:
                self.delete_obj(function)
            self.delete_obj(effector)
        self.delete_obj(project)
        self.set_status(204)
        self.finish()



