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


class EffectorForm(Form):
    id = StringField('id')
    type = StringField('type')


class EffectorsForm(Form, baseForms.SliceMixin):
    sortby = SelectField('sortby', default='id', choices=[
        ("id", "id")
    ])
    order = SelectField('order', default='asc', choices=[
        ("asc", "asc"),
        ("desc", "desc")
    ])

