from wtforms.fields import (
    StringField,
    TextAreaField,
    SelectField,
    BooleanField,
    Field,
)
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
import models

from form import Form

from .. import baseForms
from .. import baseValidators


class RegisterForm(Form):
    username = StringField('username', [
        Email(),
        InputRequired(),
    ])
    nick_name = StringField('nick_name', [
        Length(max=20),
        InputRequired(),
    ])
    password = StringField('password', [
        InputRequired(),
        Length(max=20),
    ])

    def validate_username(form, field):
        _ = field.gettext
        count = models.User.query.filter(models.User.username == field.data).count()
        if count != 0:
            raise ValidationError('This email has been used.')


class ProfileForm(Form):
    self_password = StringField('self_password')
    password = StringField('password', [
        Length(min=6),
        Optional()
    ])
    password1 = StringField('password1', [
        EqualTo('password'),
    ])

    def validate_self_password(form, field):
        current_user = form.kwargs.get('current_user', None)
        if current_user is None:
            return
        if not current_user.password:
            return
        if not form.password.data:
            return

        if not current_user.check_password(field.data):
            _ = field.gettext
            raise StopValidation(_('False password'))


class LoginForm(Form):
    """
    Used in :
        user.LoginHandler
            method=['POST']
            Get auth token
    """
    username = StringField('username', [
        InputRequired(),
        Length(max=30),
    ])
    password = StringField('password', [
        Length(max=30),
        InputRequired(),
    ])

    def validate_email(form, field):
        _ = field.gettext
        try:
            user = models.User.query \
                .filter_by(username=form.username.data) \
                .first()
            assert user.check_password(form.password.data) is True
            form.kwargs['user'] = user
        except Exception:
            raise ValidationError(_('Email or password False.'))

    validate_password = validate_email



