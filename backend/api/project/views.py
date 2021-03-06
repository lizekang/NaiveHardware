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
    "ProjectHandler",
    "ProjectsHandler",
    "ProjectsCountHandler",
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


class UserProjectsHandler(base.APIBaseHandler):
    """
    URL: /user/projects
    Allowed methods: GET POST
    """
    @base.authenticated()
    def get(self):
        query = self.current_user.projects
        self.finish_objects(forms.ProjectsForm,
                            query=query)

    @base.authenticated()
    def post(self):
        form = forms.ProjectForm(self.json_args,
                                 locale_code=self.locale.code)
        if form.validate():
            project = self.create_project(form)
            if project:
                self.finish(json.dumps(
                    project.format_detail(),
                    cls=util.AdvEncoder
                ))
            else:
                name = "project_name"
                self.check_for_same(name)
        else:
            self.validation_error(form)

    @base.db_success_or_pass
    def create_project(self, form):
        count = 0
        for project in self.current_user.projects:
            if project.project_name == form.project_name.data:
                count += 1
        if count != 0:
            return False
        project = models.Project(projectname=form.project_name.data,
                                 description=form.description.data,
                                 authority=form.authority.data)
        project.user = self.current_user
        self.session.add(project)
        return project

    @staticmethod
    def split_json_args(json_args):
        project_json = {
            "project_name": json_args['project_name'],
            "description": json_args['description'],
            "authority": json_args['authority'],
            "change_time": util.get_utc_time(),
            'uid': json_args['uid']
        }
        sensor_json = json_args['sensors']
        effector_json = json_args['effector']



class UserProjectHandler(base.APIBaseHandler):
    """
    URL: /user/project/(?P<uuid>[0-9a-fA-F]{32})
    Allowed methods: GET PATCH DELETE
    """
    @base.authenticated()
    def get(self, uuid):
        self.finish_object(models.Project,
                           uuid,
                           permission_check=self.project_user_check)

    @base.authenticated()
    def patch(self, uuid):
        project = self.get_or_404(self.current_user.projects,
                                  uid=uuid)
        form = forms.ProjectForm(self.json_args,
                                 locale_code=self.locale.code)
        if form.validate():
            project = self.edit_project(project, form)
            if project:
                self.finish(json.dumps(
                    project.format_detail(),
                    cls=util.AdvEncoder
                ))
            else:
                name = "project_name"
                self.check_for_same(name)
        else:
            self.validation_error(form)

    @base.authenticated()
    def delete(self, uuid):
        project = self.get_or_404(self.current_user.projects,
                                  uid=uuid)
        self.delete_project(project)
        self.set_status(204)
        self.finish()

    @base.db_success_or_500
    def edit_project(self, project, form):
        count = 0
        for project in self.current_user.projects:
            if project.project_name == form.project_name.data:
                count += 1
        if count != 0:
            return False
        attr_list = ['project_name', 'description', 'authority']
        self.apply_edit(project, form, attr_list)

        return project

    @base.db_success_or_500
    def delete_project(self, project):
        self.session.delete(project)

    @staticmethod
    def project_user_check(project, user):
        return True \
            if project in user.projects \
            else False


class ProjectsCountHandler(base.APIBaseHandler):
    """
    URL: /user/(?P<uuid>[0-9a-fA-F]{32})/project/count
    Allowed methods: GET
    """
    # TODO: here is a bug
    def get(self, uuid):
        user = self.get_or_404(models.User.query,
                               uid=uuid)
        self.finish_objects_count(query=user.projects)


