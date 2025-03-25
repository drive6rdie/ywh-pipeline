from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from pyotp import TOTP
import json
import os

with open("config.json") as f:
    config = json.load(f)

driver_path = config["geckodriver_path"]
profile_path = config["firefox_profile_path"]
username = config["username"]
password = config["password"]
secret = config["totp_secret"]

match None:
    case _ if driver_path is None:
        print("Please set the path to the geckodriver in the config.json file.")
        exit()
    case _ if profile_path is None:
        print("Please set the path to the firefox profile in the config.json file.")
        exit()
    case _ if username is None:
        print("Please set your username in the config.json file.")
        exit()
    case _ if password is None:
        print("Please set your password in the config.json file.")
        exit()
    case _ if secret is None:
        print("Please set your TOTP secret in the config.json file.")
        exit()

options = Options()
options.add_argument(f"--profile={profile_path}")

service = Service(driver_path)
driver = webdriver.Firefox(service=service, options=options)


driver.get('https://yeswehack.com/business-units/equans/programs/vpn-test/imports')
time.sleep(2)
if EC.presence_of_element_located((By.ID, 'program-report-imports-button')):
    ## IMPORT
    driver.find_element(By.ID, 'program-report-imports-button').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'attachments-field-default'))).send_keys(os.getcwd()+"/reports.csv")
    driver.find_element(By.ID, 'import-validate-button').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'import-close-button')))
    driver.find_element(By.ID, 'import-close-button').click()
    
else:
    ## LOGIN
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'email-input')))
    mail = driver.find_element(By.ID, 'email-input').send_keys(username)
    password = driver.find_element(By.ID, 'password-input').send_keys(password)
    driver.find_element(By.ID, 'login-submit-button').click()
    totp = TOTP(secret).now()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'totp-code-input'))).send_keys(totp)
    time.sleep(5)
    driver.find_element(By.ID, 'totp-form-submit-button').click()

    ## IMPORT
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'program-report-imports-button')))
    driver.find_element(By.ID, 'program-report-imports-button').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'attachments-field-default'))).send_keys(os.getcwd()+"/reports.csv")
    driver.find_element(By.ID, 'import-validate-button').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'import-close-button')))
    driver.find_element(By.ID, 'import-close-button').click()
    
driver.close()
driver.quit()
