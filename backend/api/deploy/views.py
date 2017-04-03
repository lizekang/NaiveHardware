import json
import string
import random
import httplib2

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
        headers = {'Content-type': "application/json"}
        conn = httplib2.Http()
        url = "http://" + server_ip + "/task"
        resp, content = conn.request(url, 'POST',
                                     headers=headers,
                                     body=json.dumps([task_list, {"device_ip": device_ip}]))
        if resp['status'] == '200':
            self.finish(json.dumps({"errno": True, "data": task_list}))
        else:
            self.finish(json.dumps({"errno": False, "data": []}))

    @base.db_success_or_pass
    def set_run(self, project):
        project.is_run = True

    @base.db_success_or_pass
    def get_task_list(self, projects):
        task_list = list()
        for project in projects:
            if project.is_run is True:
                sensors = list()
                effectors = list()
                for sensor in project.sensors:
                    sensors.append(sensor.id)
                for effector in project.effectors:
                    effectors.append(effector.id)
                task = {
                    'effectors': effectors,
                    'sensors': sensors
                }
                task_list.append(task)
        return task_list
