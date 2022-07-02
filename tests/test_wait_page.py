import allure

@allure.title('test for wait more than 30 sec')
def test_wait_more_30_sec(desktop_app_auth):
    desktop_app_auth.navigate_to("Demo pages")
    desktop_app_auth.demo_pages.open_page_after_wait(32)
    assert desktop_app_auth.demo_pages.check_wait_page()


