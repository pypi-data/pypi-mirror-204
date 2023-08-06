from dataclasses import dataclass
from typing import Callable, Optional, Sequence, Set, Tuple, Union

from tdm.abstract.datamodel import AbstractFact, FactStatus, Identifiable
from tdm.abstract.json_schema import generate_model


@dataclass(frozen=True)
class ConceptValue(object):
    concept: str
    confidence: Optional[float] = None

    def __post_init__(self):
        if self.confidence is not None and not 0 < self.confidence <= 1:
            raise ValueError(f"value confidence should be in interval (0; 1], {self.confidence} is given")

    @classmethod
    def build(cls, value: Union[str, 'ConceptValue']) -> 'ConceptValue':
        if isinstance(value, ConceptValue):
            return value
        if isinstance(value, str):
            return cls(concept=value)
        raise ValueError


@dataclass(frozen=True)
class _ConceptFact(AbstractFact):  # not an error as id argument is kw only
    type_id: str
    value: Union[ConceptValue, Tuple[ConceptValue, ...]] = tuple()

    def __post_init__(self):
        if isinstance(self.value, str):
            object.__setattr__(self, 'value', ConceptValue.build(self.value))
        elif isinstance(self.value, Sequence):
            object.__setattr__(self, 'value', tuple(map(ConceptValue.build, self.value)))
        else:
            object.__setattr__(self, 'value', ConceptValue.build(self.value))

        if self.status is FactStatus.NEW and isinstance(self.value, ConceptValue):
            object.__setattr__(self, 'value', (self.value,))  # replace with tuple
        elif self.status is FactStatus.APPROVED and isinstance(self.value, tuple):
            if len(self.value) != 1:
                raise ValueError(f"approved fact {self} should have single value")
            object.__setattr__(self, 'value', self.value[0])

    @classmethod
    def constant_fields(cls) -> Set[str]:
        return {'type_id'}


@generate_model(label='concept')
@dataclass(frozen=True)
class ConceptFact(Identifiable, _ConceptFact):
    @staticmethod
    def empty_value_filter() -> Callable[['ConceptFact'], bool]:
        return lambda f: isinstance(f.value, tuple) and not f.value

    @staticmethod
    def tuple_value_filter() -> Callable[['ConceptFact'], bool]:
        return lambda f: isinstance(f.value, tuple)

    @staticmethod
    def single_value_filter() -> Callable[['ConceptFact'], bool]:
        return lambda f: isinstance(f.value, ConceptValue)
