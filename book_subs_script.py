import time
import os
from selenium import webdriver
from selenium.common import NoSuchElementException
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
        try:
            calendars_button = driver.find_element(By.CSS_SELECTOR,
                                               'body > div:nth-child(2) > div.hidden.lg\\:flex.lg\\:w-64.lg\\:flex-col.lg\\:fixed.lg\\:inset-y-0 > div > div.flex-grow.mt-5.flex.flex-col > nav > a:nth-child(2)')
            calendars_button.click()
        except NoSuchElementException:
            print("Calendars button not found. Trying alternative selector.")
            try:
                # Fallback: Use provided CSS selector to locate and click the alternative element
                alternative_element = driver.find_element(By.CSS_SELECTOR,
                                                      "body > div:nth-child(2) > div.lg\\:pl-64 > div.lg\\:hidden.sticky.top-0.bg-white.flex.items-center.w-full.py-2.px-1.md\\:px-3.border-b.z-40 > div.absolute > button > svg > path")
                alternative_element.click()
                print("Alternative element clicked successfully.")

                # Click the next element after the alternative element
                next_element = driver.find_element(By.CSS_SELECTOR,
                                               "body > div:nth-child(2) > div.relative.z-50.lg\\:hidden > div.fixed.inset-0.flex.max-h-screen > div.relative.max-w-xs.w-full.bg-white.pt-5.pb-4.flex-1.flex.flex-col > div.mt-2.flex.flex-col.overflow-y-auto.grow > div > nav > a.bg-gray-100.text-gray-900.group.rounded-md.py-2.px-2.flex.items-center.text-sm.font-medium")
                next_element.click()
                print("Next element clicked successfully.")
            except NoSuchElementException:
                print("Alternative element or next element not found.")
                driver.quit()
                return

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



    claim_clicks = 0
    while True:
        time.sleep(1)
        sub_opportunities = driver.find_elements(By.XPATH, "//*[contains(text(),'Sub Opportunity')]")
        if sub_opportunities and claim_clicks <= 2:
            for sub in sub_opportunities:
                sub_position = sub.location['y']
                if nine_am_position < sub_position < three_pm_position:
                    print(f"Sub opportunity found at position: {sub_position}")
                    sub.click()
                    time.sleep(1)
                    claims = driver.find_elements(By.XPATH, "//*[contains(text(),'Claim')]")
                    if claims:
                        claims[0].click()
                        print("Claim attempted!")
                        claim_clicks += 1
                        time.sleep(1)
                        break
        else:
            driver.refresh()
            time.sleep(1)


try:
    login()
    navigate_to_calendars()
    process_opportunities()
finally:
    time.sleep(10)
    driver.quit()