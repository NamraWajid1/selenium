from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

# Create a new instance of the Firefox driver
driver = webdriver.Chrome('/Users/HP/Downloads/chromedriver')

# Open Google Maps
driver.get("https://www.google.com/maps")

# Find and interact with the search input field
search_input = driver.find_element(By.ID, "searchboxinput")
search_input.send_keys("hospitals in Lahore")

search_input = driver.find_element_by_id('searchbox-searchbutton')
search_input.click()

# Find and interact with the map element
map_element = driver.find_element(By.ID, "pane")
action_chains = ActionChains(driver)
action_chains.move_to_element(map_element).perform()

# Define the maximum number of scroll attempts
max_attempts = 5

# Define the scroll threshold (percentage of the viewport height)
scroll_threshold = 0.8

# Define the search result CSS class or ID (specific to Google Maps)
result_selector = "a.hfpxzc"

# Track the current map viewport
current_viewport = None

# Perform vertical scrolling until the condition is met or the maximum attempts are reached
scroll_attempts = 0
while scroll_attempts < max_attempts:
    # Scroll down by pressing the arrow-down key (adjust as needed)
    ActionChains(driver).key_down("\ue015").key_up("\ue015").perform()

    # Wait for the new search results to load or for the scroll to complete
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, result_selector)))

    # Get the updated map viewport
    updated_viewport = driver.execute_script("return arguments[0].getBoundingClientRect();", map_element)
    time.sleep(5)

    # Check if the scroll progress exceeds the threshold or if the viewport remains the same
    if current_viewport is not None and updated_viewport == current_viewport:
        break  # Exit the loop if the viewport remains the same
    elif current_viewport is not None:
        scroll_progress = (updated_viewport["top"] + updated_viewport["height"]) / driver.get_window_size()["height"]
        if scroll_progress >= scroll_threshold:
            break  # Exit the loop if the threshold is reached

    current_viewport = updated_viewport
    scroll_attempts += 1
for element in driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK'):
        try:
            Hospital_name = element.find_element(By.CSS_SELECTOR, 'div.qBF1Pd').text
        except:
            pass
        try:
            Hospital_Url = element.find_element(By.CSS_SELECTOR, 'a.hfpxzc').get_attribute('href')
        except:
            pass
        try:
            Hospital_rating = element.find_element(By.CSS_SELECTOR, 'span.MW4etd').text
        except:
            pass
        try:
            Hospital_reviews = element.find_element(By.CSS_SELECTOR, 'span.UY7F9').text.replace('(', '').replace(')', '')
        except:
            pass
        try:
             address = "".join(element.find_element(By.CSS_SELECTOR, 'div > div > div.UaQhfb.fontBodyMedium > div:nth-child(4) > div.W4Efsd').text)
        except:
            pass
        try:
            Contact_no = element.find_element(By.CSS_SELECTOR, ' div > div.UaQhfb.fontBodyMedium > div:nth-child(4) > div:nth-child(2) > span:nth-child(2) > span:nth-child(2)').text
        except:
            pass
        print(f"Hospital_name: {Hospital_name}")
        print(f"Hospital_Url: {Hospital_Url}")
        print(f"Hospital_rating: {Hospital_rating}")
        print(f"Hospital_reviews: {Hospital_reviews}")
        print(f"Address: {address}")
        print(f"Contact_no: {Contact_no}")

# Perform further actions after scrolling
# ...
