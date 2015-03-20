from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse, resolve
from selenium import webdriver
import time


class SeleniumTests(LiveServerTestCase):
    windows = []

    @classmethod
    def setUpClass(cls):
        cls.selenium = cls.new_window()
        super(SeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        for window in cls.windows:
            window.quit()
        super(SeleniumTests, cls).tearDownClass()

    @classmethod
    def new_window(cls):
        window = webdriver.Firefox()
        cls.windows.append(window)
        return window

    def fix_url(self, url):
        return "{0}{1}".format(self.live_server_url, url)

    def unfix_url(self, url):
        return url.replace(self.live_server_url, '')

    def get(self, url, window=None):
        return self.get_window(window).get(self.fix_url(url))

    def get_text_body(self, window=None):
        return self.get_window(window).find_element_by_tag_name("body").text

    def assert_at_url_name(self, name, window=None):
        self.assertEqual(resolve(self.unfix_url(self.get_window(window).current_url)).url_name, name)

    def get_window(self, window):
        if window is None:
            return self.selenium
        else:
            return window

    def wait(self, seconds):
        time.sleep(seconds)


class ChatTestCase(SeleniumTests):
    def open_create_new_page(self, window=None):
        self.get(reverse("simplechat:index"), window)

    def assert_at_create_new_room(self, window=None):
        self.assertIn("Welcome", self.get_text_body(window))

    def create_new_room(self, window=None):
        self.get_window(window).find_element_by_id("create_new_room_btn").click()

    def enter_name(self, name, window=None):
        self.get_window(window).find_element_by_id("id_name").send_keys(name)

    def enter_room(self, window=None):
        self.get_window(window).find_element_by_id("enter_room_btn").click()

    def assert_at_register(self, window=None):
        self.assert_at_url_name("room_register", window)
        self.assertIn("Please enter your nickname", self.get_text_body(window))

    def assert_at_room(self, window=None):
        self.assert_at_url_name("room_detail", window)
        self.assertRegex(self.get_text_body(window), "Welcome to room \d+, \w+")

    def get_items_in_list(self, list_elem):
        return [li.text for li in list_elem.find_elements_by_tag_name("li")]

    def get_errors(self, window=None):
        return self.get_items_in_list(self.get_window(window).find_element_by_class_name("errorlist"))

    def assert_has_errors(self, errors, window=None):
        self.assertEqual(self.get_errors(window), errors)

    def post_message(self, message, window=None):
        elem = self.get_window(window).find_element_by_id("message")
        elem.clear()
        elem.send_keys(message)
        self.get_window(window).find_element_by_id("message-send-btn").click()

    def adjust_message(self, message_dict):
        return "[{0}]: {1}".format(message_dict['user'], message_dict['message'])

    def get_messages(self, window=None):
        return self.get_items_in_list(self.get_window(window).find_element_by_id("message_list"))

    def assert_messages_are(self, expected_message_list, window=None):
        actual_message_list = self.get_messages(window)
        expected_message_list = [self.adjust_message(message) for message in expected_message_list]
        self.assertEqual(actual_message_list, expected_message_list)

    def assert_no_messages(self, window=None):
        self.assertEqual(len(self.get_messages(window)), 0)


class TestChat(ChatTestCase):
    def test_create_new_room(self):
        self.open_create_new_page()
        self.assert_at_create_new_room()
        self.create_new_room()
        self.assert_at_register()

    def test_register_empty_name_doesnt_work(self):
        self.open_create_new_page()
        self.create_new_room()
        self.enter_room()
        self.assert_at_register()
        self.assert_has_errors(["This field is required."])

    def test_register_name_leads_to_room_page(self):
        self.open_create_new_page()
        self.create_new_room()
        self.enter_name("david")
        self.enter_room()
        self.assert_at_room()

    def test_post_message_in_room(self):
        self.open_create_new_page()
        self.create_new_room()
        self.enter_name("david")
        self.enter_room()
        self.assert_no_messages()
        self.post_message("hello")
        messages = []
        messages.append({
            "user": "david",
            "message": "hello",
        })
        self.assert_messages_are(messages)
        self.post_message("again")
        messages.append({
            "user": "david",
            "message": "again",
        })
        self.assert_messages_are(messages)
