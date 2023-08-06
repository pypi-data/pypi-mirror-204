#!/usr/bin/env python

"""Tests for `mongeasy` package."""
# Do this before importing mongeasy as it will try to connect to the database
import os
os.environ['MONGOEASY_CONNECTION_STRING'] = 'mongodb://localhost:27017'
os.environ['MONGOEASY_DATABASE_NAME'] = 'mongeasy_pytest'
from pymongo import MongoClient
import pytest


from mongeasy import create_document_class


@pytest.fixture(scope='function')
def clean_mongo():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['mongeasy_pytest']

    # Clean all collections in the test database
    for collection_name in db.list_collection_names():
        db[collection_name].delete_many({})



def test_document_init_with_dict(clean_mongo):
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user.save()
    stored_user = User.find({'first_name': 'John'}).first()
    assert user.first_name == stored_user.first_name
    assert user.last_name == stored_user.last_name
    assert user.age == stored_user.age


def test_document_init_with_kwargs(clean_mongo):
    User = create_document_class('User', 'users')
    user = User(first_name='Pete', last_name='Doe', age=30)
    user.save()
    stored_user = User.find({'first_name': 'Pete'}).first()
    assert user.first_name == stored_user.first_name
    assert user.last_name == stored_user.last_name
    assert user.age == stored_user.age
    assert True


# def test_document_init_with_positional_arguments(clean_mongo):
#     assert True


# def test_document_init_with_invalid_arguments(clean_mongo):
#     assert True


def test_document_has_changed_with_no_changes(clean_mongo):
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user.save()
    assert not user.has_changed()


def test_document_has_changed_with_changes(clean_mongo):
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user.save()
    user.age += 1
    assert user.has_changed()


def test_document_has_changed_with_new_document(clean_mongo):
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})

    assert user.has_changed()


def test_document_is_saved_with_no_changes(clean_mongo):
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user.save()
    assert user.is_saved()

def test_document_is_saved_with_changes(clean_mongo):
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user.save()
    user.age += 1
    assert not user.is_saved()


def test_document_save_new_document(clean_mongo):
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user.save()
    stored_user = User.find({'first_name': 'John'}).first()
    assert user.first_name == stored_user.first_name
    assert user.last_name == stored_user.last_name
    assert user.age == stored_user.age


def test_document_save_existing_document_with_no_changes(clean_mongo):
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user.save()
    user.save()
    stored_user = User.find({'first_name': 'John'}).first()
    assert user.first_name == stored_user.first_name
    assert user.last_name == stored_user.last_name
    assert user.age == stored_user.age


def test_document_save_existing_document_with_changes(clean_mongo):
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user.save()
    user.age += 1
    user.save()
    stored_user = User.find({'first_name': 'John'}).first()
    assert user.first_name == stored_user.first_name
    assert user.last_name == stored_user.last_name
    assert user.age == stored_user.age


def test_document_reload_existing_document(clean_mongo):
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user.save()
    user.age += 1
    user.reload()
    assert user.age == 30


def test_document_reload_unsaved_document(clean_mongo):
    from mongeasy.exceptions import MongeasyDBDocumentError
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    with pytest.raises(MongeasyDBDocumentError):
        user.reload()

def test_document_delete_field(clean_mongo):
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user.save()
    user.delete_field('age')
    user.save()
    stored_user = User.find({'first_name': 'John'}).first()
    assert 'age' not in stored_user


def test_document_delete_existing_document(clean_mongo):
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user.save()
    user.delete()
    stored_user = User.find({'first_name': 'John'}).first()
    assert stored_user is None


def test_document_delete_unsaved_document(clean_mongo):
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user.delete()
    stored_user = User.find({'first_name': 'John'}).first()
    assert stored_user is None


def test_document_to_json(clean_mongo):
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user.save()
    json_user = user.to_json()
    assert isinstance(json_user, str)
    assert 'John' in json_user
    assert 'Doe' in json_user
    assert '30' in json_user
    assert str(user._id) in json_user


def test_document_get_by_id_with_valid_id(clean_mongo):
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user.save()
    stored_user = User.get_by_id(user._id)
    assert user.first_name == stored_user.first_name
    assert user.last_name == stored_user.last_name
    assert user.age == stored_user.age


def test_document_get_by_id_with_invalid_id(clean_mongo):
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user.save()
    stored_user = User.get_by_id('123')
    assert stored_user is None


def test_document_insert_many(clean_mongo):
    users = [
    {'first_name': 'Alice', 'last_name': 'Smith', 'age': 25},
    {'first_name': 'Bob', 'last_name': 'Jones', 'age': 35},
    {'first_name': 'Charlie', 'last_name': 'Brown', 'age': 45},
    {'first_name': 'Dave', 'last_name': 'Smith', 'age': 55}
]
    User = create_document_class('User', 'users')
    User.insert_many(users)
    stored_users = User.all()
    assert len(stored_users) == 4

def test_document_find(clean_mongo):
    User = create_document_class('User', 'users')
    user = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user.save()
    stored_user = User.find({'first_name': 'John'}).first()
    assert user.first_name == stored_user.first_name
    assert user.last_name == stored_user.last_name
    assert user.age == stored_user.age


def test_document_find_in(clean_mongo):
    User = create_document_class('User', 'users')
    user1 = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user1.save()
    user2 = User({'first_name': 'Alice', 'last_name': 'Smith', 'age': 25})
    user2.save()
    user3 = User({'first_name': 'Bob', 'last_name': 'Jones', 'age': 35})
    user3.save()
    stored_users = User.find_in('first_name', ['John', 'Bob'])
    assert len(stored_users) == 2
    assert user1.first_name in [user.first_name for user in stored_users]
    assert user2.first_name not in [user.first_name for user in stored_users]
    assert user3.first_name in [user.first_name for user in stored_users]


def test_document_all(clean_mongo):
    User = create_document_class('User', 'users')
    user1 = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user1.save()
    user2 = User({'first_name': 'Alice', 'last_name': 'Smith', 'age': 25})
    user2.save()
    user3 = User({'first_name': 'Bob', 'last_name': 'Jones', 'age': 35})
    user3.save()
    stored_users = User.all()
    assert len(stored_users) == 3
    assert user1.first_name in [user.first_name for user in stored_users]
    assert user2.first_name in [user.first_name for user in stored_users]
    assert user3.first_name in [user.first_name for user in stored_users]


def test_document_delete(clean_mongo):
    User = create_document_class('User', 'users')
    user1 = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user1.save()
    user2 = User({'first_name': 'Alice', 'last_name': 'Smith', 'age': 25})
    user2.save()
    user3 = User({'first_name': 'Bob', 'last_name': 'Jones', 'age': 35})
    user3.save()
    User.delete({'first_name': 'Alice'})
    stored_users = User.all()
    assert len(stored_users) == 2
    assert user1.first_name in [user.first_name for user in stored_users]
    assert user2.first_name not in [user.first_name for user in stored_users]
    assert user3.first_name in [user.first_name for user in stored_users]


def test_document_document_count(clean_mongo):
    User = create_document_class('User', 'users')
    user1 = User({'first_name': 'John', 'last_name': 'Doe', 'age': 30})
    user1.save()
    user2 = User({'first_name': 'Alice', 'last_name': 'Smith', 'age': 25})
    user2.save()
    user3 = User({'first_name': 'Bob', 'last_name': 'Jones', 'age': 35})
    user3.save()
    count = User.document_count()
    assert count == 3

