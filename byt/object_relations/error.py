__all__ = [
    'ObjectRelationError',
    'FrozenRelationError',
    'ManySameRelationsError',
]


class ObjectRelationError(Exception):
    pass


class FrozenRelationError(ObjectRelationError):
    pass


class ManySameRelationsError(ObjectRelationError):
    pass
