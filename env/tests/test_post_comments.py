import pytest
import allure
from requests.auth import HTTPBasicAuth
import random

from Lib.assertions import Asseretions
from Lib.base_case import BaseCase
from Lib.my_requests import MyRequests
from tests.test_get_list_message import TestReceivingList

@allure.epic("Проверка на внесения в API коментария")
class TestAddNewComments(BaseCase):
    def setup_method(self):
        self.post = TestReceivingList().test_get_list_message()

    @pytest.fixture
    def auth1(self):
        return HTTPBasicAuth("Ivan141", "123")

    @pytest.fixture
    def auth2(self):
        return HTTPBasicAuth("Ivan14", "123")

    with open(r"C:\Work\Liis\project\env\tests\value_for_comments\values_for_put_test_comments.txt", 'r', encoding='utf-8') as f:
        value = eval(f.read())

    @allure.description("Проверка на создание и исправление коментария")
    @pytest.mark.parametrize("title, content", value)
    def test_add_new_comments(self, title, content, auth1):
        selected_post = random.choice(self.post)
        values = {
            "title": title,
            "content": content,
            "post": selected_post
        }
        url = "v1/api/ivanovas19681/comments"
        response = MyRequests.post(url, json=values, auth=auth1)
        Asseretions.assert_code_status(response, 201)
        id_list = [] # Здесь происходит удаления всех добавленниыйх сообщений по id
        id_list.append(response.json()["id"])
        for id in id_list:
            MyRequests.delete(f"v1/api/ivanovas19681/comment/{id}", auth=auth1)
            response2 = MyRequests.get(f"v1/api/ivanovas19681/comment/{id}")
            assert response2.status_code == 404, "Удаления по id не состоялось"

    @allure.description("Проверка на внесение данных c авторизацией с одного аккаунта, последующим удалением с другого")
    @pytest.mark.parametrize("title, content", value)
    def test_add_new_comments_invalid(self, title, content, auth1, auth2):
        selected_post = random.choice(self.post)
        values = {
            "title": title,
            "content": content,
            "post": selected_post
        }
        response = MyRequests.post("v1/api/ivanovas19681/comments", json=values, auth=auth1)
        Asseretions.assert_code_status(response, 201)

        id_list = []
        id_list.append(response.json()["id"])
        for id in id_list:
            MyRequests.delete(f"v1/api/ivanovas19681/comment/{id}", auth=auth2)
            response2 = MyRequests.get(f"v1/api/ivanovas19681/comment/{id}")
            assert response2.status_code == 200, "Удаления сообщения с другого аккаунта состоялось"