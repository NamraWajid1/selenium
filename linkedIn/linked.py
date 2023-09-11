from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#Creating CSV File
import csv
headers_csv = ['Job_Title', 'Company_Name', 'Company_Link', 'Job_Location', 'Employment_type', 'Job_function', 'Industries', 'Applicants']
csvfile = open('LinkedIn_Jobs.csv', 'w', newline='', encoding='utf-8-sig')
writer = csv.DictWriter(csvfile, fieldnames=headers_csv)
if csvfile.tell() == 0:
    writer.writeheader()
    csvfile.flush()

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# All links are in links.txt file
data_file = open("links.txt", "r")
all_urls = data_file.readlines()
data_file.close()
for i in list(set(all_urls)):
    driver.get(i)
    time.sleep(3)

# Scrolling at the end of the page
n = 1000
i = 2
while i <= int((n + 200) / 25) + 1:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    i = i + 1

    try:
        send = driver.find_element(By.XPATH, "//button[@aria-label='See more jobs']")
        driver.execute_script("arguments[0].click();", send)
        time.sleep(3)

    except:
        pass
        time.sleep(5)


# Extracting Data
jobs_block = driver.find_elements(By.XPATH, "//ul[@class='jobs-search__results-list']/li")
for job in jobs_block:
    item = dict()
    try:
        item['Job_Title'] = job.find_element(By.CSS_SELECTOR, " div.base-search-card__info > h3").text
    except:
        pass
    try:
        item['Company_Name'] = job.find_element(By.CSS_SELECTOR, " div.base-search-card__info > h4 > a").text
    except:
        pass
    try:
        item['Company_Link'] = job.find_element(By.CSS_SELECTOR, " div.base-search-card__info > h4 > a").get_attribute('href')
    except:
        pass
    try:
        item['Job_Location'] = job.find_element(By.CSS_SELECTOR, " div > span.job-search-card__location").text
    except:
        pass
    try:
        job.click()
        time.sleep(3)
    except:
        pass
    try:
        item['Employment_type'] = driver.find_element(By.CSS_SELECTOR," div > section.core-section-container.my-3.description > div > ul > li:nth-child(2) > span").text
    except:
        pass
    try:
        item['Job_function'] = driver.find_element(By.CSS_SELECTOR," div > section.core-section-container.my-3.description > div > ul > li:nth-child(3) > span").text
    except:
        pass
    try:
        item['Industries'] = driver.find_element(By.CSS_SELECTOR,"div > section.core-section-container.my-3.description > div > ul > li:nth-child(4) > span").text
    except:
        pass
    try:
        try:
            item['Applicants'] = driver.find_element(By.CSS_SELECTOR,"body > div.base-serp-page > div > section > div.details-pane__content.details-pane__content--show > section > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div > h4 > div:nth-child(2) > figure > figcaption").text
        except:
            item['Applicants'] = driver.find_element(By.CSS_SELECTOR," body > div.base-serp-page > div > section > div.details-pane__content.details-pane__content--show > section > div > div.top-card-layout__entity-info-container.flex.flex-wrap.papabear\:flex-nowrap > div > h4 > div:nth-child(2) > span.num-applicants__caption.topcard__flavor--metadata.topcard__flavor--bullet").text
    except:
        pass


# Printing Data As well as storing in CSV
    print(item)
    writer.writerow(item)
    csvfile.flush()

    driver.back()
    time.sleep(2)

driver.quit()