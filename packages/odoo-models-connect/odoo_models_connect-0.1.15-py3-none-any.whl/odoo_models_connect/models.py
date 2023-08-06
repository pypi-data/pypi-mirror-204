import xmlrpc.client
from .fields import OdooField
from dotenv import dotenv_values
from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv
from .decorators import access_denied
from .exceptions import (
    GenericalException,
    ObjectDoesNotExist,
    IDRequiredException,
    EnvVariablesException,
    AccessDeniedException,
)

def load_env_vars(env_path):
    if not os.path.exists(env_path):
        raise FileNotFoundError(".env not found, wrong path")
    load_dotenv(env_path)

class OdooModel(object):
    _DATABASE = None
    _USERNAME = None
    _PASSWORD = None
    _URL = None
    _UUID = None
    _MODELS = None

    _COMMON = '/xmlrpc/2/common'
    _OBJECTS = '/xmlrpc/2/object'

    _FIELDS = {}

    _name = None
    id = None

    def __init__(self, **kwargs):
        self._FIELDS = {}
        if kwargs:
            for name, value in kwargs.items():
                setattr(self, name, value)
                self._FIELDS[name] = value

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"

    @classmethod
    def search_count(cls, query=[]):
        records = cls.search_read(query=query)
        return len(records)

    @classmethod
    def search_by_id(cls, obj_id=None):
        cls._validate_id_required(obj_id)
        record = cls.search_read(query=[["id", '=', obj_id]])
        cls._validate_object_not_exist(record, obj_id)
        return record[0]

    @classmethod
    def _validate_id_required(cls, obj_id):
        if obj_id is None:
            raise IDRequiredException()

    @classmethod
    def _validate_object_not_exist(cls, record, obj_id):
        if len(record) == 0:
            raise ObjectDoesNotExist(obj_id)

    @classmethod
    @access_denied
    def search_read(cls, query=[], **kwargs):
        records = cls._MODELS.execute_kw(
            cls._DATABASE,
            cls._UUID,
            cls._PASSWORD,
            cls._name,
            'search_read',
            [query],
            {'fields': list(cls._FIELDS.keys())}
        )
        instances = cls._instances_from_list(records)
        return instances

    @classmethod
    def _instances_from_list(cls, records):
        return [cls._create_instance_from_dict(record) for record in records]

    @classmethod
    def _create_instance_from_dict(cls, obj):
        return cls(**obj)

    @access_denied
    def create(self):
        return self._MODELS.execute_kw(self._DATABASE, self._UUID, self._PASSWORD, self._name, 'create', [self._FIELDS])

    @access_denied
    def update(self):
        return self._MODELS.execute_kw(self._DATABASE, self._UUID, self._PASSWORD, self._name, 'write', [[self.id], self._FIELDS])

    @access_denied
    def delete(self):
        return self._MODELS.execute_kw(self._DATABASE, self._UUID, self._PASSWORD, self._name, 'unlink', [[self.id]])

    def __init_subclass__(cls):
        try:
            cls._set_config_envs()
            cls._fill_fields()
            cls._set_attributes_initialized_none()
            super().__init_subclass__()
        except OSError:
            raise EnvVariablesException()

    @classmethod
    def _set_attributes_initialized_none(cls):
        cls._set_models_attribute()
        cls._set_uuid_attribute()

    @classmethod
    def _set_config_envs(cls):
        cls._DATABASE = os.getenv('DATABASE')
        cls._USERNAME = os.getenv('USERNAME')
        cls._PASSWORD = os.getenv('PASSWORD')
        cls._URL = os.getenv('URL')

    @classmethod
    def _set_uuid_attribute(cls):
        common = xmlrpc.client.ServerProxy(
            '{}{}'.format(cls._URL, cls._COMMON))
        cls._UUID = common.authenticate(
            cls._DATABASE, cls._USERNAME, cls._PASSWORD, {})

    @classmethod
    def _set_models_attribute(cls):
        cls._MODELS = xmlrpc.client.ServerProxy(
            '{}{}'.format(cls._URL, cls._OBJECTS))

    @classmethod
    def _fill_fields(cls):
        cls._FIELDS = {}
        cls._iterate_dir_class()

    @classmethod
    def _iterate_dir_class(cls):
        for attr_name in dir(cls):
            attr = cls._is_not_abstract_method_attribute(attr_name)
            cls._add_field_if_is_odoo_field(attr, attr_name)

    @classmethod
    def _add_field_if_is_odoo_field(cls, attr, attr_name):
        if isinstance(attr, OdooField):
            cls._FIELDS[attr_name] = attr._type

    @classmethod
    def _is_not_abstract_method_attribute(cls, attr_name):
        if attr_name != '__abstractmethods__':
            return getattr(cls, attr_name)
