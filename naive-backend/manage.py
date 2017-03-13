#!/bin/bash/env python
# -*- utf-8 -*-
import pytest
from flask_script import Manager

manager = Manager(app)
@manager.command
def runserver():
    """
    Overrides default runserver()
    """
    app.run(host='127.0.0.1', port=8080, debug=True)

@manager.command
def test():
    """
    do unit test using pytest
    """
    errno = pytest.main(args=['-v', './test'])
    return errno

@manager.command
def create_db():
    """
    TODOS:
    """
