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
    id = Column(GUID(),
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
                            backref='user',
                            lazy='dynamic',
                            foreign_keys="[Project.user_id]")
    nick_name = Column(Unicode(50),
                       nullable=False)
    is_admin = Column(Boolean,
                      default=False)

    def check_password(self, request_pwd):
        return util.check_password(request_pwd, self.password)

    def set_password(self, new_pwd):
        self.password = util.set_password(new_pwd)

    def __init__(self, username=None,
                 number=None, nick_name=None):
        self.name = username
        self.create_time = util.get_utc_time()
        self.nick_name = nick_name
        if number is None:
            self.number = User.query.count()
        else:
            self.number = number

    def format_detail(self):
        detail = {
            'id': self.id.hex,
            'name': self.name,
            'nick_name': self.nick_name
        }

        if self.avatar:
            detail['avatar'] = self.avatar.format_detail()
        if self.school:
            detail.update(self.school.format_detail())
        if self.styles:
            for s in self.styles:
                detail.update(s.format_detail())
        if self.categories:
            for c in self.categories:
                detail.update(c.format_detail())
        if self.cover_collection:
            detail['collection'] = self.cover_collection.format_detail(get_photographer=False)
        else:
            hottest_collection = self.collections.order_by("likes desc").first()
            detail['collection'] = hottest_collection.format_detail(get_photographer=False) \
                if hottest_collection else None

        return detail


class Project(Base):
    __tablename__ = 'project'
    id = Column(GUID(),
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
    profile = Column(JSON,
                     nullable=False)
    user_id = Column(GUID(),
                     ForeignKey('user.id'))
    likes = Column(BigInteger,
                   default=0)
    change_time = Column(DateTime(timezone=True),
                         nullable=False)

    def __init__(self, projectname=None, description=None,
                 authority=None, profile=None, change_time=None):
        self.project_name = projectname
        self.description = description
        self.create_time = util.get_utc_time()
        self.authority = authority
        self.profile = profile
        if not change_time:
            self.change_time = util.get_utc_time()

    def format_detail(self, get_user=True):
        detail = {
            'id': self.id.hex,
            'project_name': self.projectname,
            'description': self.description,
            'create_time': self.create_time,
            'likes': self.likes,
            'authority': self.authority
        }
        if get_user:
            detail['user'] = self.user.format_detail()
        if self.profile:
            detail['profile'] = self.profile

        return detail


class Data(Base):
    __tablename__ = 'data'
    id = Column(GUID(),
                default=uuid.uuid4,
                primary_key=True)
    project_name = Column(GUID(),
                          ForeignKey('project.id'))
    data_json = Column(JSON,
                       nullable=True)
    user_id = Column(GUID(),
                     ForeignKey('user.id'))
