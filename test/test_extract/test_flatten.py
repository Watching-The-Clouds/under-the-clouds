from extract_utils import flatten
import pytest

def test_returns_dict():
    test_input = "x"   

    assert type(flatten(test_input)) == dict

def test_empty_input():
    assert flatten({}) == {}
    assert flatten([]) == {}
    assert flatten("") == {"": ""}

def test_nested_dict():
    test_input = {"a": {"b": {"c": 1}}}

    expected_output = {"a.b.c": 1}

    assert flatten(test_input) == expected_output

def test_nested_list():
    test_input = [1, [2, [3]]]

    expected_output = {"0": 1, "1.0": 2, "1.1.0": 3}

    assert flatten(test_input) == expected_output

def test_mixed_dict_list():
    test_input = {"a": [1, {"b": 2}]}

    expected_output = {"a.0": 1, "a.1.b": 2}

    assert flatten(test_input) == expected_output

def test_primitive_value():
    test_input = 42

    expected_output = {"": 42}

    assert flatten(test_input) == expected_output

def test_with_name():
    test_input = {"b": 1}

    expected_output = {"prefix.b": 1}

    assert flatten(test_input, name="prefix") == expected_output

def test_special_character_keys():
    test_input = {"a b": {"c@d": 3}}

    expected_output = {"!.a b.c@d": 3}

    assert flatten(test_input, "!") == expected_output

def test_large_input():
    test_input = {"a": list(range(1000))}

    result = flatten(test_input)

    assert result["a.999"] == 999

def test_for_additional_keys_in_some_dicts():
    test_input = [{'a':'b',
                   'c':'d'},
                  {'e':'f', 
                   'g':'h',
                   'i':{'j':'k'}}]

    expected_output = {'0.a':'b','0.c':'d','1.e':'f', '1.g':'h', '1.i.j':'k'}

    assert flatten(test_input) == expected_output