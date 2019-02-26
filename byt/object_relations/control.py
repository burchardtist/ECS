from abc import ABC
from dataclasses import dataclass
from typing import Dict, Optional, Set
from uuid import UUID

from byt.object_relations.error import InvalidRelationError, \
    ManySameRelationsError, MissingRelationError, SubstitutionNotAllowedError
from byt.object_relations.relations import ManyRelation, OneRelation, Relation
from byt.object_relations.utils import method_dispatch

__all__ = [
    'ObjectRelationManager'
]


@dataclass(frozen=True)
class RelationFields:
    rel1: Relation
    rel2: Relation


class RelationOperationsDispatcher(ABC):
    """
    Takes care of relation operations: get, add, remove.
    Every operation has method dispatch for OneRelation and ManyRelation.
    """

    def __init__(self):
        self._container: Dict[UUID, Set[object]] = dict()

    # GET #####################################################################
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

    # ADD #####################################################################
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

    # REMOVE ##################################################################
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


class ObjectsContainer(ABC):
    """
    Holds objects of the same type.
    Keeps self._add_objects and self._remove_objects as protected methods.
    """

    def __init__(self):
        self._objects: Dict[type, Set[object]] = dict()

    def get_type(self, type_: type) -> Set[object]:
        return self._objects.get(type_) or set()

    def _add_objects(self, *objects: object):
        objects_dict = self._objects
        for obj in objects:
            type_id = type(obj)
            if type_id not in objects_dict.keys():
                objects_dict[type_id] = set()
            objects_dict[type_id].add(obj)

    def _remove_objects(self, *objects: object):
        objects_dict = self._objects
        for obj in objects:
            objects_dict[type(obj)].remove(obj)


class ObjectRelationManager(RelationOperationsDispatcher, ObjectsContainer):
    """
    Entry class to keep all objects bounded in relations.
    Ensures that objects are kept equally on the both sides of relations
    """
    def __init__(self):
        RelationOperationsDispatcher.__init__(self)
        ObjectsContainer.__init__(self)
        self._relations: Dict[int, Relation] = dict()

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

    def _ensure_substitution(
            self,
            obj1: object,
            obj2: object,
            relations: RelationFields
    ):
        """
        Provide substitution for one-to-many relation.

        If substitution is allowed and ManyRelation contains already
        the object to substitute remove it from this relation
        to ensure that it will not be duplicated.
        """
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

        if self.get_relation(one_relation):
            if not one_relation.substitution:
                raise SubstitutionNotAllowedError
            relation = self._relations[id(self.get_relation(one_relation))]
            self._remove_relation(relation, to_remove)

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
