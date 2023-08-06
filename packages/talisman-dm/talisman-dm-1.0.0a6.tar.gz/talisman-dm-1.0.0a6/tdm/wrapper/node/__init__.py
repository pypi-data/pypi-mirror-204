__all__ = [
    'AbstractNodeWrapper',
    'generate_wrapper', 'validate', 'getter', 'modifier'
]

from ._decorator import MethodType, NodeWrapperDecorator
from ._interface import AbstractNodeWrapper

generate_wrapper = NodeWrapperDecorator.generate_wrapper
validate = NodeWrapperDecorator.validate

getter = NodeWrapperDecorator.set_method_type(MethodType.getter)
modifier = NodeWrapperDecorator.set_method_type(MethodType.modifier)
