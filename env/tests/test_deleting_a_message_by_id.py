import pytest
from requests.auth import HTTPBasicAuth

from Lib.assertions import Asseretions

from Lib.base_case import BaseCase
from Lib.my_requests import MyRequests
import allure

from tests.test_get_list_message import TestReceivingList


@allure.epic("Проверка удаления сообщения")
class TestDeletingMessageById(BaseCase):

    @pytest.fixture
    def auth1(self):
        return HTTPBasicAuth("Ivan141", "123")

    @allure.description("Проверка на создания и удаления сообщения")
    def test_deleting_message(self, auth1):
        values = {
            "title": "yournewpostdsadsadsadsadasname",
            "content": "yournewpostcontent"
        }
        response = MyRequests.post("v1/api/ivanovas19681/posts", json=values, auth=auth1)
        Asseretions.assert_code_status(response, 201)
        TestReceivingList().test_get_list_message()  # Здесь проходят проверки того как в каком ввиде книги внеслись в базу
        id_from_make_book = response.json()["id"]
        response2 = MyRequests.delete(f"v1/api/ivanovas19681/post/{id_from_make_book}", auth=auth1)
        Asseretions.assert_code_status(response2, 204)
        response3 = MyRequests.get(f"v1/api/ivanovas19681/post/{id_from_make_book}")
        Asseretions.assert_code_status(response3, 404)