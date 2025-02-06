import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load existing JSON data
with open("courses_data.json", "r", encoding="utf-8") as f:
    courses_data = json.load(f)

# Initialize Selenium WebDriver
driver = webdriver.Chrome()

try:
    for course in courses_data:
        course_link = course.get("link", "")
        if not course_link:
            continue  # Skip if no link is present

        driver.get(course_link)
        time.sleep(3)  # Allow time for the page to load

        try:
            # Wait for the content inside the target class to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "react-tabs__tab-panel--selected"))
            )

            # Find the target class
            panel = driver.find_element(By.CLASS_NAME, "react-tabs__tab-panel--selected")

            # Extract all paragraph texts
            paragraphs = panel.find_elements(By.TAG_NAME, "p")
            extracted_text = [p.text.strip() for p in paragraphs if p.text.strip()]

            # Update the JSON with the extracted details
            course["details"] = extracted_text

        except Exception as e:
            print(f"Error scraping {course_link}: {e}")
            course["details"] = "Failed to extract details"

finally:
    driver.quit()

# Save updated JSON file
with open("courses_data.json", "w", encoding="utf-8") as f:
    json.dump(courses_data, f, indent=4, ensure_ascii=False)

print("Scraping complete. Updated data saved to courses_data.json")
