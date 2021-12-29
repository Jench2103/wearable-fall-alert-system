from __future__ import annotations
from enum import unique
import json
import random
import string
from typing import Union
from datetime import datetime

from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from flaskr import db


class DatabaseManager():
    @classmethod
    def create(cls, object) -> bool:
        if not isinstance(object, db.Model):
            return False
        db.session.add(object)
        return cls.update()

    @classmethod
    def update(cls) -> bool:
        try:
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def delete(cls, object) -> bool:
        if not isinstance(object, db.Model):
            return False
        db.session.delete(object)
        return cls.update()


class User(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    # password_hash = db.Column(db.Text)
    name = db.Column(db.String, nullable=True)
    sex = db.Column(db.String, nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    blood_type = db.Column(db.String, nullable=True)
    line_id = db.Column(db.Text, nullable=True)
    insurer_id = db.Column(db.Integer, nullable=True)
    hospital = db.Column(db.Text, unique=False, nullable=True)

    def __init__(self, username: str, **kwargs):
        self.username = username
        # self.password_hash = generate_password_hash(kwargs['password']) if 'password' in kwargs else None
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.sex = kwargs['sex'] if '' in kwargs else None
        self.birthday = kwargs['birthday'] if 'birthday' in kwargs else None
        self.blood_type = kwargs['blood_type'] if 'blood_type' in kwargs else None
        self.line_id = kwargs['line_id'] if 'line_id' in kwargs else None

    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)
        
    # def set_password(self, password: str) -> None:
    #     self.password_hash = generate_password_hash(password)
    #     DatabaseManager.update()

    # def check_password(self, password: str) -> bool:
    #     return check_password_hash(self.password_hash, password)

    def remove(self) -> bool:
        return DatabaseManager.delete(self)

    @classmethod
    def create(cls, username: str, **kwargs) -> User:
        # check USERNAME duplication
        if cls.query.filter(func.lower(cls.username) == func.lower(username)).first() is not None:
            raise ValueError('username')

        # generate new user
        new_user = cls(username, **kwargs)
        DatabaseManager.create(new_user)
        return new_user


class EmergencyContact(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False)
    name = db.Column(db.String, unique=False)
    phone = db.Column(db.Text, nullable=True, unique=False)
    line_id = db.Column(db.Text, nullable=True, unique=False)

    def __init__(self, user_id: int, **kwargs):
        self.user_id = user_id
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.phone = kwargs['phone'] if 'phone' in kwargs else None
        self.line_id = kwargs['line_id'] if 'line_id' in kwargs else None

    def remove(self) -> bool:
        return DatabaseManager.delete(self)


    @classmethod
    def create(cls, user_id: int, **kwargs) -> EmergencyContact:
        new_emergency_contact = cls(user_id, **kwargs)
        DatabaseManager.create(new_emergency_contact)
        return new_emergency_contact

    @classmethod
    def get_emergency_contact(cls, user_id: int) -> list:
        return cls.query.filter_by(user_id=user_id).all() or []


class EmergencyEvent(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False)
    time = db.Column(db.DateTime, unique=False)
    location = db.Column(db.Text, unique=False, nullable=True)  # {"gps": {"longitude": 121.0, "latitude": 24.0}, "address": ""}
    user_status = db.Column(db.Text, unique=False, nullable=True)   # {"heart_rate": 120}
    event_status = db.Column(db.Text, unique=False, nullable=True)  # [{"time": "", "type": "", "agency": "", "content": ""}]
    web_token = db.Column(db.Text, unique=True)

    def __init__(self, user_id: int, time: datetime, **kwargs):
        self.user_id = user_id
        self.time = time
        self.location = json.dumps(kwargs.get('location', None), ensure_ascii=False) if type(kwargs.get('location', None)) == dict else json.dumps(dict(), ensure_ascii=False)
        self.user_status = json.dumps(kwargs.get('user_status', None), ensure_ascii=False) if type(kwargs.get('user_status', None)) == dict else json.dumps(dict(), ensure_ascii=False)
        self.event_status = json.dumps(kwargs.get('event_status', None), ensure_ascii=False) if type(kwargs.get('event_status', None)) == dict else json.dumps(dict(), ensure_ascii=False)
        self.web_token = kwargs.get('web_token', '')

    def remove(self) -> bool:
        return DatabaseManager.delete(self)


    @classmethod
    def create(cls, user_id: int, **kwargs) -> EmergencyEvent:
        while True:
            token = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(12))
            if cls.query.filter_by(web_token=token).first() is None:
                break
        new_emergency_event = cls(user_id, kwargs.get('time', datetime.now()), web_token=token, **kwargs)
        DatabaseManager.create(new_emergency_event)
        return new_emergency_event


