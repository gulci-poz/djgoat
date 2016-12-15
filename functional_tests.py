from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        # self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Janek wchodzi na stronę nowej aplikacji to-do
        self.browser.get('http://localhost:8000')

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
        inputbox.send_keys('Shoppping')

        # naciska ENTER, strona się uaktualnia i wyświetla wprowadzone zadanie
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        # szukamy wielu elementów, możemy dostać pustą listę
        # w przypadku metody bez "s" dostaniemy wyjątek
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Shopping' for row in rows),
            'New to-do item did not appear in table'
        )

        # oprócz tego wyświetlane jest pole do wprowadzenia kolejnego zadania
        # Janek wpisuje "Sprzątanie"

        # latarnia, mamy pewność, że do tego miejsca wszystko idzie dobrze
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main()
