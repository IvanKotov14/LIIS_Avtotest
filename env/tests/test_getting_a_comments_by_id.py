from Lib.assertions import Asseretions

from Lib.base_case import BaseCase
from Lib.my_requests import MyRequests
import allure
from tests.test_get_list_comments import TestReceivingListComments


@allure.epic("Проверка получения сообщения по id")
class TestGettingCommentsById(BaseCase):
    @allure.description("Проверка на наличия полей в запросе по id всех сообщения")
    def test_get_comments_id(self):
        all_id = TestReceivingListComments().test_get_list_comments()
        for number in all_id:
            url = f"v1/api/ivanovas19681/comment/{number}"
            response = MyRequests.get(url)
            Asseretions.assert_code_status(response, 200)
            Asseretions.assert_json_has_keys(response, ["author", "title", "content", "id", "publication_datetime", "post"])

    @allure.description("Проверка соответсвия формата заполненых данных в запросе по id")
    def test_comments_by_id_format_data(self):
        all_id = TestReceivingListComments().test_get_list_comments()
        for number in all_id:
            url = f"v1/api/ivanovas19681/comment/{number}"
            response = MyRequests.get(url)
            Asseretions.assert_json_value_is_number(response, "id")
            Asseretions.assert_json_value_is_number(response, "author")

    @allure.description("Проверка, что значения поля id в ответе соотвествует запрашиваемому id")
    def test_comments_match_id_fields(self):
        all_id = TestReceivingListComments().test_get_list_comments()
        for number in all_id:
            url = f"v1/api/ivanovas19681/comment/{number}"
            response = MyRequests.get(url)
            assert number == response.json()["id"], "Поле id в запросе сообщения по id, не совпадает с номером " \
                                                            "его вызова"