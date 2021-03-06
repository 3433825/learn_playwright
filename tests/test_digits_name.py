def test_new_testcase_digits_name(desktop_app_auth):
    test_name = '123'
    desktop_app_auth.navigate_to('Create new test')
    desktop_app_auth.create_test(test_name, 'digits')
    desktop_app_auth.navigate_to('Test Cases')
    assert desktop_app_auth.test_cases.check_test_exists(test_name)
    desktop_app_auth.test_cases.delete_test_by_name(test_name)