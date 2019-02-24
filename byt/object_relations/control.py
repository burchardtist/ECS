from dataclasses import dataclass
from typing import Dict, List, Set, Union
from uuid import UUID

from byt.object_relations.error import InvalidRelationError, \
    ManySameRelationsError, MissingRelationError, SubstitutionNotAllowedError
from byt.object_relations.relations import ManyRelation, OneRelation, Relation
from byt.object_relations.utils import method_dispatch

__all__ = [
    'ObjectRelation'
]


@dataclass
class RelationFields:
    rel1: Relation
    rel2: Relation


class ObjectRelation:
    _container: Dict[UUID, Union[Set[object], object]]

    def __init__(self):
        self._container = dict()

    @method_dispatch
    def _add_relation(self, relation: Relation, related: object):
        raise InvalidRelationError(  # pragma: no cover
            f'invalid relation `{relation.relation_type}`'
        )

    @_add_relation.register
    def _many_add(self, relation: ManyRelation, related: object):
        container = self._container
        id_ = relation.id

        if id_ not in container.keys():
            container[id_] = set()
        container[id_].add(related)

    @_add_relation.register
    def _one_add(self, relation: OneRelation, related: object):
        container = self._container
        id_ = relation.id

        if container.get(id_):
            if not relation.substitution:
                raise SubstitutionNotAllowedError
            raise NotImplementedError

        container[id_] = related

    def _get_fields(self, obj1: object, obj2: object) -> RelationFields:
        def seek_relations(obj) -> List[Relation]:
            return [
                getattr(obj, x) for x in dir(obj)
                if isinstance(getattr(obj, x), Relation)
            ]

        obj1_fields = seek_relations(obj1)
        obj2_fields = seek_relations(obj2)

        if not (len(obj1_fields) == 1 and len(obj2_fields) == 1):
            raise ManySameRelationsError

        return RelationFields(
            rel1=obj1_fields[0],
            rel2=obj2_fields[0],
        )

    @method_dispatch
    def _remove_relation(self, relation: Relation, related: object):
        raise InvalidRelationError(  # pragma: no cover
            f'invalid relation `{relation.relation_type}`'
        )

    @_remove_relation.register
    def _many_remove(self, relation: ManyRelation, related: object):
        container = self._container
        id_ = relation.id
        try:
            container[id_].remove(related)
        except KeyError:
            raise MissingRelationError

    @_remove_relation.register
    def _one_remove(self, relation: OneRelation, related: object):
        container = self._container
        id_ = relation.id

        try:
            del container[id_]
        except KeyError:
            raise MissingRelationError

    def get(self, relation: Relation):
        return self._container.get(relation.id)

    def add(self, obj1: object, obj2: object):
        relations = self._get_fields(obj1, obj2)
        self._add_relation(relations.rel1, obj2)
        self._add_relation(relations.rel2, obj1)

    def remove(self, obj1: object, obj2: object):
        relations = self._get_fields(obj1, obj2)
        self._remove_relation(relations.rel1, obj2)
        self._remove_relation(relations.rel2, obj1)
