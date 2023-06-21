import json

from Lib.assertions import Asseretions

from Lib.base_case import BaseCase
from Lib.my_requests import MyRequests
import allure


@allure.epic("Проверка получения списка всех сообщений")
class TestReceivingList(BaseCase):

    list_all_id = []

    @allure.description("Проверка наличия всех полей у сообщений")
    def test_get_list_message(self):
        url = "v1/api/ivanovas19681/posts"
        response = MyRequests.get(url)
        Asseretions.assert_code_status(response, 200)
        Asseretions.assert_json_has_keys(response, ["author", "title", "content", "id", "publication_datetime"])
        response_data = json.loads(response.text)
        self.__class__.list_all_id = [book["id"] for book in response_data]

        return self.list_all_id

    @allure.description("Проверка, что сообщение имеет уникальный id у сообщений")
    def test_message_id_unique(self):
        assert len(set(self.list_all_id)) == len(self.list_all_id), "Найдены дубликаты id"

    @allure.description("Проверка соответсвия формата заполненых данных у сообщений")
    def test_message_format_data(self):
        url = "v1/api/ivanovas19681/posts"
        response = MyRequests.get(url)
        Asseretions.assert_json_value_is_number(response, "id")
        Asseretions.assert_json_value_is_number(response, "author")
