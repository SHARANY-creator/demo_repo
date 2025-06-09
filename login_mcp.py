from selenium import webdriver
from selenium.webdriver.common.by import By
import pyotp
import time
from Variable import *

# Calculates an OTP based on the pingID secret
secret = pingS
totp = pyotp.TOTP(secret)
otp = totp.now()

#Open a new Edge browser session
driver =webdriver.Edge()
driver.get('https://mercedes-benz.atlassian.net/jira')

# Fill in the registration form
time.sleep(5)
driver.find_element(By.ID,'username').send_keys(eMail)
driver.find_element(By.ID,'login-submit').click()

driver.find_element(By.ID,'userid').send_keys(userID)
driver.find_element(By.ID,'next-btn').click()

time.sleep(5)
driver.find_element(By.ID,'password').send_keys(pw)
driver.find_element(By.ID,'loginSubmitButton').click()

time.sleep(5)
driver.find_element(By.ID,'otp').send_keys(otp)

time.sleep(5)
driver.find_element(By.XPATH, "//input[@value='Anmelden']").click()

time.sleep(60)

# Check whether the login was successful
if "Home" in driver.page_source:
    print("Registration successful")
else:
    print("Failed")

driver.quit()




{
        "description": "{ProblemDetailsHTML} Problem URL: {ProblemURL}",
        "tag": "{Tags}",
        "alias": "{ProblemTitle} + {State}",
        "entity": "{ImpactedEntity}",
        "message": "{ProblemTitle} ID: {ProblemID}",
        "responders": [    {
            "id": "4e624c14-4c80-4364-be75-e3eb1e9a2592",
        "type": "team"    }]
        "priority": "P5"
    }