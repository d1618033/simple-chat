from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse, resolve
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


class SeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        firefox_binary = FirefoxBinary('/usr/bin/firefox')
        firefox_profile = FirefoxProfile("/home/david/.mozilla/firefox/btz4i8jg.Default User/")
        cls.selenium = webdriver.Firefox(firefox_binary=firefox_binary, firefox_profile=firefox_profile)
        super(SeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTests, cls).tearDownClass()

    def fix_url(self, url):
        return "{0}{1}".format(self.live_server_url, url)

    def unfix_url(self, url):
        return url.replace(self.live_server_url, '')

    def get(self, url):
        return self.selenium.get(self.fix_url(url))

    def get_text_body(self):
        return self.selenium.find_element_by_tag_name("body").text

    def assert_at_url_name(self, name):
        self.assertEqual(resolve(self.unfix_url(self.selenium.current_url)).url_name, name)

class TestChat(SeleniumTests):
    def open_create_new_page(self):
        self.get(reverse("simplechat:index"))

    def assert_at_create_new_room(self):
        self.assertIn("Welcome", self.get_text_body())

    def create_new_room(self):
        self.selenium.find_element_by_id("create_new_room_btn").click()

    def enter_name(self, name):
        self.selenium.find_element_by_id("id_name").send_keys(name)

    def enter_room(self):
        self.selenium.find_element_by_id("enter_room_btn").click()

    def assert_at_register(self):
        self.assert_at_url_name("room_register")
        self.assertIn("Please enter your nickname", self.get_text_body())

    def assert_at_room(self):
        self.assert_at_url_name("room_detail")
        self.assertRegex(self.get_text_body(), "Welcome to room \d+, \w+")

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

    def test_register_name_leads_to_room_page(self):
        self.open_create_new_page()
        self.create_new_room()
        self.enter_name("david")
        self.enter_room()
        self.assert_at_room()