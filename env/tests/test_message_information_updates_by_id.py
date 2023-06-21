import json

import pytest
from requests.auth import HTTPBasicAuth

from Lib.assertions import Asseretions

from Lib.base_case import BaseCase
from Lib.my_requests import MyRequests
import allure

from tests.test_get_list_message import TestReceivingList


@allure.epic("Проверка исправления книги")
class TestUpdatesMessageById(BaseCase):

    @pytest.fixture
    def auth1(self):
        return HTTPBasicAuth("Ivan141", "123")

    @pytest.fixture
    def auth2(self):
        return HTTPBasicAuth("Ivan14", "123")

    with open(r"C:\Work\Liis\project\env\tests\value_for_message\values_for_put_test_massage.txt", 'r', encoding='utf-8') as f:
        value = eval(f.read())

    @allure.description("Проверка на создание и исправление сообщения")
    @pytest.mark.parametrize("title, content", value)
    def test_updates_message(self, title, content, auth1):
        values = {
            "title": title,
            "content": content
        }
        values2 = {
            "title": "yournewpostdsadsadsadsadasname",
            "content": "yournewpostcontent"
        }
        response = MyRequests.post("v1/api/ivanovas19681/posts", json=values2, auth=auth1)
        Asseretions.assert_code_status(response, 201)
        id_from_make_book = response.json()["id"]
        response2 = MyRequests.put(f"v1/api/ivanovas19681/post/{id_from_make_book}", json=values, auth=auth1)
        Asseretions.assert_code_status(response2, 200)
        Asseretions.assert_json_value_by_name(response2, "message", "updated", "Метод Put не исправил значения")
        Asseretions.assert_json_value_by_name(response2, "type", "success", "Метод Put не исправил значения")
        response3 = MyRequests.get(f"v1/api/ivanovas19681/post/{id_from_make_book}")
        Asseretions.assert_json_value_by_name(response3, "title", title, "Метод Put не исправил значения")
        Asseretions.assert_json_value_by_name(response3, "content", content, "Метод Put не исправил значения")
        TestReceivingList().test_get_list_message()
        MyRequests.delete(f"v1/api/ivanovas19681/post/{id_from_make_book}", auth=auth1)
        response2 = MyRequests.get(f"v1/api/ivanovas19681/post/{id_from_make_book}")
        assert response2.status_code == 404, "Удаления по id не состоялось"

    @allure.description("Проверка на создание и исправление сообщения")
    @pytest.mark.parametrize("title, content", value)
    def test_updates_message_invalid(self, title, content, auth2, auth1):
        values = {
            "title": title,
            "content": content
        }
        values2 = {
            "title": "yournewpostdsadsadsadsadasname",
            "content": "yournewpostcontent"
        }
        response = MyRequests.post("v1/api/ivanovas19681/posts", json=values2, auth=auth1)
        Asseretions.assert_code_status(response, 201)
        id_from_make_book = response.json()["id"]
        response2 = MyRequests.put(f"v1/api/ivanovas19681/post/{id_from_make_book}", json=values, auth=auth2)
        Asseretions.assert_code_status(response2, 403)
        MyRequests.delete(f"v1/api/ivanovas19681/post/{id_from_make_book}", auth=auth1)
        response2 = MyRequests.get(f"v1/api/ivanovas19681/post/{id_from_make_book}")
        assert response2.status_code == 404, "Удаления по id не состоялось"

