from selenium import webdriver

browser = webdriver.Firefox()

# jeśli Firefox ESR nie jest domyślnym Firefoksem
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# browser = webdriver.Firefox(firefox_binary=FirefoxBinary(firefox_path='c:\\firefox\\path'))

# Janek wchodzi na stronę nowej aplikacji to-do
browser.get('http://localhost:8000')

# dostrzega w tytule strony, że jest to aplikacja to-do
assert 'To-Do' in browser.title, "Browser title was " + browser.title

browser.quit()
