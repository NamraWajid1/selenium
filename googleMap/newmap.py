from selenium import webdriver
from selenium.webdriver.common.by import By
import time
# Set up Selenium webdriver
driver = webdriver.Chrome('/Users/HP/Downloads/chromedriver')  # Replace with the path to your chromedriver executable

# Open Google Maps
driver.get('https://www.google.com/maps')

Place = driver.find_element_by_class_name('searchboxinput')
Place.send_keys("Hospitals in Lahore")
submit = driver.find_element_by_id('searchbox-searchbutton')
submit.click()


# Wait for search results to load
driver.implicitly_wait(10)

# container = driver.find_elements(By.CSS_SELECTOR, 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd ')
# print(container)
# Extract hospital data


# OLD_totL_LENGTH = len(hospital_elements)
old_hospital_elements = []
while True:
    new_hospital_elements = old_hospital_elements + [v.get_attribute('href') for v in driver.find_elements(By.CSS_SELECTOR, 'a.hfpxzc')]
    for element in driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK'):
        try:
            Hospital_name = element.find_element(By.CSS_SELECTOR, 'div.qBF1Pd').text
        except:
            pass
        Hospital_Url = element.find_element(By.CSS_SELECTOR, 'a.hfpxzc').get_attribute('href')
        Hospital_rating = element.find_element(By.CSS_SELECTOR, 'span.MW4etd').text
        Hospital_reviews = element.find_element(By.CSS_SELECTOR, 'span.UY7F9').text.replace('(', '').replace(')', '')
        address = "".join(element.find_element(By.CSS_SELECTOR, 'div > div > div.UaQhfb.fontBodyMedium > div:nth-child(4) > div.W4Efsd').text)
        # Contact_no = element.find_element(By.CSS_SELECTOR, 'div.UaQhfb.fontBodyMedium > div:nth-child(4) > div:nth-child(2) > span:nth-child(2) > span:nth-child(2)').text

        print(f"Hospital_name: {Hospital_name}")
        print(f"Hospital_Url: {Hospital_Url}")
        print(f"Hospital_rating: {Hospital_rating}")
        print(f"Hospital_reviews: {Hospital_reviews}")
        print(f"Address: {address}")

    hospital_element_scroll = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK')[-1]
    driver.execute_script("arguments[0].scrollIntoView(true);", hospital_element_scroll)
    time.sleep(5)

    old_hospital_elements = old_hospital_elements + [v.get_attribute('href') for v in driver.find_elements(By.CSS_SELECTOR, 'a.hfpxzc')]

    if len(old_hospital_elements) == len(new_hospital_elements):
        break

    # print(f"Contact_no: {Contact_no}")
#
#     print()
# # Close the browser
# driver.quit()