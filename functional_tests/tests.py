from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys


class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        # jeśli używamy liveserver, to atrybut live_server_url nie istnieje
        # (pochodzi on z pakietu do testowania)
        if hasattr(cls, 'live_server_url'):
            if cls.server_url == cls.live_server_url:
                super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        # błąd w Windows nie ustępuje po dodaniu refresh
        # self.browser.refresh()
        # na liverver w ubuntu błąd nie występuje
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Janek wchodzi na stronę nowej aplikacji to-do
        self.browser.get(self.server_url)

        # dostrzega w tytule strony i nagłówku, że jest to aplikacja to-do
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # jest proszony o wprowadzenie nowego zadania do wykonania
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # wpisuje "Shopping"
        inputbox.send_keys('Shopping')

        # naciska ENTER, strona się uaktualnia i wyświetla wprowadzone zadanie
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Shopping')

        # oprócz tego wyświetlane jest pole do wprowadzenia kolejnego zadania
        # Janek wpisuje "Sprzątanie"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Sprzątanie')
        inputbox.send_keys(Keys.ENTER)

        # na stronie widzimy dwa nowe elementy dodane przez Janka
        self.check_for_row_in_list_table('1: Shopping')
        self.check_for_row_in_list_table('2: Sprzątanie')

    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.server_url)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Ubieranie choinki')
        inputbox.send_keys(Keys.ENTER)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Porządki w szafie')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Ubieranie choinki')
        self.check_for_row_in_list_table('2: Porządki w szafie')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.server_url)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Ubieranie choinki')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Ubieranie choinki')

        # Janek zastanawia się, czy jego lista zostanie zapamiętana
        # Janek widzi unikalny url

        janek_list_url = self.browser.current_url
        self.assertRegex(janek_list_url, '/lists/.+')

        # # nowa sesja przeglądarki dla kolejnego użytkownika - Wojtka
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Wojtek odwiedza stronę
        self.browser.get(self.server_url)

        # # sprawdzamy, czy Wojtek widzi pozycje listy Janka

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Ubieranie choinki', page_text)

        # Wojtek dodaje nowy element

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Umyć samochód')
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Umyć samochód')

        # Wojtek zastanawia się, czy jego lista zostanie zapamiętana
        # Wojtek widzi unikalny url

        wojtek_list_url = self.browser.current_url
        self.assertRegex(wojtek_list_url, '/lists/.+')

        # # porównyjemy URL-e list Janka i Wojtka
        self.assertNotEqual(janek_list_url, wojtek_list_url)

        # # sprawdzenie zawartości bieżącej listy,
        # # czy nie zawiera elementów poprzedniej listy
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Ubieranie choinki', page_text)
        self.assertIn('Umyć samochód', page_text)

    def test_layout_and_styling(self):
        # Janek uruchamia stronę startową
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # dostrzega wyśrodkowany inputbox
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # Janek wpisuje zadanie tworząc tym samym nową listę,
        # po zaakceptowaniu widzi wyśrodkowany inputbox

        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # self.fail('Finish the test!')
