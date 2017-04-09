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
    "LoginHandler",
    "RegisterHandler"
]


class RegisterHandler(base.APIBaseHandler):
    """
    URL: /register
    Allowed methods: POST
    """
    def post(self):
        """
        create a new user
        """
        form = forms.RegisterForm(self.json_args,
                                  locale_code=self.locale.code)
        if form.validate():
            user = self.create_user(form)

            self.set_status(201)
            self.finish(json.dumps({
                'auth': self.create_signed_value('uid', user.uid.hex).decode('utf-8'),
            }))
        else:
            self.validation_error(form)

    @base.db_success_or_pass
    def create_user(self, form):
        number = self.session.query(func.max(models.User.number)).first()[0] + 1
        print(form.username.data)
        user = models.User(username=form.username.data,
                           number=number,
                           nick_name=form.nick_name.data)
        user.set_password(form.password.data)
        self.session.add(user)

        return user


class LoginHandler(base.APIBaseHandler):
    """
    URL: /login
    Allowed methods: 'POST'
    """
    def post(self):
        """
        Get auth token
        """
        form = forms.LoginForm(self.json_args,
                               locale_code=self.locale.code)
        if form.validate():
            user = form.kwargs['user']
            self.finish(json.dumps({
                'auth': self.create_signed_value('uid', user.uid.hex).decode('utf-8'),
            }))
        else:
            self.validation_error(form)

