from abc import ABCMeta
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from typing import Callable, Generic, Iterable, Optional, Set, Type, TypeVar, Union

from .base import EnsureIdentifiable


@total_ordering
class FactStatus(str, Enum):
    def __new__(cls, name: str, priority: int):
        obj = str.__new__(cls, name)
        obj._value_ = name
        obj.priority = priority
        return obj

    APPROVED = ("approved", 0)
    DECLINED = ("declined", 1)
    AUTO = ("auto", 2)
    HIDDEN = ("hidden", 3)
    NEW = ("new", 4)

    def __lt__(self, other: 'FactStatus'):
        if not isinstance(other, FactStatus):
            return NotImplemented
        return self.priority < other.priority


@dataclass(frozen=True)
class AbstractFact(EnsureIdentifiable, metaclass=ABCMeta):
    status: FactStatus

    @staticmethod
    def id_filter(obj: Union['AbstractFact', str]) -> Callable[['AbstractFact'], bool]:
        id_ = obj.id if isinstance(obj, AbstractFact) else obj

        def _filter(fact: AbstractFact) -> bool:
            return fact.id == id_

        return _filter

    @staticmethod
    def status_filter(status: Union[FactStatus, Iterable[FactStatus]]) -> Callable[['AbstractFact'], bool]:
        if isinstance(status, FactStatus):
            def _filter(fact: AbstractFact) -> bool:
                return fact.status is status
        else:
            statuses = frozenset(status)

            def _filter(fact: AbstractFact) -> bool:
                return fact.status in statuses

        return _filter

    @staticmethod
    def type_filter(type_: Type['AbstractFact']) -> Callable[['AbstractFact'], bool]:
        def _filter(fact: AbstractFact) -> bool:
            return isinstance(fact, type_)

        return _filter


_ST = TypeVar('_ST', bound=AbstractFact)
_TT = TypeVar('_TT', bound=AbstractFact)


@dataclass(frozen=True)
class AbstractLinkFact(AbstractFact, Generic[_ST, _TT]):
    type_id: str
    source: _ST
    target: _TT
    value: Optional[str] = None

    @classmethod
    def constant_fields(cls) -> Set[str]:
        return {'source', 'target', 'type_id'}

    @staticmethod
    def type_id_filter(type_id: Union[str, Iterable[str]]) -> Callable[['AbstractLinkFact'], bool]:
        if isinstance(type_id, str):
            def _filter(fact: AbstractLinkFact) -> bool:
                return fact.type_id == type_id
        else:
            type_ids = frozenset(type_id)

            def _filter(fact: AbstractLinkFact) -> bool:
                return fact.type_id in type_ids

        return _filter

    @staticmethod
    def source_filter(filter_: Callable[[_ST], bool]) -> Callable[['AbstractLinkFact'], bool]:
        def _filter(fact: AbstractLinkFact) -> bool:
            return filter_(fact.source)

        return _filter

    @staticmethod
    def target_filter(filter_: Callable[[_TT], bool]) -> Callable[['AbstractLinkFact'], bool]:
        def _filter(fact: AbstractLinkFact) -> bool:
            return filter_(fact.target)

        return _filter
