import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the path to your ChromeDriver
chromedriver_path = "C:/Users/jnole/OneDrive/Documents/chromedriver-win64/chromedriver.exe"

# Set up the Chrome driver service
service = Service(executable_path=chromedriver_path)

# Create a new Chrome session
driver = webdriver.Chrome(service=service)


def read_confidential():
    username = os.getenv('COMPANY_LOGIN_EMAIL')
    password = os.getenv('COMPANY_LOGIN_PASSWORD')
    company_website = os.getenv('COMPANY_WEBSITE')
    return username, password, company_website


def login():
    username, password, company_website = read_confidential()
    try:
        # Open the login page
        driver.get(company_website)

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


def set_range():
    wait = WebDriverWait(driver, 10)

    try:
        nine_am_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '9 AM')]"))
        )
        nine_am_position_min = nine_am_element.location['y']
        print("9 AM found.")

    except Exception as e:
        print(f"9 AM not found or error: {e}")
        driver.quit()
        return

    try:
        three_pm_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '3 PM')]"))
        )
        three_pm_position_max = three_pm_element.location['y']
        print("3 PM found.")
    except Exception as e:
        print(f"3 PM not found or error: {e}")
        driver.quit()
        return

    return nine_am_position_min, three_pm_position_max


def process_opportunities(nine_am_position, three_pm_position):
    claim_clicks = 0
    while True:
        time.sleep(2)
        sub_opportunities = driver.find_elements(By.XPATH, "//*[contains(text(),'Sub Opportunity')]")
        if sub_opportunities and claim_clicks < 3:
            for sub in sub_opportunities:
                sub_position = sub.location['y']
                if nine_am_position < sub_position < three_pm_position:
                    print(f"Sub opportunity found at position: {sub_position}")
                    try:
                        sub.click()
                        time.sleep(1)
                    except Exception as e:
                        print(f"There was an issue with the click: {e}")
                        error_messages = [
                            "Another tutor has already claimed this session.",
                            "There was an error claiming this session."
                        ]
                        for message in error_messages:
                            elements = driver.find_elements(By.XPATH, f"//*[contains(text(),'{message}')]")
                            if elements:
                                print(message)
                                break

                    claims = driver.find_elements(By.XPATH, "//*[contains(text(),'Claim')]")
                    if claims:
                        claims[0].click()
                        print("Claim attempted!")
                        claim_clicks += 1
                        time.sleep(1)

                        error_messages = [
                            "Another tutor has already claimed this session.",
                            "There was an error claiming this session."
                        ]
                        for message in error_messages:
                            elements = driver.find_elements(By.XPATH, f"//*[contains(text(),'{message}')]")
                            if elements:
                                print(message)
                                break

                        try:
                            nine_am_element = wait.until(
                                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '9 AM')]"))
                            )
                            nine_am_position = nine_am_element.location['y']
                            print("9 AM found.")
                        except Exception as e:
                            print(f"9 AM not found or error: {e}")
                            driver.quit()
                            return

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
                        break
                    break
        else:
            driver.refresh()
            time.sleep(1)


try:
    login()
    navigate_to_calendars()
    min_position, max_position = set_range()
    process_opportunities(min_position, max_position)
finally:
    time.sleep(10)
    driver.quit()
