import pytest

from byt.object_relations.error import SubstitutionNotAllowedError
from tests.object_relations.conftest import Ssn, SsnPerson, TestPersonSsn


def test_add_one(one_orm: TestPersonSsn):
    orm, person, ssn = one_orm

    assert orm.get_relation(person.ssn) is ssn
    assert orm.get_relation(ssn.person) is person
    assert len(orm.get_type(SsnPerson)) == 1
    assert len(orm.get_type(Ssn)) == 1


def test_remove_one(one_orm: TestPersonSsn):
    orm, person, ssn = one_orm
    orm.remove(person, ssn)

    assert orm.get_relation(person.ssn) is None
    assert orm.get_relation(ssn.person) is None
    assert not orm.get_type(SsnPerson)
    assert not orm.get_type(Ssn)


def test_substitution_not_allowed(one_orm: TestPersonSsn):
    orm, person, ssn = one_orm
    another_ssn = Ssn()
    another_person = SsnPerson()

    with pytest.raises(SubstitutionNotAllowedError):
        orm.add(person, another_ssn)

    with pytest.raises(SubstitutionNotAllowedError):
        orm.add(another_person, ssn)
