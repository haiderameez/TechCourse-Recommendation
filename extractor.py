from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

driver = webdriver.Chrome()

courses_data = []

try:
    driver.get('https://brainlox.com/courses/category/technical')

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'col-lg-6.col-md-12'))
    )

    course_sections = driver.find_elements(By.CLASS_NAME, 'col-lg-6')

    for section in course_sections:
        if "col-md-12" in section.get_attribute("class"):
            try:
                h3_element = section.find_element(By.TAG_NAME, 'h3')
                heading = h3_element.text.strip() if h3_element else "No Title"

                p_element = section.find_element(By.TAG_NAME, 'p')
                paragraph = p_element.text.strip() if p_element else "No Description"

                link_element = section.find_element(By.TAG_NAME, 'a')
                link = link_element.get_attribute('href') if link_element else "No Link"

                courses_data.append({
                    "title": heading,
                    "description": paragraph,
                    "link": link
                })

            except Exception as e:
                print(f"Error extracting data from a section: {e}")

finally:
    driver.quit()

with open("courses_data.json", "w", encoding="utf-8") as f:
    json.dump(courses_data, f, indent=4, ensure_ascii=False)

print("Data extraction complete. Saved to courses_data.json")