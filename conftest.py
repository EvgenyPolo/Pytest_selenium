import pytest
import uuid
from selenium import webdriver
from settings import driver_chrome, driver_firefox


# @pytest.fixture(autouse=True)
@pytest.fixture()
def browser_driver_firefox():
    pytest.driver = webdriver.Firefox(executable_path=driver_firefox)

    yield pytest.driver

    pytest.driver.quit()


# @pytest.fixture(autouse=True)
@pytest.fixture()
def browser_driver_chrome():
    pytest.driver = webdriver.Chrome(executable_path=driver_chrome)
    # pytest.driver = webdriver.Chrome(executable_path=path_by_driver+'\chromedriver.exe')

    yield pytest.driver

    pytest.driver.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield

    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    return rep


@pytest.fixture
def web_browser(request, browser_driver_chrome):
    # def web_browser(request, selenium):

    browser = browser_driver_chrome
    browser.set_window_size(1360, 768)

    # Return browser instance to test case:
    yield browser

    # Do teardown (this code will be executed after each test):

    if request.node.rep_call.failed:
        # Make the screen-shot if test failed:
        try:
            browser.execute_script("document.body.bgColor = 'white';")

            # Make screen-shot for local debug:
            browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

            # For happy debugging:
            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)

        except:
            print('Что-то пошло не так!!!')
            pass  # just ignore any errors here
