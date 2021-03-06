from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse, resolve
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from simplechat.models import Participant, Room
import re


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

    def tearDown(self):
        self.close_extra_windows()

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

    def assert_in_body_regex(self, text, window=None):
        self.assertRegex(self.get_text_body(window), text)

    def assert_in_body(self, text, window=None):
        self.assertIn(text, self.get_text_body(window))

    def get_window(self, window):
        if window is None:
            return self.selenium
        else:
            return window

    @classmethod
    def close_extra_windows(cls):
        for window in cls.windows[1:]:
            window.quit()
        cls.windows = [cls.windows[0]]


class ChatTestCase(SeleniumTests):
    def open_create_new_room_page(self, window=None):
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
        self.assert_in_body_regex("Please enter your nickname\s*Name:", window)

    def assert_at_room(self, window=None, name=None):
        self.assert_at_url_name("room_detail", window)
        if name is None:
            pattern = "Welcome to room \d+, .+"
        else:
            pattern = "Welcome to room \d+, {0}".format(re.escape(name))
        self.assert_in_body_regex(pattern, window)

    def get_li_elems_in_list(self, list_elem):
        return list_elem.find_elements_by_tag_name("li")

    def get_text_in_elems(self, elems):
        return [e.text for e in elems]

    def get_items_in_list(self, list_elem):
        return self.get_text_in_elems(self.get_li_elems_in_list(list_elem))

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

    def get_messages(self, window=None, expected_number=None, max_timeout=10):
        return self.get_items_with_delay(
            lambda driver: driver.find_element_by_id("message_list"),
            window=window,
            expected_number=expected_number,
            max_timeout=max_timeout,
        )

    def get_items_with_delay(self, func, window=None, expected_number=None, max_timeout=10):
        def condition(driver):
            li_elems = self.get_li_elems_in_list(func(driver))
            if len(li_elems) == expected_number:
                return self.get_text_in_elems(li_elems)

        if expected_number is None:
            return self.get_items_in_list(func(self.get_window(window)))
        else:
            return WebDriverWait(self.get_window(window), max_timeout).until(condition)

    def assert_messages_are(self, expected_message_list, window=None):
        actual_message_list = self.get_messages(window, expected_number=len(expected_message_list), max_timeout=10)
        expected_message_list = [self.adjust_message(message) for message in expected_message_list]
        self.assertEqual(actual_message_list, expected_message_list)

    def assert_no_messages(self, window=None):
        self.assertRaises(TimeoutException, self.get_messages, window, expected_number=1)
        self.assertEqual(len(self.get_messages(window)), 0)

    def assert_participants_are(self, expected, wait_for=None, window=None):
        if wait_for is not None:
            self.assertRaises(TimeoutException, self.get_participants, window, expected_number=wait_for, max_timeout=10)
        actual = self.get_participants(
            window,
            expected_number=len(expected),
            max_timeout=10
        )
        self.assertEqual(sorted(actual), sorted(expected))

    def get_participants(self, window=None, expected_number=None, max_timeout=10):
        return self.get_items_with_delay(
            lambda driver: driver.find_element_by_id("people_list"),
            window=window,
            expected_number=expected_number,
            max_timeout=max_timeout,
        )

    def enter_user_into_current_room(self, name, window=None):
        second_window = self.new_window()
        second_window.get(self.get_window(window).current_url)
        self.assert_at_register(second_window)
        self.enter_name(name, second_window)
        self.enter_room(second_window)
        return second_window

    def logout(self, window=None):
        self.get_window(window).find_element_by_id("logout").click()

    def create_and_enter_user_into_room(self, name, window=None):
        self.open_create_new_room_page(window)
        self.create_new_room(window)
        self.enter_name(name, window)
        self.enter_room(window)


