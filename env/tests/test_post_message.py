import json
import pytest
import allure
from requests.auth import HTTPBasicAuth

from Lib.assertions import Asseretions
from Lib.base_case import BaseCase
from Lib.my_requests import MyRequests
from tests.test_get_list_message import TestReceivingList


@allure.epic("Проверка на внесения в API сообщения")
class TestAddNewMessage(BaseCase):

    @pytest.fixture
    def auth1(self):
        return HTTPBasicAuth("Ivan141", "123")

    @pytest.fixture
    def auth2(self):
        return HTTPBasicAuth("Ivan14", "123")

    @staticmethod
    def values():
        with open(r"C:\Work\Liis\project\env\tests\value_for_message\values_for_post_test.txt", 'r', encoding='utf-8') as f:
            data = f.read()
            return json.loads(data)

    @allure.description("Проверка на внесения в API нового сообщения")
    @pytest.mark.parametrize("values", values())
    def test_add_new_message(self, values, auth1):
        url = "v1/api/ivanovas19681/posts"
        response = MyRequests.post(url, json=values, auth=auth1)
        Asseretions.assert_code_status(response, 201)

        TestReceivingList().test_get_list_message()  # Здесь проходят проверки того как в каком виде сообщения отображаются в базе
        TestReceivingList().test_message_id_unique()
        TestReceivingList().test_message_format_data()

        id_list = [] # Здесь происходит удаления всех добавленниыйх сообщений по id
        id_list.append(response.json()["id"])
        for id in id_list:
            MyRequests.delete(f"v1/api/ivanovas19681/post/{id}", auth=auth1)
            response2 = MyRequests.get(f"v1/api/ivanovas19681/post/{id}")
            assert response2.status_code == 404, "Удаления по id не состоялось"

    @staticmethod
    def values2():
        with open(r"C:\Work\Liis\project\env\tests\value_for_message\values_for_post_stress_test.txt", 'r',
                  encoding='utf-8') as f:
            data = f.read()
            return json.loads(data)

    @allure.description("Стресс тест на внесение большого кол-во сообщений одним разом")
    @pytest.mark.parametrize("value", values2())
    def test_add_new_message_stress(self, value, auth1):
        response = MyRequests.post("v1/api/ivanovas19681/posts", json=value, auth=auth1)
        Asseretions.assert_code_status(response, 201)

        id_list = []
        id_list.append(response.json()["id"])
        for id in id_list:
            MyRequests.delete(f"v1/api/ivanovas19681/post/{id}", auth=auth1)
            response2 = MyRequests.get(f"v1/api/ivanovas19681/post/{id}")
            assert response2.status_code == 404, "Удаления по id не состоялось"

    @allure.description("Проверка на внесение данных c авторизацией с одного аккаунта, последующим удалением с другого")
    @pytest.mark.parametrize("value", values())
    def test_add_new_book_invalid(self, value, auth2, auth1):
        response = MyRequests.post("v1/api/ivanovas19681/posts", json=value, auth=auth2)
        Asseretions.assert_code_status(response, 201)

        id_list = []
        id_list.append(response.json()["id"])
        for id in id_list:
            MyRequests.delete(f"v1/api/ivanovas19681/post/{id}", auth=auth1)
            response2 = MyRequests.get(f"v1/api/ivanovas19681/post/{id}")
            assert response2.status_code == 200, "Удаления сообщения с другого аккаунта состоялось"