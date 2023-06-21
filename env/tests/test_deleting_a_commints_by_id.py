import pytest
from requests.auth import HTTPBasicAuth

from Lib.assertions import Asseretions

from Lib.base_case import BaseCase
from Lib.my_requests import MyRequests
import allure
import random

from tests.test_get_list_message import TestReceivingList


@allure.epic("Проверка удаления сообщения")
class TestDeletingMessageById(BaseCase):

    def setup_method(self):
        self.post = TestReceivingList().test_get_list_message()

    @pytest.fixture
    def auth1(self):
        return HTTPBasicAuth("Ivan141", "123")

    @allure.description("Проверка на создания и удаления сообщения")
    def test_deleting_message(self, auth1):
        selected_post = random.choice(self.post)
        values = {
            "title": "yournewpostdsadsadsadsadasname",
            "content": "yournewpostcontent",
            "post": selected_post
        }
        response = MyRequests.post("v1/api/ivanovas19681/comments", json=values, auth=auth1)
        Asseretions.assert_code_status(response, 201)
        id_from_make_book = response.json()["id"]
        response2 = MyRequests.delete(f"v1/api/ivanovas19681/comment/{id_from_make_book}", auth=auth1)
        Asseretions.assert_code_status(response2, 204)
        response3 = MyRequests.get(f"v1/api/ivanovas19681/comment/{id_from_make_book}")
        Asseretions.assert_code_status(response3, 404)