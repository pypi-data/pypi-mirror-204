from tdm.abstract.datamodel import AbstractFact, AbstractMarkup, AbstractNode, AbstractNodeMention, AbstractValue, BaseNodeMetadata
from .identifiable import IdSerializer
from .markup import MarkupSerializer
from .mention import NodeMentionSerializer
from .metadata import NodeMetadataSerializer
from .value import ValueSerializer


def build_serializers():
    result = {
        AbstractNode: IdSerializer(AbstractNode),
        AbstractFact: IdSerializer(AbstractFact),
        AbstractNodeMention: NodeMentionSerializer(),
        BaseNodeMetadata: NodeMetadataSerializer(),
        AbstractValue: ValueSerializer(),
        AbstractMarkup: MarkupSerializer()
    }
    # other serializers could be added here
    return result
