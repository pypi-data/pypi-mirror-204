from collections import defaultdict
from typing import Dict, Iterable, Set, Tuple, Type, TypeVar, Union

from tdm.abstract.datamodel import EnsureIdentifiable
from ._container import TypedIdsContainer
from ._types import get_base_type
from ._view import AbstractView, object_view

_TD = TypeVar('_TD', bound='BaseImpl')


class BaseImpl(object):
    __slots__ = (
        '_id2view', '_dependencies', '_containers'
    )

    def __init__(
            self,
            id2view: Dict[str, Union[EnsureIdentifiable, AbstractView]],
            dependencies: Dict[str, Set[Tuple[str, Type[EnsureIdentifiable]]]],
            containers: Dict[Type[EnsureIdentifiable], TypedIdsContainer],
    ):
        self._id2view = id2view
        self._dependencies = dependencies
        self._containers = containers

    def _replace(self: _TD, **kwargs) -> _TD:
        return type(self)(
            **{
                'id2view': self._id2view,
                'dependencies': self._dependencies,
                'structure': self._structure,
                'containers': self._containers,
                **kwargs
            }
        )

    def with_elements(self: _TD, elements: Iterable[EnsureIdentifiable], *, update: bool = False) -> _TD:
        containers: Dict[Type[EnsureIdentifiable], TypedIdsContainer] = dict(self._containers)
        id2view = dict(self._id2view)
        dependencies = defaultdict(set, self._dependencies)
        updated = set()

        elements = self._order_dependencies(set(elements), update)

        for element_type, element, element_view in elements:
            container = containers[element_type]
            if element.id in container:
                try:
                    id2view[element.id].validate_update(element_view)
                except ValueError as e:
                    raise ValueError(f"Couldn't update element {element}") from e
            else:
                if element.id in id2view:
                    raise ValueError(f"Element {element} identifiers collision: document already "
                                     f"contains {id2view[element.id].orig_type()} with same id")
            if isinstance(element_view, AbstractView):
                for dep in element_view.__depends_on__:
                    if dep not in updated:
                        dependencies[dep] = set(dependencies[dep])
                        updated.add(dep)
                    dependencies[dep].add((element.id, element_type))
            id2view[element.id] = element_view
            containers[element_type] = containers[element_type].with_ids([(element.id, type(element))])

        return self._replace(
            id2view=id2view,
            dependencies=dependencies,
            containers=containers
        )

    def without_elements(self: _TD, ids: Iterable[str], *, cascade: bool = False) -> _TD:
        ids = set(self._id2view.keys()).intersection(ids)  # ignore excess ids
        if not cascade:
            # check no hang links
            for id_ in ids:
                for dep, _ in self._dependencies.get(id_, ()):
                    if dep not in ids:
                        raise ValueError(f"Couldn't remove element {id_} as it depends on element {dep}")
        remove_from_containers = defaultdict(set)
        id2view = dict(self._id2view)
        dependencies = dict(self._dependencies)
        updated = set()
        remove = defaultdict(set)
        for id_ in ids:
            remove[get_base_type(id2view[id_].orig_type())].add(id_)
        while remove:
            to_remove = defaultdict(set)
            for base_type, ids in remove.items():
                for id_ in ids:
                    for dep_id, dep_type in dependencies.get(id_, ()):
                        to_remove[dep_type].add(dep_id)
                    view = id2view.pop(id_)
                    dependencies.pop(id_, None)
                    remove_from_containers[base_type].add(id_)
                    if not isinstance(view, AbstractView):
                        continue
                    for dep in view.__depends_on__:
                        if dep not in dependencies:
                            continue
                        if dep not in updated:
                            dependencies[dep] = set(dependencies[dep])
                            updated.add(dep)
                        dependencies[dep].discard((id_, base_type))
                        if not dependencies[dep]:
                            dependencies.pop(dep)
            remove = to_remove

        containers = dict(self._containers)
        for base_type, ids in remove_from_containers.items():
            containers[base_type] = containers[base_type].without_ids(ids)

        return self._replace(id2view=id2view, dependencies=dependencies, containers=containers)

    def _order_dependencies(
            self, elements: Set[EnsureIdentifiable], update: bool = False
    ) -> Iterable[Tuple[Type[EnsureIdentifiable], EnsureIdentifiable, AbstractView]]:
        result = []
        visited = set()
        while elements:
            to_process = set()
            for element in elements:
                visited.add(element)
                view = object_view(element)

                result.append((get_base_type(element), element, view))

                if not isinstance(view, AbstractView):
                    continue  # no dependencies

                dependencies = view.get_dependencies(element)
                dependencies.difference_update(elements)  # will be processed next steps
                dependencies.difference_update(visited)
                if update:
                    to_process.update(dependencies)  # add to queue
                else:
                    self._validate_elements(dependencies)
            elements = to_process
        return result[::-1]

    def _validate_elements(self, elements: Set[EnsureIdentifiable]) -> None:
        for element in elements:
            if element.id not in self._id2view:
                raise ValueError(f"document contains no {element}")
            view = self._id2view[element.id]
            element_type = type(element)
            view_type = view.orig_type() if isinstance(view, AbstractView) else type(view)
            if not issubclass(element_type, view_type) or not issubclass(view_type, element_type):
                raise ValueError(f"Type mismatch for {element}. Expected: {view_type}, actual: {element_type}")
