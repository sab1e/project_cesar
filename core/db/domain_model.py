import datetime


class Field(property):
    def __init__(self):
        super().__init__(self.get_value, self.set_value)
        self.name = None
        self.storage_name = None
        self.model_cls = None

    def bind_name(self, name):
        self.name = name
        self.storage_name = ''.join(('_', self.name))
        return self

    def bind_model_cls(self, model_cls):
        self.model_cls = model_cls
        return self

    def init_model(self, model, value):
        self.set_value(model, value)

    def get_value(self, model):
        return getattr(model, self.storage_name)

    def set_value(self, model, value):
        setattr(model, self.storage_name, self.__converter(value))

    def get_builtin_type(self, model):
        return self.get_value(model)

    def __converter(self, value):
        return value

    @staticmethod
    def _get_model_instance(model_cls, data):
        return model_cls(**data) if isinstance(data, dict) else data


class Boll(Field):
    def __converter(self, value):
        return bool(value)


class Int(Field):
    def __converter(self, value):
        return int(value)


class Float(Field):
    def __converter(self, value):
        return float(value)


class String(Field):
    def __converter(self, value):
        return str(value)


class Date(Field)
    def __converter(self, value):
        if not isinstance(value, datetime.date):
            raise TypeError(f'{value} is not valid date')


class Model(Field):
    def __init__(self, related_model_cls):
        super().__init__()
        self.related_model_cls = related_model_cls

    def __converter(self, value):
        return self._get_model_instance(self.related_model_cls, value)

    def get_builtin_type(self, model):
        return self.get_value(model).get_data()


class FieldCollection(Field):
    def __init__(self, related_model_cls):
        super().__init__()
        self.related_model_cls = related_model_cls

    def get_builtin_type(self, model):
        return [item.get_data() if isinstance(item, self.related_model_cls)
                else item for item in self.get_value(model)]


class DomainModelMetaClass(type):
    def __new__(cls, class_name, bases, attributes):
        model_fields = cls.parse_fields(attributes)

        if attributes.get('__slots_optimization__', True):
            attributes['__slots__'] = cls.prepare_model_slots(model_fields)

        new_cls = type.__new__(cls, class_name, bases, attributes)

        new_cls.__fields__ = cls.bind_fields_attribute(
            attribute_name='__unique_key', attributes=attributes,
            class_name=class_name)

        new_cls.__view_key__ = cls.prepare_fields_attribute(
            attribute_name='__view_key', attributes=attributes,
            class_name=class_name)

        return new_cls

    @staticmethod
    def parse_fields(attributes):
        return tuple(field.bind_name(name)
                      for name, field in attributes.items()
                      if isinstance(field, Field))

    @staticmethod
    def prepare_model_slots(model_fields):
        return tuple(field.storage_name for field in model_fields)

    @staticmethod
    def prepare_fields_attribute(attribute_name, attributes, class_name):
        attribute = attributes.get(attribute_name)
        if attribute:
            return tuple(attribute)
        else:
            return tuple()

    @staticmethod
    def bind_fields_to_model_cls(new_cls, model_fields):
        return dict((field.name, field.bind_model_cls(new_cls))
                    for field in model_fields)


class DomainModel(metaclass=DomainModelMetaClass):
    __fields__ = dict()
    __view_key__ = tuple()
    __unique_key__ = tuple()
    __slots_optimization__ = True

    def __init__(self, **kwargs):
        for name, field in self.__class__.__fields__.items():
            field.init_model(self, kwargs.get(name))

    def __eq__(self, other):
        if self is other:
            return True

        if not isinstance(other, self.__class__):
            return False

        if not self.__class__.__unique_key__:
            return NotImplemented

        for field in self.__class__.__unique_key__:
            if field.get_value(self) != field.get_value(other):
                return False

        return True

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self == other
        return NotImplemented

    def __str__(self):
        if not self.__class__.__view_key__:
            return self.__repr__()

        fields_values = ', '.join(
            '='.join((field.name, str(field.get_value(self))))
            for field in self.__class__.__view_key__)
        return f'{self.__class__.__name__}({fields_values})'

    def get(self, field_name):
        try:
            field = self.__class__.__fields__[field_name]
        except KeyError:
            raise AttributeError(f"Field {field_name} does not exist.")
        else:
            return field.get_value(self)

    def get_data(self):
        return dict((name, field.get_builtin_type(self))
                    for name, field in
                    self.__class__.__fields__.items())

    def set_data(self, data):
        for name, field in self.__class__.__fields__.items():
            field.init_model(self, data.get(name))
