from byt.middleware.utils import make_iterable


def test_make_iterable_none():
    assert make_iterable(None) == list()


def test_make_iterable_iterable():
    test_list = [1, 2, 3]
    assert make_iterable(test_list) is test_list

    test_set = {1, 2, 3}
    assert make_iterable(test_set) is test_set

    test_tuple = (1, 2, 3)
    assert make_iterable(test_tuple) is test_tuple


def test_make_iterable_default():
    test_object = object()
    iterable_test_object = make_iterable(test_object)
    assert iterable_test_object == [test_object]
    assert test_object is iterable_test_object[0]
