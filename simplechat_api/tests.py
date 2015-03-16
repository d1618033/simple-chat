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


class TestChat(SeleniumTests):
    def test_create_new_room(self):
        self.get(reverse("simplechat:index"))
        self.assertIn("Create a new room", self.get_text_body())
        self.selenium.find_element_by_id("create_new_room").click()
        self.selenium.implicitly_wait(3)
        self.selenium.find_element_by_id("new_room_link").click()
        self.assertEqual(resolve(self.unfix_url(self.selenium.current_url)).url_name, "room_detail")
