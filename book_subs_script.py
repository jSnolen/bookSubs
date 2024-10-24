import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the path to your ChromeDriver
chromedriver_path = "C:/Users/jnole/Documents/chromedriver-win64/chromedriver.exe"

# Login credentials
username = "ENTER_USERNAME"
password = "ENTER_PASSWORD"

# Set up the Chrome driver service
service = Service(executable_path=chromedriver_path)

# Create a new Chrome session
driver = webdriver.Chrome(service=service)


def login():
    try:
        # Open the login page
        driver.get("https://spark.ignite-reading.com/")

        # Find username field and enter username
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#tutor_email"))
        )
        username_field.send_keys(username)

        # Find password field and enter password
        password_field = driver.find_element(By.CSS_SELECTOR, "#tutor_password")
        password_field.send_keys(password)

        # Find login button and click it
        login_button = driver.find_element(By.CSS_SELECTOR, "#new_tutor > div > div:nth-child(7) > input")
        login_button.click()

        # Print login attempted message
        print("Login attempted!")
    except Exception as e:
        print(f"Error during login: {e}")
        driver.quit()


def navigate_to_calendars():
    try:
        # Wait for the login process to complete and the next page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            'body > div:nth-child(2) > div.hidden.lg\\:flex.lg\\:w-64.lg\\:flex-col.lg\\:fixed.lg\\:inset-y-0 > div > div.flex-grow.mt-5.flex.flex-col > nav > a:nth-child(2)'))
        )

        # Find and click the button
        calendars_button = driver.find_element(By.CSS_SELECTOR,
                                               'body > div:nth-child(2) > div.hidden.lg\\:flex.lg\\:w-64.lg\\:flex-col.lg\\:fixed.lg\\:inset-y-0 > div > div.flex-grow.mt-5.flex.flex-col > nav > a:nth-child(2)')
        calendars_button.click()

        # Wait for the 'Calendar View' text to be clickable, and then click it
        calendar_view = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Calendar View']"))
        )
        calendar_view.click()

        # Wait for a few seconds (change the seconds if needed)
        time.sleep(3)

        # Wait for the 'Open Sub Opportunities' text to be clickable, and then click it
        open_sub_opportunities = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Open Sub Opportunities']"))
        )
        open_sub_opportunities.click()
    except Exception as e:
        print(f"Error during navigation: {e}")
        driver.quit()


def process_opportunities():
    wait = WebDriverWait(driver, 10)
    try:
        three_pm_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '3 PM')]"))
        )
        three_pm_position = three_pm_element.location['y']
        print("3 PM found.")
    except Exception as e:
        print(f"3 PM not found or error: {e}")
        driver.quit()
        return

    claim_clicks = 0
    while True:
        time.sleep(1)
        sub_opportunities = driver.find_elements(By.XPATH, "//*[contains(text(),'Sub Opportunity')]")
        if sub_opportunities and claim_clicks < 4:
            for sub in sub_opportunities:
                sub_position = sub.location['y']
                if sub_position < three_pm_position:
                    sub.click()
                    time.sleep(1)
                    claims = driver.find_elements(By.XPATH, "//*[contains(text(),'Claim')]")
                    if claims:
                        claims[0].click()
                        claim_clicks += 1
                        time.sleep(1)
                        break
        else:
            driver.refresh()
            time.sleep(1)

        if claim_clicks >= 1:
            print("Claim attempted!")
            break


try:
    login()
    navigate_to_calendars()
    process_opportunities()
finally:
    time.sleep(10)
    driver.quit()
