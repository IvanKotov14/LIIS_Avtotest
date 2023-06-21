import json

from Lib.assertions import Asseretions

from Lib.base_case import BaseCase
from Lib.my_requests import MyRequests
import allure


@allure.epic("Проверка получения списка всех комментариев")
class TestReceivingListComments(BaseCase):

    list_all_id = []

    @allure.description("Проверка наличия всех полей у комментарий")
    def test_get_list_comments(self):
        url = "v1/api/ivanovas19681/comments"
        response = MyRequests.get(url)
        Asseretions.assert_code_status(response, 200)
        Asseretions.assert_json_has_keys(response, ["author", "title", "content", "id", "publication_datetime", "post"])
        response_data = json.loads(response.text)
        self.__class__.list_all_id = [book["id"] for book in response_data]

        return self.list_all_id

    @allure.description("Проверка, что сообщение имеет уникальный id у комментарие")
    def test_comments_id_unique(self):
        assert len(set(self.list_all_id)) == len(self.list_all_id), "Найдены дубликаты id"

    @allure.description("Проверка соответсвия формата заполненых данных у коментариев")
    def test_comments_format_data(self):
        url = "v1/api/ivanovas19681/comments"
        response = MyRequests.get(url)
        Asseretions.assert_json_value_is_number(response, "id")
        Asseretions.assert_json_value_is_number(response, "author")
        Asseretions.assert_json_value_is_number(response, "post")