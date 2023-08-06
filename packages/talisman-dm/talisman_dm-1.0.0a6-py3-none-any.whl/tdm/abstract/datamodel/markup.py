from abc import abstractmethod
from dataclasses import dataclass
from typing import Mapping, Sequence, Type, TypeVar

from immutabledict import immutabledict

_AbstractMarkup = TypeVar('_AbstractMarkup', bound='AbstractMarkup')


class AbstractMarkup(object):
    @property
    @abstractmethod
    def markup(self) -> immutabledict:
        pass

    @classmethod
    @abstractmethod
    def from_markup(cls: Type[_AbstractMarkup], markup: 'AbstractMarkup') -> _AbstractMarkup:
        pass

    def __hash__(self):
        return hash(self.markup)

    def __eq__(self, other):
        if not isinstance(other, AbstractMarkup):
            return NotImplemented
        return self.markup == other.markup


@dataclass(frozen=True)
class FrozenMarkup(AbstractMarkup):
    _markup: immutabledict = immutabledict()

    @property
    def markup(self) -> immutabledict:
        return self._markup

    @classmethod
    def from_markup(cls, markup: AbstractMarkup) -> 'FrozenMarkup':
        if isinstance(markup, FrozenMarkup):
            return markup
        return cls(markup.markup)

    def __hash__(self):
        return hash(self._markup)

    @classmethod
    def freeze(cls, markup: dict) -> 'FrozenMarkup':
        if not isinstance(markup, dict):
            raise ValueError
        return cls(_freeze_dict(markup))


def _freeze_dict(obj: Mapping) -> immutabledict:
    return immutabledict((k, _freeze(v)) for k, v in obj.items())


def _freeze(obj):
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, Mapping):
        return _freeze_dict(obj)
    if isinstance(obj, set):
        return frozenset(_freeze(v) for v in obj)
    if isinstance(obj, Sequence):
        return tuple(_freeze(v) for v in obj)
    raise ValueError