class AmbulanceInfo(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.Text, nullable=True)       # phone number list in json data
    line_id = db.Column(db.Text, nullable=True)     # Line ID list in json data
    address = db.Column(db.Text, nullable=True)     # address dict in json data

    def __init__(self, name: str, **kwargs):
        self.name = name
        self.phone = json.dumps(kwargs['phone'], ensure_ascii=False) if kwargs.get('phone', None) is list else None
        self.line_id = json.dumps(kwargs['line_id'], ensure_ascii=False) if kwargs.get('line_id', None) is list else None
        self.address = json.dumps(kwargs['address'], ensure_ascii=False) if kwargs.get('address', None) is dict else None


    @classmethod
    def create(cls, name: str, **kwargs) -> AmbulanceInfo:
        new_ambulance = cls(name, **kwargs)
        DatabaseManager.create(new_ambulance)
        return new_ambulance


class DistrictAffairsInfo(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.Text, nullable=True)       # phone number list in json data
    line_id = db.Column(db.Text, nullable=True)     # Line ID list in json data
    address = db.Column(db.Text, nullable=True)     # address dict in json data

    def __init__(self, name: str, **kwargs):
        self.name = name
        self.phone = json.dumps(kwargs['phone'], ensure_ascii=False) if kwargs.get('phone', None) is list else None
        self.line_id = json.dumps(kwargs['line_id'], ensure_ascii=False) if kwargs.get('line_id', None) is list else None
        self.address = json.dumps(kwargs['address'], ensure_ascii=False) if kwargs.get('address', None) is dict else None


    @classmethod
    def create(cls, name: str, **kwargs) -> DistrictAffairsInfo:
        new_district_affairs = cls(name, **kwargs)
        DatabaseManager.create(new_district_affairs)
        return new_district_affairs


class InsurerInfo(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.Text, nullable=True)

    def __init__(self, name: str, **kwargs):
        self.name = name
        self.email = kwargs.get('email', None)


    @classmethod
    def create(cls, name: str, **kwargs) -> InsurerInfo:
        new_insurer = cls(name, **kwargs)
        DatabaseManager.create(new_insurer)
        return new_insurer


class LineToken(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    owner_class_name = db.Column(db.String, unique=False)
    owner_object_id = db.Column(db.Integer, unique=True)
    token_hash = db.Column(db.Text, unique=True)
    disposable = db.Column(db.Boolean)
    has_used = db.Column(db.Boolean, default=False)

    def __init__(self, owner_class_name: str, owner_object_id: int, disposable: bool = True):
        self.owner_class_name = owner_class_name
        self.owner_object_id = owner_object_id
        self.disposable = disposable
    
    def check_token(self, token: str) -> bool:
        return check_password_hash(self.token_hash, token)


    @classmethod
    def generate(cls, owner_class_name: str, owner_object_id: int, disposable: bool = False, token_length: int = 6) -> str:
        token_length = 6 if token_length <= 0 or token_length > 24 else token_length
        while True:
            token = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(token_length))
            if cls.get_match_token(token) is None:
                break
        token_object = cls(owner_class_name, owner_object_id, disposable)
        token_object.token_hash = generate_password_hash(token)
        DatabaseManager.create(token_object)
        return token

    @classmethod
    def get_match_token(cls, token: str) -> Union[LineToken, None]:
        for token_object in (cls.query.all() or []):
            if token_object.disposable and token_object.has_used:
                DatabaseManager.delete(token_object)
                continue
            if check_password_hash(token_object.token_hash, token):
                token_object.has_used = True
                DatabaseManager.update(token_object)
                return token_object
        return None
