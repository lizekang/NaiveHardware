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

from .. import baseForms
from .. import baseValidators


class ProjectForm(Form):
    name = StringField('project_name')
    description = TextAreaField('description')
    authority = BooleanField('authority')


class ProjectsForm(Form):
    sortby = SelectField('sortby', default="likes", choices=[
        ("create_time", "create_time"),
        ("likes", "likes"),
    ])
