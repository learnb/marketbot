from selenium import webdriver
from selenium.webdriver.chrome.options import Options

selenium_url = "http://sandbox-browser:4444/wd/hub"

chrome_options = Options()

driver = webdriver.Remote(
    command_executor=selenium_url,
    options=chrome_options
)

driver.get("https://www.facebook.com/marketplace")
print(driver.title)