import pytest

from byt.object_relations.control import ObjectRelation
from byt.object_relations.error import ManySameRelationsError
from byt.object_relations.relations import ManyRelation, OneRelation

SAMPLE_SIZE = 30


# FIXTURES
@pytest.fixture
def orm():
    return ObjectRelation()


# TEST MODELS
class IHouse:
    person: OneRelation

    def __init__(self):
        self.person = OneRelation(to_type=Person)


class ManyRelationsHouse:
    person_a: OneRelation
    person_b: OneRelation

    def __init__(self):
        self.person_a = OneRelation(to_type=Person)
        self.person_b = OneRelation(to_type=Person)


class Person:
    houses: ManyRelation

    def __init__(self):
        self.houses = ManyRelation(to_type=IHouse)


# TESTS
def test_unique_id():
    ids = {Person().houses.id for _ in range(SAMPLE_SIZE)}
    assert len(ids) == SAMPLE_SIZE


def test_add(orm: ObjectRelation):
    person = Person()
    houses_list = list()

    for _ in range(SAMPLE_SIZE):
        house = IHouse()
        houses_list.append(house)
        orm.add(person, house)

    assert len(orm.get(person.houses)) == SAMPLE_SIZE
    assert all([orm.get(house.person) is person for house in houses_list])


def test_multiple_relations(orm):
    person = Person()
    house = ManyRelationsHouse()
    with pytest.raises(ManySameRelationsError):
        orm.add(person, house)
