from playwright.sync_api import sync_playwright
# в синхронной реализации меньше кода


def run(playwright):
    # необх создать экземпляр браузера с обязательным параметром по умолчанию headless=False
    browser = playwright.chromium.launch(headless=False)
    # в браузере создаем контекст
    context = browser.new_context()

    # Open new page
    page = context.new_page()
    # в результате получен объект page, с которым
    # будет дальнейшее взаимодействие

    # первое действие - открыть ссылку сайта
    # page.goto("http://127.0.0.1:8000/login/?next=/")
    page.goto("http://127.0.0.1:8000/login/")
    # кликнуть по input, чтобы сфокусироваться на нем,
    # в качестве аргумента указываем селектор
    # указывать этот клик не нужно, это сделает сам метод,
    # поэтому этот click удаляем
    page.click("input[name=\"username\"]")                              # удаляем

    # след шаг - вводим логин, затем с помощью Tab меняем фокус
    # Fill input[name="username"]
    page.fill("input[name=\"username\"]", "alice")

    # Press Tab
    # это действие в коде не нужно
    page.press("input[name=\"username\"]", "Tab")                       # удаляем

    # вводим пароль
    # Fill input[name="password"]                                         удаляем
    page.fill("input[name=\"password\"]", "Qamania123")

    # нажимаем Enter и осуществляем логин
    # Press Enter                                             удаляем
    page.press("input[name=\"username\"]", "Enter")
    # assert page.url == "http://127.0.0.1:8000/"             удаляем

    # Click text="Create new test"                            удаляем
    page.click("text=\"Create new test\"")
    # assert page.url == "http://127.0.0.1:8000/test/new"

    # Click input[name="name"]                                удаляем
    page.click("input[name=\"name\"]")                      # удаляем

    # Fill input[name="name"]                                 удаляем
    page.fill("input[name=\"name\"]", "hello")

    # Press Tab                                               удаляем
    page.press("input[name=\"name\"]", "Tab")               # удаляем

    # Fill textarea[name="description"]                       удаляем
    page.fill("textarea[name=\"description\"]", "world")

    # Click input[type="submit"]                              удаляем
    page.click("input[type=\"submit\"]")  # убираем
    # assert page.url == "http://127.0.0.1:8000/test/new"     удаляем

    # Click text="Test Cases"                                 удаляем
    page.click("text=\"Test Cases\"")
    # assert page.url == "http://127.0.0.1:8000/tests"        удаляем

    assert page.query_selector('//td[text()="hello"]') is not None

    # Click //tr//[13]/td[9]/button[normalize-space(.)='Delete']     # удаляем
    # page.click("//tr//[13]/td[9]/button[normalize-space(.)='Delete'")

    # Close page                                                удаляем
    page.close()

    # -----------------------                                   удаляем
    context.close()
    browser.close()


def test_new_testcase():
    with sync_playwright() as playwright:
        run(playwright)
