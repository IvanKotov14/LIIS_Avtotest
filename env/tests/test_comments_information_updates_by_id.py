import pytest
from requests.auth import HTTPBasicAuth

from Lib.assertions import Asseretions

from Lib.base_case import BaseCase
from Lib.my_requests import MyRequests
import allure
import random

from tests.test_get_list_comments import TestReceivingListComments
from tests.test_get_list_message import TestReceivingList


@allure.epic("Проверка исправления книги")
class TestUpdatesCommentsById(BaseCase):

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

    @allure.description("Проверка на создание и исправление сообщения")
    @pytest.mark.parametrize("title, content", value)
    def test_updates_comments(self, title, content, auth1):
        selected_post = random.choice(self.post)
        values = {
            "title": title,
            "content": content
        }
        values2 = {
            "title": "yournewpostdsadsadsadsadasname",
            "content": "yournewpostcontent",
            "post": selected_post
        }
        response = MyRequests.post("v1/api/ivanovas19681/comments", json=values2, auth=auth1)
        Asseretions.assert_code_status(response, 201)
        id_from_make_book = response.json()["id"]
        response2 = MyRequests.put(f"v1/api/ivanovas19681/comment/{id_from_make_book}", json=values, auth=auth1)
        Asseretions.assert_code_status(response2, 200)
        Asseretions.assert_json_value_by_name(response2, "message", "updated", "Метод Put не исправил значения")
        Asseretions.assert_json_value_by_name(response2, "type", "success", "Метод Put не исправил значения")
        response3 = MyRequests.get(f"v1/api/ivanovas19681/comment/{id_from_make_book}")
        Asseretions.assert_json_value_by_name(response3, "title", title, "Метод Put не исправил значения")
        Asseretions.assert_json_value_by_name(response3, "content", content, "Метод Put не исправил значения")
        MyRequests.delete(f"v1/api/ivanovas19681/comment/{id_from_make_book}", auth=auth1)
        response2 = MyRequests.get(f"v1/api/ivanovas19681/comment/{id_from_make_book}")
        assert response2.status_code == 404, "Удаления по id не состоялось"

    @allure.description("Проверка на создание и исправление в коментариях")
    @pytest.mark.parametrize("title, content", value)
    def test_updates_comments_invalid(self, title, content, auth2, auth1):
        selected_post = random.choice(self.post)
        values = {
            "title": title,
            "content": content
        }
        values2 = {
            "title": "yournewpostdsadsadsadsadasname",
            "content": "yournewpostcontent",
            "post": selected_post
        }
        response = MyRequests.post("v1/api/ivanovas19681/comments", json=values2, auth=auth1)
        Asseretions.assert_code_status(response, 201)
        id_from_make_book = response.json()["id"]
        response2 = MyRequests.put(f"v1/api/ivanovas19681/{id_from_make_book}", json=values, auth=auth2)
        Asseretions.assert_code_status(response2, 404)
        MyRequests.delete(f"v1/api/ivanovas19681/comment/{id_from_make_book}", auth=auth1)
        response2 = MyRequests.get(f"v1/api/ivanovas19681/comment/{id_from_make_book}")
        assert response2.status_code == 404, "Удаления по id не состоялось"

