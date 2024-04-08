import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController

@pytest.fixture
def sut(users: list):
    magic_dao = mock.MagicMock()
    magic_dao.find.return_value = users #[{"email": "jane@doe.com"}]

    sut = UserController(dao = magic_dao)
    return sut

@pytest.mark.unit
@pytest.mark.parametrize('users, email, expected',[([{"email": "jane@doe.com"}], "Jane@doe.com", {"email": "jane@doe.com"}),
([{"email": "jane@doe.com", "Name": "Jane1"}, {"email": "jane@doe.com", "Name": "Jane2"}], "Jane@doe.com", {"email": "jane@doe.com", "Name": "Jane1"})
])
def test_getUserByEmail(sut, email, expected):
    # one user, more than one user
    result = sut.get_user_by_email(email)
    assert result == expected

@pytest.mark.unit
@pytest.mark.parametrize('users',[[{"email": "jane@doe.com"}]])
def test_invalid_email(sut):
    email = "jane-doe.com"

    with pytest.raises(ValueError):
        sut.get_user_by_email(email)


@pytest.mark.unit
@pytest.mark.parametrize('users',[[]])
def test_valid_email_no_user(sut):
    # no user should return None but give IndexError at the moment.
    email = "Jane@doe.com"
    result = sut.get_user_by_email(email)
    assert result == None


@pytest.mark.unit
@pytest.mark.parametrize('users',[Exception])
def test_valid_email_db_fail(sut):
    email = "Jane@doe.com"

    with pytest.raises(Exception):
        sut.get_user_by_email(email)
