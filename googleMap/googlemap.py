from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
headers_csv = ['Hospital_name', 'Hospital_Url', 'Hospital_rating', 'Hospital_reviews', 'Hospital_Address', 'Contact_no']
csvfile = open('Hospitals_Data_Google_Map.csv', 'w', newline='', encoding='utf-8-sig')
writer = csv.DictWriter(csvfile, fieldnames=headers_csv)
if csvfile.tell() == 0:
    writer.writeheader()
    csvfile.flush()



# Set up Selenium webdriver
driver = webdriver.Chrome( )  # Replace with the path to your chromedriver executable

# Open Google Maps
driver.get('https://www.google.com/maps')

Place = driver.find_element_by_class_name('searchboxinput')
Place.send_keys("Hospitals in Lahore")
submit = driver.find_element_by_id('searchbox-searchbutton')
submit.click()


# Wait for search results to load
driver.implicitly_wait(10)


# Extract hospital data
# OLD_totL_LENGTH = len(hospital_elements)
old_hospital_elements = []
while True:
    new_hospital_elements = old_hospital_elements + [v.get_attribute('href') for v in driver.find_elements(By.CSS_SELECTOR, 'a.hfpxzc')]
    for element in driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK'):
        item = dict()
        try:
            item['Hospital_name'] = element.find_element(By.CSS_SELECTOR, 'div.qBF1Pd').text
        except:
            pass
        try:
            item['Hospital_Url'] = element.find_element(By.CSS_SELECTOR, 'a.hfpxzc').get_attribute('href')
        except:
            pass
        try:
            item['Hospital_rating'] = element.find_element(By.CSS_SELECTOR, 'span.MW4etd').text
        except:
            pass
        try:
            item['Hospital_reviews'] = element.find_element(By.CSS_SELECTOR, 'span.UY7F9').text.replace('(', '').replace(')', '')
        except:
            pass
        try:
            item['Hospital_Address'] = "".join(element.find_element(By.CSS_SELECTOR, 'div > div > div.UaQhfb.fontBodyMedium > div:nth-child(4) > div.W4Efsd').text)
        except:
            pass
        try:
            item['Contact_no'] = element.find_element(By.CSS_SELECTOR, ' div > div.UaQhfb.fontBodyMedium > div:nth-child(4) > div:nth-child(2) > span:nth-child(2) > span:nth-child(2)').text
        except:
            pass
        # print(f"Hospital_name: {Hospital_name}")
        # print(f"Hospital_Url: {Hospital_Url}")
        # print(f"Hospital_rating: {Hospital_rating}")
        # print(f"Hospital_reviews: {Hospital_reviews}")
        # print(f"Address: {address}")
        # print(f"Contact_no: {Contact_no}")
        writer.writerow(item)
        csvfile.flush()

    hospital_element_scroll = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK')[-1]
    driver.execute_script("arguments[0].scrollIntoView(true);", hospital_element_scroll)
    time.sleep(5)

    old_hospital_elements = old_hospital_elements + [v.get_attribute('href') for v in driver.find_elements(By.CSS_SELECTOR, 'a.hfpxzc')]

    if len(old_hospital_elements) == len(new_hospital_elements):
        break

# Close the browser
driver.quit()