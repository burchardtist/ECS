from dataclasses import dataclass
from typing import Dict, Set, Optional
from uuid import UUID

from byt.object_relations.error import InvalidRelationError, \
    ManySameRelationsError, MissingRelationError, SubstitutionNotAllowedError
from byt.object_relations.relations import ManyRelation, OneRelation, Relation
from byt.object_relations.utils import method_dispatch

__all__ = [
    'ObjectRelation'
]


@dataclass(frozen=True)
class RelationFields:
    rel1: Relation
    rel2: Relation


class ObjectRelation:
    def __init__(self):
        self._container: Dict[UUID, Set[object]] = dict()
        self._relations: Dict[int, Relation] = dict()
        self._objects: Dict[int, Set[object]] = dict()

    @method_dispatch
    def _add_relation(self, relation: Relation, related: object):
        raise InvalidRelationError(  # pragma: no cover
            f'invalid relation `{type(relation)}`'
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
        self._container[relation.id] = {related}

    def _seek_relations(self, obj: object) -> Relation:
        return self._relations.get(id(obj)) or self._setup_relation(obj)

    def _setup_relation(self, obj: object) -> Relation:
        relations = {
            getattr(obj, x) for x in dir(obj)
            if isinstance(getattr(obj, x), Relation)
        }

        if not len(relations) == 1:
            raise ManySameRelationsError

        relation = relations.pop()
        self._relations[id(obj)] = relation

        return relation

    def _get_relations(self, obj1: object, obj2: object) -> RelationFields:
        return RelationFields(
            rel1=self._seek_relations(obj1),
            rel2=self._seek_relations(obj2),
        )

    @method_dispatch
    def _remove_relation(self, relation: Relation, related: object):
        raise InvalidRelationError(  # pragma: no cover
            f'invalid relation `{type(relation)}`'
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

    def _ensure_substitution(
            self,
            obj1: object,
            obj2: object,
            relations: RelationFields
    ):
        if (isinstance(relations.rel1, OneRelation) and
                isinstance(relations.rel2, ManyRelation)):
            one_relation = relations.rel1
            to_remove = obj1
        elif (isinstance(relations.rel2, OneRelation) and
                isinstance(relations.rel1, ManyRelation)):
            one_relation = relations.rel2
            to_remove = obj2
        else:
            return

        if self._container.get(one_relation.id):
            if not one_relation.substitution:
                raise SubstitutionNotAllowedError
            relation = self._relations[id(self.get_relation(one_relation))]
            self._remove_relation(relation, to_remove)

    def _add_objects(self, *objects: object):
        objects_dict = self._objects
        for obj in objects:
            type_id = id(type(obj))
            if type_id not in objects_dict.keys():
                objects_dict[type_id] = set()
            objects_dict[type_id].add(obj)

    def _remove_objects(self, *objects: object):
        objects_dict = self._objects
        for obj in objects:
            objects_dict[id(type(obj))].remove(obj)

    @method_dispatch
    def get_relation(self, relation: Relation):
        raise InvalidRelationError(  # pragma: no cover
            f'invalid relation `{type(relation)}`'
        )

    @get_relation.register
    def _get_many(self, relation: ManyRelation) -> Set[object]:
        return self._container.get(relation.id)

    @get_relation.register
    def _get_one(self, relation: OneRelation) -> Optional[object]:
        obj = self._container.get(relation.id)
        return list(obj)[0] if obj else None
    
    def get_type(self, type_: type) -> Set[object]:
        return self._objects.get(id(type_)) or set()

    def add(self, obj1: object, obj2: object):
        relations = self._get_relations(obj1, obj2)
        self._ensure_substitution(obj1, obj2, relations)
        self._add_relation(relations.rel1, obj2)
        self._add_relation(relations.rel2, obj1)
        self._add_objects(obj1, obj2)

    def remove(self, obj1: object, obj2: object):
        relations = self._get_relations(obj1, obj2)
        self._remove_relation(relations.rel1, obj2)
        self._remove_relation(relations.rel2, obj1)
        self._remove_objects(obj1, obj2)
