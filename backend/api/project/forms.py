from wtforms.fields import StringField

from wtforms.validators import (
    StopValidation,
    ValidationError,
    InputRequired,
    EqualTo,
    Email,
    Regexp,
    Length,
    Optional,
)

from wtforms.fields import (
    StringField,
    TextAreaField,
    SelectField,
    BooleanField,
    Field,
)

import models
from form import Form
import util

from .. import baseForms
from .. import baseValidators


class ProjectForm(Form):
    project_name = StringField('project_name')
    description = TextAreaField('description')
    authority = BooleanField('authority')
    # change_time = StringField('change_time')


class ProjectsForm(Form, baseForms.SliceMixin):
    sortby = SelectField('sortby', default="create_time", choices=[
        ("create_time", "create_time"),
        ("likes", "likes"),
    ])
    order = SelectField('order', default="asc", choices=[
        ("asc", "asc"),
        ("desc", "desc"),
    ])


class SensorAndEffectorForm(Form):
    id = StringField('id')
    type = StringField('type')


class FunctionForm(Form):
    function_name = StringField("function_name")
    args = StringField("args")
