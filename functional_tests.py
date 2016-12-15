from selenium import webdriver

# if Firefox ESR is not the default Firefox
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# browser = webdriver.Firefox(firefox_binary=FirefoxBinary(firefox_path='c:\\firefox\\path'))

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title
