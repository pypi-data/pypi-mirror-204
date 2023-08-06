import enum
import inspect
from abc import ABCMeta
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Type, TypeVar

from tdm.abstract.datamodel import AbstractMarkup, AbstractNode
from tdm.helper import generics_mapping
from ._delegate import getter_delegate, modifier_delegate, property_delegate
from ._impl import AbstractNodeWrapperImpl
from ._interface import _Node as _NodeType

_Node = TypeVar('_Node', bound=AbstractNode)
_Markup = TypeVar('_Markup', bound=AbstractMarkup)


class MethodType(str, enum.Enum):
    getter = 'getter'
    modifier = 'modifier'


class NodeWrapperDecorator(object):
    _validators = {}
    _method2type = {}

    @classmethod
    def generate_wrapper(cls, markup: Type[_Markup]):
        def generate_type(cls_: Type[_Node]) -> Type[_Node]:
            node_type = generics_mapping(cls_)[_NodeType]
            validators = defaultdict(list)

            for _, f in inspect.getmembers(cls_, predicate=inspect.isfunction):
                if f in cls._validators:
                    validators[cls._validators[f]].append(f)

            methods = {
                '_node_type': classmethod(lambda _: node_type),
                '_markup_type': classmethod(lambda _: markup),
                '__hash__': lambda self: node_type.__hash__(self)
            }

            for name in cls_.__abstractmethods__:  # delegate all abstract methods to markup
                try:
                    methods[name] = cls._delegate(name, getattr(cls_, name), validators)
                except KeyError:
                    pass

            class _Impl(AbstractNodeWrapperImpl[node_type, markup], cls_, metaclass=ABCMeta):
                pass

            return dataclass(frozen=True, eq=False)(type(f'{cls_.__name__}with{markup.__name__}', (_Impl,), methods))

        return generate_type

    @classmethod
    def validate(cls, orig: Callable):
        def decorate(f):
            # TODO: check signature
            cls._validators[f] = orig
            return f

        return decorate

    @classmethod
    def _delegate(cls, name, f, validators):
        if isinstance(f, property):
            return property_delegate(name)
        mode = cls._method2type[f]
        if mode is MethodType.getter:
            return getter_delegate(name)
        elif mode is MethodType.modifier:
            return modifier_delegate(name, validators.get(f, []))
        raise ValueError

    @classmethod
    def set_method_type(cls, method: MethodType):
        def wrap(f):
            cls._method2type[f] = method
            return f

        return wrap
