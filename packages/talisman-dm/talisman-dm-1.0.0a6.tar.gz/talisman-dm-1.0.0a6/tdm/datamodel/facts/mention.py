from dataclasses import dataclass
from typing import Callable, Set, Union

from tdm.abstract.datamodel import AbstractFact, AbstractNode, AbstractNodeMention, Identifiable
from tdm.abstract.json_schema import generate_model
from .value import AtomValueFact


@dataclass(frozen=True)
class _MentionFact(AbstractFact):
    mention: AbstractNodeMention
    value: AtomValueFact

    @classmethod
    def constant_fields(cls) -> Set[str]:
        return {'mention', 'value'}


@generate_model(label='mention')
@dataclass(frozen=True)
class MentionFact(Identifiable, _MentionFact):
    @staticmethod
    def node_filter(node: Union[AbstractNode, str]) -> Callable[['MentionFact'], bool]:
        node_id = node.id if isinstance(node, AbstractNode) else node

        def _filter(fact: MentionFact) -> bool:
            return fact.mention.node_id == node_id

        return _filter

    @staticmethod
    def value_filter(filter_: Callable[[AtomValueFact], bool]) -> Callable[['MentionFact'], bool]:
        def _filter(fact: MentionFact) -> bool:
            return filter_(fact.value)

        return _filter
