import uuid
import json

from wtforms.validators import (
    ValidationError,
    StopValidation,
)
from ..import models


def objects_get(query, msg):
    def _objects_get(form, field):
        datas = list()
        for data_id in list(field.data):
            try:
                data = query.get(data_id)
                assert data is not None
                datas.append(data)
            except Exception:
                raise StopValidation(msg)
        field.data = tuple(datas)
    return _objects_get


def object_get(query, msg):
    def _object_get(form, field):
        try:
            if not field.data:
                return None
            target = query.get(field.data)
            assert target is not None
            field.data = target
        except Exception:
            raise StopValidation(msg)
    return _object_get


def object_filter_get(query, msg, **kwargs):
    def _object_filter_get(form, field):
        try:
            if not field.data:
                return None
            target = query.filter_by(id=field.data, **kwargs).first()
            assert target is not None
            field.data = target
        except Exception:
            raise StopValidation(msg)
    return _object_filter_get


def objects_filter_get(query, msg, **kwargs):
    def _objects_filter_get(form, field):
        datas = list()
        for data_id in list(field.data):
            try:
                data = query.filter_by(id=data_id, **kwargs).first()
                assert data is not None
                datas.append(data)
            except Exception:
                raise StopValidation(msg)
        field.data = tuple(datas)
    return _objects_filter_get


def image_get(form, field):
    _ = field.gettext
    return object_get(models.Image.query,
                      _('Invalid Image.'))(form, field)


def images_get(form, field):
    _ = field.gettext
    return objects_get(models.Image.query,
                       _('Invalid Image.'))(form, field)


def banner_get(form, field):
    _ = field.gettext
    return object_get(models.Banner.query,
                      _('Invalid Banner.'))(form, field)


def banners_get(form, field):
    _ = field.gettext
    return objects_get(models.Banner.query,
                       _('Invalid Banner.'))(form, field)


def user_get(form, field):
    _ = field.gettext
    return object_get(models.User.query,
                      _('Invalid User.'))(form, field)


def photographer_get(form, field):
    _ = field.gettext
    return object_filter_get(models.User.query,
                             _('Invalid Photographer.'),
                             is_admin=False)(form, field)


def photographers_get(form, field):
    _ = field.gettext
    return objects_filter_get(models.User.query,
                              _('Invalid Photographer.'),
                              is_admin=False)(form, field)


def home_photographers_get(form, field):
    _ = field.gettext
    return objects_get(models.HomePhotographer.query,
                       _('Invalid Photographer.'))(form, field)


def home_collections_get(form, field):
    _ = field.gettext
    return objects_get(models.HomeCollection.query,
                       _('Invalid Work.'))(form, field)


def styles_get(form, field):
    _ = field.gettext
    return objects_get(models.Style.query,
                       _('Invalid Style.'))(form, field)


def themes_get(form, field):
    _ = field.gettext
    return objects_get(models.Theme.query,
                       _('Invalid Theme'))(form, field)


def schools_get(form, field):
    _ = field.gettext
    return objects_get(models.School.query,
                       _('Invalid School'))(form, field)


def school_get(form, field):
    _ = field.gettext
    return object_get(models.School.query,
                       _('Invalid School'))(form, field)


def categories_get(form, field):
    _ = field.gettext
    return objects_get(models.Category.query,
                       _('Invalid Category'))(form, field)


def collection_get(form, field):
    _ = field.gettext
    return object_get(models.Collection.query,
                      _('Invalid Collection'))(form, field)


def collections_get(form, field):
    _ = field.gettext
    return objects_get(models.Collection.query,
                       _('Invalid Collection'))(form, field)


def user_collection_get(form, field):
    _ = field.gettext
    try:
        current_user = form.kwargs.get('current_user', None)
        assert current_user is not None
    except AssertionError:
        raise ValidationError(_('Invalid collection.'))

    return object_filter_get(current_user.collections,
                             _('Invalid collection.'))(form, field)


def ignore_match(kw, form, field):
    ignore = form.kwargs.get(kw, None)
    if ignore is not None \
            and ignore == field.data:
        return True

