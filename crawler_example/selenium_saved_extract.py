from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# init selenium
selenium_url = "http://sandbox-browser:4444/wd/hub"
chrome_options = Options()
driver = webdriver.Remote(
    command_executor=selenium_url,
    options=chrome_options
)

# open marketplace and wait for manual login
driver.get("https://www.facebook.com/marketplace")
wait = WebDriverWait(driver, 600) # wait max 10 minutes for login
print("Please manually log in via the browser windows")
wait.until(EC.invisibility_of_element_located((By.ID, "login_popup_cta_form")))

print("Login detected, proceeding...")


time.sleep(60) # sleep, in case of human check
print("sleep complete")


# open saved items page
driver.get("https://www.facebook.com/marketplace/you/saved")
print("opening saved items page")


# wait for page and listings to load
wait = WebDriverWait(driver, 15)
items_container = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='main']"))
)
print("page load wait complete")

time.sleep(10)
print("sleep complete")

# scroll to load all saved items
def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

print("scrolling to bottom of page")
scroll_to_bottom()

# locate saved items
print("locating saved items")
#items = driver.find_elements(By.CSS_SELECTOR, "div[style*='min-width: 242px'] > div > div > a[href*='/marketplace/item/']")
items = driver.find_elements(By.CSS_SELECTOR, "a[role='link'][href*='/marketplace/item/']")
print(f"Found {len(items)} saved items")
#saved_items = items_container.find_elements(By.CSS_SELECTOR, "a[role='link'][href*='/marketplace/item/']")
#print(f"Found {len(saved_items)} saved items")

# extract details from each item
print("extracting details from each item")
results = []
for item_link in items:
    try:
        url = item_link.get_attribute("href")
        
        # Image src
        img_el = item_link.find_element(By.TAG_NAME, "img")
        img_url = img_el.get_attribute("src") if img_el else None

        # Price: usually a span with dollar sign near the link root
        price_el = item_link.find_element(By.XPATH, ".//span[contains(text(), '$')]")
        price = price_el.text if price_el else "Unknown"

        # Title: from the span with the two-line clamp style (or fallback to text of link)
        # given your example: span with style -webkit-line-clamp: 2
        title_el = item_link.find_element(By.XPATH, ".//span[contains(@style, '-webkit-line-clamp: 2')]")
        title = title_el.text if title_el else item_link.text

        # Location: span near bottom (last span inside the link)
        # We look for span inside a div near the end with text (assuming location format)
        location_el = item_link.find_elements(By.XPATH, ".//span")[-1]
        location = location_el.text if location_el else "Unknown"

        results.append({
            "url": url,
            "image_url": img_url,
            "price": price,
            "title": title,
            "location": location
        })

    except Exception as e:
        print(f"Error processing item: {e}")
        continue

# print results
for result in results:
    print(f"---\n{result}\n---\n")




