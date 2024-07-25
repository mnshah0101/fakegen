""" 
import pytest
from dataclasses import dataclass
from fakegen.FakeGen import FakeGen  # Ensure this is the correct import path for FakeGen


@pytest.fixture
def fake_gen():
    return FakeGen(api_key="")


@dataclass
class Person:
    name: str
    age: int
    email: str


@pytest.fixture
def example_person():
    return Person(name="John Doe", age=30, email="johndoe@example.com")


@pytest.fixture
def example_dict():
    return {"key1": "value1", "key2": 42, "key3": [1, 2, 3]}


@pytest.fixture
def example_list():
    return [1, 2, 3, 4, 5]


def test_generate_fake_data_person(fake_gen, example_person):
    fake_persons = fake_gen.generate_fake_data(example_person, 3)
    assert len(fake_persons) == 3
    for person in fake_persons:
        assert isinstance(person, Person)
        assert hasattr(person, 'name')
        assert hasattr(person, 'age')
        assert hasattr(person, 'email')
        print(person)


def test_generate_fake_data_dict(fake_gen, example_dict):
    fake_dicts = fake_gen.generate_fake_data(example_dict, 3)
    assert len(fake_dicts) == 3
    for d in fake_dicts:
        assert isinstance(d, dict)
        assert "key1" in d
        assert "key2" in d
        assert "key3" in d
        print(d)


def test_generate_fake_data_list(fake_gen, example_list):
    fake_lists = fake_gen.generate_fake_data(example_list, 3)
    assert len(fake_lists) == 3
    for lst in fake_lists:
        assert isinstance(lst, list)
        assert all(isinstance(item, int) for item in lst)
        print(lst)

        
        """