class TestChat(ChatTestCase):
    def test_create_new_room(self):
        self.open_create_new_room_page()
        self.assert_at_create_new_room()
        self.create_new_room()
        self.assert_at_register()

    def test_register_empty_name_doesnt_work(self):
        self.create_and_enter_user_into_room("")
        self.assert_at_register()
        self.assert_has_errors(["This field is required."])

    def test_register_name_leads_to_room_page(self):
        self.create_and_enter_user_into_room("david")
        self.assert_at_room(name="david")

    def test_post_message_in_room(self):
        self.create_and_enter_user_into_room("david")
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

    def test_post_messages_multiple_users(self):
        self.create_and_enter_user_into_room("david")
        self.assert_no_messages()
        self.post_message("hello")
        second_window = self.enter_user_into_current_room("bro")
        messages = []
        messages.append({
            "user": "david",
            "message": "hello",
        })
        self.assert_messages_are(messages, second_window)
        self.post_message("goodbye", second_window)
        messages.append({
            "user": "bro",
            "message": "goodbye",
        })
        self.assert_messages_are(messages, second_window)
        self.assert_messages_are(messages)

    def test_participant_list(self):
        participants = []
        self.create_and_enter_user_into_room("david")
        participants.append("david")
        self.assert_participants_are(participants)
        second_window = self.enter_user_into_current_room("bro")
        participants.append("bro")
        self.assert_participants_are(participants, second_window)
        self.assert_participants_are(participants)
        third_window = self.enter_user_into_current_room("dude")
        participants.append("dude")
        self.assert_participants_are(participants, third_window)
        self.assert_participants_are(participants)
        self.assert_participants_are(participants, second_window)
        self.logout(second_window)
        self.assert_at_create_new_room(second_window)
        participants.remove("bro")
        self.assert_participants_are(participants)
        self.assert_participants_are(participants, third_window)

    def test_not_allowed_to_post_in_someone_elses_name(self):
        self.create_and_enter_user_into_room("david")
        second_window = self.enter_user_into_current_room("bro")
        third_window = self.enter_user_into_current_room("dude")
        room = Room.objects.all().order_by('-pk')[0]
        participant = Participant.objects.all().order_by('-pk')[1]
        url = reverse("simplechat_api:message-list")
        room_pk = room.pk
        participant_pk = participant.pk
        script = '$.post("{0}", {{room: {1}, participant: {2}, message: "hahahahah"}})'.format(url, room_pk,
                                                                                             participant_pk)
        self.selenium.execute_script(script)
        # david posts a message in bro's name.
        # david will see the message as his
        # bro will not see the message because it's supposedly his
        # dude will see the message as if bro posted it
        # what should actually happen is that none of the windows should see any message
        self.assert_no_messages(third_window)
        self.assert_no_messages(second_window)
        self.assert_no_messages()

    def test_not_allowed_to_logout_in_someone_elses_name(self):
        self.create_and_enter_user_into_room("david")
        second_window = self.enter_user_into_current_room("bro")
        self.assert_participants_are(["david", "bro"])
        self.assert_participants_are(["david", "bro"], window=second_window)
        pk = Participant.objects.latest('pk').pk
        self.selenium.execute_script(
            '$.ajax({{url: "{0}",method: "delete"}})'
            ''.format(reverse("simplechat_api:participant-detail", args=(pk, )))
        )
        self.assert_participants_are(["david", "bro"], wait_for=1)
        self.assert_participants_are(["david", "bro"], window=second_window, wait_for=1)

    def test_xss_in_messages(self):
        self.create_and_enter_user_into_room("david")
        self.post_message("<script>location.href='{0}';</script>".format(reverse("simplechat:index")))
        self.assert_at_room(name="david")

    def test_xss_in_username(self):
        name = "<script>location.href='{0}';</script>".format(reverse("simplechat:index"))
        self.create_and_enter_user_into_room(name)
        self.assert_at_room(name=name)

    def test_no_double_escaping_messages(self):
        self.create_and_enter_user_into_room("dude")
        self.post_message("<")
        self.assert_messages_are([{"user": "dude", "message": "<"}])