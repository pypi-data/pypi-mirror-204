import json
import logging
import allure
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class BaseClass:
    """Класс базовых действий: подключение к БД, проверка наличия элемента """

    def __init__(self, browser, cursor, timeout=1):
        self.browser = browser
        self.cursor = cursor
        self.browser.implicitly_wait(timeout)
        self.logger = logging.getLogger(type(self).__name__)
        file_handler = logging.FileHandler("example_1.log")
        file_handler.setFormatter(logging.Formatter("[%(asctime)s: %(levelname)s] %(message)s"))
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.DEBUG)

    @allure.step("Open url: {url}")
    def open_page(self, url):
        """Открытие веб-страницы
        :param url: url страницы"""
        self.logger.info(F"Open url: {url}")
        self.browser.get(url)

    # БЛОК ПРОВЕРОК - ОБЕРТОК ЭЛЕМЕНТОВ------------------------------------------------------
    @allure.step("Check that element {locator} is present")
    def is_element_present(self, locator, timeout=1):
        """Проверка наличия элемента
        :param locator: локатор
        :param timeout: сколько времени ждать (1 секунда по умолчанию)
        """
        self.logger.info(f"Check that element {locator} is present")
        try:
            WebDriverWait(self.browser, timeout).until(ec.visibility_of_element_located(locator))
        except TimeoutException:
            self.get_screen()
            return False
        return True

    @allure.step("Check that element {locator} is not present")
    def is_element_not_present(self, locator, timeout=0.1):
        """Проверка отсутствия элемента
        :param locator: локатор
        :param timeout: таймер
        """
        self.logger.info(f"Check that element {locator} is not present")
        try:
            WebDriverWait(self.browser, timeout).until(ec.presence_of_element_located(locator))
        except TimeoutException:
            return True
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            attachment_type=allure.attachment_type.PNG,
            name='screen_image')
        return False

    @allure.step("Check that text on element {locator} is valid")
    def is_valid_text(self, locator, text, timeout=0.1):
        """Проверка на соответствие текста элемента (не введенного)
        :param locator: локатор
        :param text: текст для сравнения
        :param timeout: таймаут"""
        self.logger.info(f"Check that text on element {locator} is valid")
        try:
            WebDriverWait(self.browser, timeout).until(ec.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            self.get_screen()
            return False
        return True

    @allure.step("Validation of entered text {text} in an element {locator}")
    def is_text_entered(self, locator, text, timeout=0.2):
        """Проверка успешности ввода текста в элемент
        :param locator: локатор
        :param text: текст для сравнения
        :param timeout: таймаут"""
        self.logger.info(f"Validation of entered text {text} in an element {locator}")
        try:
            WebDriverWait(self.browser, timeout).until(ec.text_to_be_present_in_element_value(locator, text))
        except TimeoutException:
            self.get_screen()
            return False
        return True

    @allure.step("Check that element {locator} is not disabled (enabled)")
    def is_element_enabled(self, locator, timeout=0.1):
        """Проверка на то, что элемент не 'disabled'
        :param locator: локатор
        :param timeout: таймаут"""
        self.logger.info(f"Check that element {locator} is not disabled (enabled)")
        try:
            WebDriverWait(self.browser, timeout).until(ec.element_to_be_clickable(locator))
        except TimeoutException:
            self.get_screen()
            return False
        return True

    @allure.step("Check that element {locator} is disabled")
    def is_element_disabled(self, locator, timeout=0.1):
        """Проверка на то, что элемент 'disabled'
       :param locator: локатор
       :param timeout: таймаут"""
        self.logger.info(f"Check that element {locator} is disabled")
        try:
            WebDriverWait(self.browser, timeout).until(ec.element_to_be_clickable(locator))
        except TimeoutException:
            return True
        self.get_screen()
        return False

    @allure.step("Check that element {locator} is visible")
    def is_element_visible(self, locator, timeout=0.1):
        """ Проверка на то, что элемент видим (не только есть в DOM, но и имеет размер и визуально отображается)
        :param timeout: таймаут
        :param locator: локатор"""
        self.logger.info(f"Check that element {locator} is visible")
        try:
            WebDriverWait(self.browser, timeout).until(ec.visibility_of_element_located(locator))
        except TimeoutException:
            self.get_screen()
            return False
        return True

    @allure.step("Check that element {locator} is hidden")
    def is_element_hidden(self, locator, timeout=0.1):
        """ Проверка на то, что элемент не видим (есть в DOM, но визуально не отображается)
        :param timeout: таймаут
        :param locator: локатор"""
        self.logger.info(f"Check that element {locator} is hidden")
        try:
            WebDriverWait(self.browser, timeout).until(ec.invisibility_of_element_located(locator))
        except TimeoutException:
            self.get_screen()
            return False
        return True

    @allure.step("Click element {locator}")
    def click_element(self, locator):
        """Клик по элементу
        :param locator: локатор"""
        self.logger.info(f"Click element {locator}")
        element = self.browser.find_element(*locator)
        element.click()

    @allure.step("Input {value} in {locator}")
    def input_value(self, locator, value):
        """Ввод значения в элемент типа 'Поле ввода'
        :param locator: элемент, куда необходимо ввести
        :param value: значение, которое необходимо ввести"""
        self.logger.info(f"Input {value} in {locator}")
        input_field = self.browser.find_element(*locator)
        input_field.click()
        # input_field.clear()
        input_field.send_keys(Keys.SHIFT + Keys.HOME + Keys.DELETE)
        input_field.send_keys(value)

    @allure.step("Clean input field in {locator}")
    def clean_input_field(self, locator):
        """Очистка поля ввода элемента"""
        self.logger.info(f"Clean input field in {locator}")
        element = self.browser.find_element(*locator)
        len_str = len(element.get_attribute("value"))
        self.click_element(locator)
        element.send_keys(Keys.BACKSPACE * len_str)

    @allure.step("Get attribute {attribute} from {locator}")
    def get_value_from_attribute(self, locator, attribute):
        """Получение значения атрибута элемента
        :param locator: локатор
        :param attribute: аттрибут"""
        self.logger.info(f"Get attribute {attribute} from {locator}")
        element = self.browser.find_element(*locator)
        return element.get_attribute(attribute)

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    @allure.step("Write data {key}:{value} in {receiver}")
    def write_json_data(self, receiver, key, value):
        """Запись данных в json
        :param value: что необходимо записать
        :param receiver: приемник для записи данных
        :param key: ключ, который будет записан в паре с данными для записи на вход"""
        self.logger.info(f"Write data {key}:{value} in {receiver}")
        with open(receiver, encoding='utf8') as f:
            data_json = json.load(f)
            data_json[key] = value
        with open(receiver, 'w', encoding='utf8') as outfile:
            json.dump(data_json, outfile, ensure_ascii=False, indent=4)

    @allure.step("Read data from JSON file {source}")
    def read_json_data(self, source, key_name=None):
        """Чтение данных из json
        :param source: источник для чтения
        :param key_name: имя ключа. Если передается, то читаем значение этого ключа. Иначе возвращаем словарь"""
        # self.logger.info(f"Read data from JSON file {source}")
        with open(source, 'r', encoding='utf8') as f:
            data_json = json.load(f)
            for key, value in data_json.items():
                if key_name is not None:
                    if key == key_name:
                        return value
            else:
                return data_json

    @allure.step("Get 'username' from JSON file {data_file}")
    def get_username_from_data(self, data_file):
        """Получение имени пользователя из json-файла с подготовленными для теста данными
        :param data_file: источник для чтения"""
        self.logger.info(f"Get 'username' from JSON file {data_file}")
        return self.read_json_data(data_file, 'username')

    @allure.step("Get screen and attach to report")
    def get_screen(self):
        self.logger.info(f"Get screen and attach to report")
        allure.attach(body=self.browser.get_screenshot_as_png(),
                      attachment_type=allure.attachment_type.PNG,
                      name='screen_image')

    @allure.step("Get round {number}")
    def get_round(self, number):
        """Приведение числа в соответствии с его правилами приведения в АРМе. Если после зяпятой нули, то приводим
        число к целому. Иначе, округляем число до нужного количества знаков
        :param number: число, к которому будут применено округление"""
        self.logger.info(f"Get round {number}")
        if round(number) - number == 0:
            return round(number)
        elif round(number, 1) - number == 0:
            return round(number, 1)
        else:
            return round(number, 2)
