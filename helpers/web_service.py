import requests
import re

class WebService:
    def __init__(self, base_url:str):
        self.session = requests.session()
        self.base_url = base_url

    def _get_token(self, url: str):
        # открываем веб-стр для получения токена
        rsp = self.session.get(self.base_url + url)
        # поиск токена на странице
        # первый аргумент - выражение, которое будем искать
        # второй - весь контент страницы
        match = re.search('<input type="hidden" name="csrfmiddlewaretoken" value="(.+?)">', rsp.text)
        if match:
            # если нашли - создаем объект
            return match.group(1)
        else:
            # если нет - фейлим создание объекта
            assert False, 'failed to get token'

    def login(self, login: str, password: str):
        token = self._get_token('/login/')
        data = {
            'username': login,
            'password': password,
            'csrfmiddlewaretoken': token
        }
        self.session.post(self.base_url + '/login/', data=data)

    def create_test(self, test_name: str, test_description: str):
        token = self._get_token('/test/new')
        data = {
            'name': test_name,
            'description': test_description,
            'csrfmiddlewaretoken': token
        }
        self.session.post(self.base_url + '/test/new', data=data)

    def close(self):
        self.session.close()


