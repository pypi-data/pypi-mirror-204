from dataclasses import dataclass
from typing import Callable, Sequence, Set, Tuple, Union

from tdm.abstract.datamodel import AbstractFact, FactStatus, Identifiable
from tdm.abstract.datamodel.value import AbstractValue
from tdm.abstract.json_schema import generate_model


@dataclass(frozen=True)
class _AtomValueFact(AbstractFact):
    type_id: str
    # tuple is in first place due to strange pydantic bug ((AbstractValue,) is treated as AbstractValue)
    value: Union[Tuple[AbstractValue, ...], AbstractValue] = tuple()

    def __post_init__(self):
        if isinstance(self.value, Sequence) and not isinstance(self.value, AbstractValue):  # AbstractValue could implement Sequence?
            if any(not isinstance(v, AbstractValue) for v in self.value):
                raise ValueError(f"Atom value fact {self} value should be value or tuple of value")
            object.__setattr__(self, 'value', tuple(self.value))
        elif not isinstance(self.value, AbstractValue):
            raise ValueError(f"Atom value fact {self} value should be value or tuple of value")

        if self.status is FactStatus.NEW and isinstance(self.value, AbstractValue):
            object.__setattr__(self, 'value', (self.value,))
        elif self.status is FactStatus.APPROVED and isinstance(self.value, tuple):
            if len(self.value) != 1 or not isinstance(self.value[0], AbstractValue):
                raise ValueError(f"approved fact {self} should have single value")
            object.__setattr__(self, 'value', self.value[0])

    @classmethod
    def constant_fields(cls) -> Set[str]:
        return {'type_id'}


@generate_model(label='atom')
@dataclass(frozen=True)
class AtomValueFact(Identifiable, _AtomValueFact):
    @staticmethod
    def empty_value_filter() -> Callable[['AtomValueFact'], bool]:
        return lambda f: isinstance(f.value, tuple) and not f.value

    @staticmethod
    def tuple_value_filter() -> Callable[['AtomValueFact'], bool]:
        return lambda f: isinstance(f.value, tuple)

    @staticmethod
    def single_value_filter() -> Callable[['AtomValueFact'], bool]:
        return lambda f: isinstance(f.value, AbstractValue)


@dataclass(frozen=True)
class _CompositeValueFact(AbstractFact):
    type_id: str

    @classmethod
    def constant_fields(cls) -> Set[str]:
        return {'type_id'}


@generate_model(label='composite')
@dataclass(frozen=True)
class CompositeValueFact(Identifiable, _CompositeValueFact):
    pass
