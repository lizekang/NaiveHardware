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
    "UserEffectorHandler",
    "ProjectEffectorHandler",
    "EffectorHandler"
]


class UserEffectorHandler(base.APIBaseHandler):
    """
    URL: /user/effectors
    Allowed methods: GET POST
    """
    @base.authenticated()
    def get(self):
        """
        get effectors under a user, using when send data to ruff
        """
        query = self.current_user.effectors
        self.finish_objects(forms.EffectorsForm,
                            query=query)


class ProjectEffectorHandler(base.APIBaseHandler):
    """
    URL: /user/project/(?P<uuid>[0-9a-fA-F]{32})/effectors
    Allowed methods: GET POST
    """
    @base.authenticated()
    def get(self, uuid):
        """
        get effectors under a project
        """
        project = self.get_or_404(self.current_user.projects,
                                  uid=uuid)
        query = project.effectors
        self.finish_objects(forms.EffectorsForm,
                            query=query)

    @base.authenticated()
    def post(self, uuid):
        form = forms.EffectorForm(self.json_args,
                                  locale_code=self.locale.code)
        if form.validate():
            effector = self.create_effector(form)
            if effector:
                self.finish(json.dumps(
                    effector.format_detail(),
                    cls=util.AdvEncoder
                ))
            else:
                name = "id"
                self.check_for_same(name)
        else:
            self.validation_error(form)

    @base.db_success_or_pass
    def create_effector(self, form, uuid):
        count = 0
        for effector in self.current_user.effectors:
            if effector.id == form.id.data:
                count += 1
        if count != 0:
            return False
        effector = models.Effector(id=form.id.data,
                                   type=form.type.data)
        effector.user = self.current_user
        effector.project = self.get_or_404(self.current_user.projects,
                                           uid=uuid)
        self.session.add(effector)
        return effector


class EffectorHandler(base.APIBaseHandler):
    """
    URL: /user/project/(?P<project_uuid>[0-9a-fA-F]{32})/effector/(?P<effector_uuid>[0-9a-fA-F]{32})
    Allowed methods: GET PATCH DELETE
    """
    @base.authenticated()
    def get(self, project_uuid, effector_uuid):
        project = self.get_or_404(self.current_user.projects,
                                  uid=project_uuid)
        effector = self.get_or_404(project.effectors,
                                   uid=effector_uuid)
        self.finish(json.dumps(
            effector.format_detail(),
            cls=util.AdvEncoder
        ))

    @base.authenticated()
    def patch(self, project_uuid, effector_uuid):
        project = self.get_or_404(self.current_user.projects,
                                  uid=project_uuid)
        effector = self.get_or_404(project.effectors,
                                   uid=effector_uuid)
        form = forms.EffectorForm(self.json_args,
                                  locale_code=self.locale.code)
        if form.validate():
            effector = self.edit_effector(effector, form)
            if effector:
                self.finish(json.dumps(
                    effector.format_detail(),
                    cls=util.AdvEncoder
                ))
            else:
                name = "id"
                self.check_for_same(name)
        else:
            self.validation_error(form)

    @base.authenticated()
    def delete(self, project_uuid, effector_uuid):
        project = self.get_or_404(self.current_user.projects,
                                  uid=project_uuid)
        effector = self.get_or_404(project.effectors,
                                   uid=effector_uuid)
        self.delete_effector(effector)
        self.set_status(204)
        self.finish()

    @base.db_success_or_500
    def edit_effector(self, effector, form):
        count = 0
        for effector in self.current_user.effectors:
            if effector.id == form.id.data:
                count += 1
        if count != 0:
            return False
        attr_list = ['id', 'type']
        self.apply_edit(effector, form, attr_list)
        return effector

    @base.db_success_or_500
    def delete_effector(self, effector):
        self.session.delete(effector)
