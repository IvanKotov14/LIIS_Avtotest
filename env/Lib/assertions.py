from requests import Response
import json


class Asseretions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expented_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не в Json формате. Ответ текста '{response.text}'"
        assert name in response_as_dict, f"Ответ Json не содержит ключ 'name'"
        assert response_as_dict[name] == expented_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не в Json формате. Ответ текста '{response.text}'"
        assert name in response_as_dict, f"Ответ Json не содержит ключ '{name}'"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, f"Ответ статус кода {response.status_code}, не соответсвует ожидаемому {expected_status_code}"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            json_obj = response.json()
        except json.JSONDecodeError:
            raise AssertionError("JSON ответ не в формате")

        if isinstance(json_obj, list):
            for key in names:
                if key not in json_obj[0]:
                    raise AssertionError(f"Ключ {key} отсутствует в JSON ответе")
        else:
            for key in names:
                if key not in json_obj:
                    raise AssertionError(f"Ключ {key} отсутствует в JSON ответе")

    @staticmethod
    def assert_json_value_is_number(response: Response, key: str):
        try:
            json_obj = response.json()
        except json.JSONDecodeError:
            raise AssertionError("JSON ответ не в формате")

        if isinstance(json_obj, list):
            for obj in json_obj:
                if not isinstance(obj[key], int):
                    raise AssertionError(f"Значение ключа '{key}' не является числом")
        else:
            if not isinstance(json_obj[key], int):
                raise AssertionError(f"Значение ключа '{key}' не является числом")


