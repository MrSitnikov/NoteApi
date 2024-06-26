import pytest
from tests.init_test import client, application, auth_headers, user_admin
from api.models.user import UserModel


@pytest.fixture()
def user():
    user_data = {"username": "testuser", "password": "1234"}
    user = UserModel(**user_data)
    user.save()
    return user


def test_user_get_by_id(client, user):
    response = client.get('/users/1')
    assert response.status_code == 200
    assert response.json["username"] == user.username
    #assert len(response.json)  == 3
    assert response.json["role"] in ('admin','simple_user')


def test_user_not_found(client, user):
    response = client.get('/users/2')
    assert response.status_code == 404


def test_user_creation(client):
    user_data = {
        "username": 'admin',
        'password': 'admin',
        'role':'admin'
    }
    response = client.post('/users',
                           json=user_data,
                           content_type='application/json')
    data = response.json
    assert response.status_code == 201
    assert 'admin' in data.values()


#@pytest.mark.skip(reason="test not finished")
def test_user_creation_already_exist(client, user):
    """
    Тест на создание пользователя с существующим именем
    """
    # 1. Используя фикстуру user - создаем пользователя с "username": "testuser"
    # 2. Отправляем put запрос на создание пользователя с таким же username
    user_data = {"username": "testuser", "password": "1234"}
    response = client.post('/users', json=user_data, content_type='application/json')
    assert response.status_code == 409
    # DONE: допишите тест и запустите его, убрав декоратор @pytest.mark.skip



def test_user_edit(client, user, auth_headers):
    user_edited_data = {
        "username": "new_name"
    }
    response = client.put(f'/users/{user.id}',
                          json=user_edited_data,
                          headers=auth_headers)
    data = response.json
    assert response.status_code == 200
    assert data["username"] == user_edited_data["username"]


#@pytest.mark.skip(reason="test not implemented")
def test_user_delete(client, user, auth_headers):
    response = client.delete(f'/users/{user.id}', headers=auth_headers)
    assert response.status_code == 200
    response = client.delete(f'/users/100', headers=auth_headers)
    assert response.status_code == 404
    #DONE: реализуйте тест на удаление пользователя и запустите его, убрав декоратор @pytest.mark.skip
