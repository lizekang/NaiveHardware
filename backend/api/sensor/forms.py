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
from ... import util

from .. import baseForms
from .. import baseValidators


class SensorForm(Form):
    id = StringField('id')
    type = SelectField('type')
    function = SelectField('function')
    arguments = StringField('arguments')
