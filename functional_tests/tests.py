from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Janek wchodzi na stronę nowej aplikacji to-do
        self.browser.get(self.live_server_url)

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

        # Janek zastanawia się, czy jego lista zostanie zapamiętana
        # Janek widzi unikalny url

        # latarnia, mamy pewność, że do tego miejsca wszystko idzie dobrze
        self.fail('Finish the test!')
