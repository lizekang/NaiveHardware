import json
import string
import random
import httplib2

from urllib.request import urlopen
from urllib.error import HTTPError

import tornado.httpclient
from tornado import gen
from tornado.httpclient import (
    AsyncHTTPClient
)
from sqlalchemy import func

import util
import models
from .. import base

__all__ = [
    "DeployHandler"
]


class DeployHandler(base.APIBaseHandler):
    """
    URL: /user/project/(?P<uuid>[0-9a-fA-F]{32})/deploy
    Allowed methods: POST
    """
    @base.authenticated()
    def post(self, uuid):
        server_ip = self.json_args['server_ip'][0]
        device_ip = self.json_args['device_ip'][0]
        project = self.get_or_404(self.current_user.projects,
                                  uid=uuid)
        self.set_run(project)
        task_list = self.get_task_list(self.current_user.projects)
        driver_obj = self.get_driver(self.current_user.projects)
        app_json_obj = self.generate_config(self.get_config()).generate_app_json()
        package_json_obj = self.generate_config(self.get_config()).generate_package_json()
        user_obj = self.generate_user_obj()
        headers = {'Content-type': "application/json"}
        conn = httplib2.Http()
        server_url = "http://" + server_ip + "/task"
        resp, content = conn.request(server_url, 'POST',
                                     headers=headers,
                                     body=json.dumps([{"device_ip": device_ip},
                                                      task_list,
                                                      driver_obj,
                                                      app_json_obj,
                                                      package_json_obj,
                                                      user_obj]))
        if resp['status'] == '200':
            self.finish(json.dumps({"errno": True, "data": task_list}))
        else:
            self.finish(json.dumps({"errno": False, "data": []}))

    @base.db_success_or_pass
    def set_run(self, project):
        project.is_run = True

    @staticmethod
    def get_task_list(projects):
        task_list = list()
        for project in projects:
            if project.is_run is True:
                sensors = list()
                effectors = list()
                for sensor in project.sensors:
                    if sensor.functions is not None:
                        for function in sensor.functions:
                            sensors.append({"id": sensor.id.encode().decode(), 'args': function.args.encode().decode()})
                for effector in project.effectors:
                    if effector.functions is not None:
                        for function in effector.functions:
                            effectors.append({"id": effector.id.encode().decode(), 'args': function.args.encode().decode()})
                task = {
                    'effectors': effectors,
                    'sensors': sensors,
                    'id': project.project_name.encode().decode()
                }
                task_list.append(task)
        return task_list

    @staticmethod
    def get_driver(projects):
        def key1(x):
            if x['functionlist'][0]['function'] == 'on':
                return 2
            if x['functionlist'][0]['function'] == 'time':
                return 1
            else:
                return 0
        driver = {}
        sensors = list()
        effectors = list()
        for project in projects:
            if project.is_run is True:
                for sensor in project.sensors:
                    functions = list()
                    for function in sensor.functions:
                        functions.append({'args': function.args,
                                          'function': function.function_name})
                    sensors.append({
                        'functionlist': functions,
                        'id': sensor.id
                    })
                for effector in project.effectors:
                    functions = list()
                    for function in effector.functions:
                        functions.append({'args': function.args,
                                          'function': function.function_name})
                    effectors.append({
                        'functionlist': functions,
                        'id': effector.id
                    })
        driver['effectors'] = effectors
        driver['sensors'] = sensors
        driver['sensors'] = sorted(driver['sensors'], key=key1, reverse=True)
        return driver

    @base.db_success_or_pass
    def get_config(self):
        objects = list()
        for sensor in self.current_user.sensors:
            a_object = {
                "id": sensor.id,
                "driver": sensor.type
            }
            objects.append(a_object)
        for effector in self.current_user.effectors:
            a_object = {
                "id": effector.id,
                "driver": effector.type
            }
            objects.append(a_object)
        return objects

    @staticmethod
    def generate_config(objects):
        obj = RuffJson(json.dumps(objects))
        return obj

    @base.db_success_or_pass
    def generate_user_obj(self):
        user_obj = {
            "username": self.current_user.username,
            "password": self.current_user.password
        }
        return user_obj


class RuffJson(object):
    def __init__(self, json):
        # when init you should pass the command.json
        self.__command_json = json
        self.path = '/home/lzk/ruff/cc2531/ruff_modules/'

    def set_path(self, path):
        self.path = path

    def get_command_json(self):
        # get the command json
        return self.__command_json

    def generate_app_json(self):  # generate the app.json
        command_list = json.loads(self.__command_json)
        app_json_list = []
        for task in command_list:
            print(task['driver'])
            try:
                print('https://raw.githubusercontent.com/ruff-drivers/'+task['driver']+'/master/driver.json')
                html = urlopen('https://raw.githubusercontent.com/ruff-drivers/'+task['driver']+'/master/driver.json')
                json_str = html.read().decode('utf-8')
                json_ob = json.loads(json_str)
            except HTTPError as e:
                print(e)

            for i in list(json_ob.keys()):
                if i == 'models':
                    task[i] = (json_ob[i][0] if len(json_ob[i]) else [])
                else:
                    task[i] = json_ob[i]
            app_json_list.append(task)
        self.__app_json = json.dumps(dict(devices=app_json_list))
        return self.__app_json

    def generate_package_json(self): # generate the package.json
        command_list = json.loads(self.__command_json)
        k = {
            "name": "app",
            "version": "0.1.0",
            "description ": "a test",
            "author": "ZekangLi",
            "main": "src/index.js",
            "ruff": {
                "boards": {
                    " ruff-mbd-v1 ": "^4.2.2",
                    " *": "*"
                    },
                "dependencies": {}
            }
        }
        for i in [task['driver'] for task in command_list]:
            with open(self.path+'%s/package.json'%i, 'r+') as fp:
                package = json.loads(fp.read())
                k['ruff']["dependencies"][i] = "^" + package['version']
        self.__package_json = json.dumps(k)
        return self.__package_json
