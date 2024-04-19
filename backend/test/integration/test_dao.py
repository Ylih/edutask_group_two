import pytest
from unittest.mock import patch
from pymongo.errors import WriteError
from src.util.dao import DAO

@pytest.fixture
def sut():
    with patch('src.util.dao.getValidator', autospec=True) as mockedValidator:
        mockedValidator.return_value = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["userName", "email"],
                "properties": {
                    "userName": {
                        "bsonType": "string",
                        "description": "the username of a user must be determined"
                    },
                    "userHobbies": {
                        "bsonType": "string",
                        "description": "the hobbies of a user are optional",
                    },
                    "email": {
                        "bsonType": "string",
                        "description": "the email address of a user must be determined",
                        "uniqueItems": True
                    }
                }
            }
        }

        sut = DAO("test")

        yield sut

        #teardown
        sut.drop()


@pytest.mark.integration
def test_dao_create_success(sut):
    data = {
            "userName": "jan3",
            "email": "jane@mail.com"
    }
    result = sut.create(data)
    assert result.keys() == {'_id', 'userName', 'email'}

@pytest.mark.integration
def test_missing_required_properties_dao_create(sut):
    data = {
            "email": "john@mail.com",
            "userHobbies": "coffee drinking"
    }
    with pytest.raises(WriteError):
        sut.create(data)

@pytest.mark.integration
def test_false_bson_type_dao_create(sut):
    data = {
            "userName": False,
            "email": "john@mail.com"
    }
    with pytest.raises(WriteError):
        sut.create(data)

@pytest.mark.integration
def test_no_uniqueItems_dao_create(sut):
    # user with same email already exists see test above
    data = {
            "userName": "Jane",
            "email": "jane@mail.com"
    }

    sut.create(data)
    with pytest.raises(WriteError):
        sut.create(data)