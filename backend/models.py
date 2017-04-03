import uuid
import json

from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.schema import (
    UniqueConstraint,
    PrimaryKeyConstraint,
    Index,
)

from sqlalchemy import (
    Table,
    Column,
    BigInteger,
    SmallInteger,
    Integer,
    Unicode,
    UnicodeText,
    Boolean,
    DateTime,
    ForeignKey,
    JSON
)

from sqlalchemy.orm import (
    relationship,
    backref,
)

from database import Base
import util

IMAGE_HOST = "http://yuepai01-1251817761.file.myqcloud.com/image/"


class GUID(TypeDecorator):
    """
    Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID(as_uuid=False))
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(str(value))


class User(Base):
    __tablename__ = 'user'
    uid = Column(GUID(),
                 default=uuid.uuid4,
                 primary_key=True)
    number = Column(Integer,
                    autoincrement=True,
                    nullable=False,
                    unique=True)
    password = Column(Unicode(100),
                      nullable=True)
    username = Column(Unicode(30),
                      nullable=False)
    projects = relationship('Project',
                            back_populates='user',
                            uselist=True,
                            lazy='dynamic')
    nick_name = Column(Unicode(50),
                       nullable=False)
    is_admin = Column(Boolean,
                      default=False)
    sensors = relationship('Sensor',
                           back_populates='user',
                           uselist=True,
                           lazy='dynamic')
    effectors = relationship('Effector',
                             back_populates='user',
                             uselist=True,
                             lazy='dynamic')

    def check_password(self, request_pwd):
        return util.check_password(request_pwd, self.password)

    def set_password(self, new_pwd):
        self.password = util.set_password(new_pwd)

    def __init__(self, username=None,
                 number=None, nick_name=None):
        self.username = username
        self.create_time = util.get_utc_time()
        self.nick_name = nick_name
        if number is None:
            self.number = User.query.count()
        else:
            self.number = number

    def format_detail(self):
        detail = {
            'uid': self.uid.hex,
            'name': self.username,
            'nick_name': self.nick_name
        }
        return detail


class Project(Base):
    __tablename__ = 'project'
    uid = Column(GUID(),
                 default=uuid.uuid4,
                 primary_key=True)
    project_name = Column(Unicode(30),
                          nullable=False)
    description = Column(UnicodeText,
                         nullable=True)
    create_time = Column(DateTime(timezone=True),
                         nullable=False)
    authority = Column(Boolean,
                       nullable=False)
    user_id = Column(GUID(),
                     ForeignKey('user.uid'))
    user = relationship('User',
                        back_populates='projects')
    likes = Column(BigInteger,
                   default=0)
    change_time = Column(DateTime(timezone=True),
                         nullable=False)
    sensors = relationship('Sensor',
                           back_populates='project',
                           uselist=True,
                           lazy='dynamic')
    effectors = relationship('Effector',
                             back_populates='project',
                             uselist=True,
                             lazy='dynamic')

    def __init__(self, projectname=None, description=None,
                 authority=None, change_time=None):
        self.project_name = projectname
        self.description = description
        self.create_time = util.get_utc_time().isoformat()
        self.authority = authority
        if not change_time:
            self.change_time = util.get_utc_time().isoformat()

    def format_detail(self, get_user=True):
        detail = {
            'uid': self.uid.hex,
            'project_name': self.project_name,
            'description': self.description,
            'create_time': self.create_time,
            'likes': self.likes,
            'authority': self.authority,
            'change_time': self.change_time
        }
        if get_user:
            detail['user'] = self.user.format_detail()

        return detail


class Sensor(Base):
    __tablename__ = 'sensor'
    uid = Column(GUID(),
                 default=uuid.uuid4,
                 primary_key=True)
    id = Column(Unicode(30),
                nullable=False)
    type = Column(Unicode(50),
                  nullable=False)
    functions = relationship('SensorAndEffectorFunction',
                             back_populates='sensor',
                             uselist=True,
                             lazy='dynamic')
    project_id = Column(GUID,
                        ForeignKey('project.uid'))
    project = relationship('Project', back_populates='sensors')
    user_id = Column(GUID,
                     ForeignKey('user.uid'))
    user = relationship('User', back_populates='sensors')

    def __init__(self, id=None, type=None):
        self.id = id
        self.type = type

    def format_detail(self):
        detail = {
            "uid": self.uid.hex,
            "id": self.id,
            "type": self.type,
        }
        #if self.functions:
        #    detail['functions'] = self.functions
        return detail


class Effector(Base):
    __tablename__ = 'effector'
    uid = Column(GUID,
                 default=uuid.uuid4,
                 primary_key=True)
    id = Column(Unicode(30),
                nullable=False)
    type = Column(Unicode(50),
                  nullable=False)
    functions = relationship('SensorAndEffectorFunction',
                             back_populates='effector',
                             uselist=True,
                             lazy='dynamic')
    project_id = Column(GUID,
                        ForeignKey('project.uid'))
    project = relationship('Project',
                           back_populates='effectors')
    user_id = Column(GUID,
                     ForeignKey('user.uid'))
    user = relationship('User',
                        back_populates='effectors')

    def __init__(self, id=None, type=None):
        self.id = id
        self.type = type

    def format_detail(self):
        detail = {
            "uid": self.uid,
            "id": self.id,
            "type": self.type
        }
        if self.functions is not None:
            detail['functions'] = self.functions
        return detail


class SensorAndEffectorFunction(Base):
    __tablename__ = 'function'
    uid = Column(GUID,
                 default=uuid.uuid4,
                 primary_key=True)
    function_name = Column(Unicode(50),
                           nullable=True)
    args = Column(Unicode(40),
                  nullable=True)
    sensor_id = Column(GUID,
                       ForeignKey('sensor.uid'),
                       nullable=True)
    effector_id = Column(GUID,
                         ForeignKey('effector.uid'),
                         nullable=True)
    sensor = relationship('Sensor',
                          back_populates='functions')
    effector = relationship('Effector',
                            back_populates='functions')

    def __init__(self, function_name=None, args=None):
        self.function_name = function_name
        self.args = args

    def format_detail(self):
        detail = {
            "uid": self.uid.hex,
            "function_name": self.function_name,
            "args": self.args
        }
        return detail
