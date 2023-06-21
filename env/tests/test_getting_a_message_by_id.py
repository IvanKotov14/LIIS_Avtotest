from Lib.assertions import Asseretions

from Lib.base_case import BaseCase
from Lib.my_requests import MyRequests
import allure
from tests.test_get_list_message import TestReceivingList


@allure.epic("Проверка получения сообщения по id")
class TestGettingMessageById(BaseCase):
    @allure.description("Проверка на наличия полей в запросе по id всех сообщения")
    def test_get_message_id(self):
        all_id = TestReceivingList().test_get_list_message()
        for number in all_id:
            url = f"v1/api/ivanovas19681/post/{number}"
            response = MyRequests.get(url)
            Asseretions.assert_code_status(response, 200)
            Asseretions.assert_json_has_keys(response, ["author", "title", "content", "id", "publication_datetime"])

    @allure.description("Проверка соответсвия формата заполненых данных в запросе по id")
    def test_message_by_id_format_data(self):
        all_id = TestReceivingList().test_get_list_message()
        for number in all_id:
            url = f"v1/api/ivanovas19681/post/{number}"
            response = MyRequests.get(url)
            Asseretions.assert_json_value_is_number(response, "id")
            Asseretions.assert_json_value_is_number(response, "author")

    @allure.description("Проверка, что значения поля id в ответе соотвествует запрашиваемому id")
    def test_message_match_id_fields(self):
        all_id = TestReceivingList().test_get_list_message()
        for number in all_id:
            url = f"v1/api/ivanovas19681/post/{number}"
            response = MyRequests.get(url)
            assert number == response.json()["id"], "Поле id в запросе сообщения по id, не совпадает с номером " \
                                                            "его вызова"