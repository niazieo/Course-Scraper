import time
import os
import random
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from twilio.rest import Client

# Load your environment variables
load_dotenv('twilio.env')
load_dotenv('uofa.env')

# Twilio account SID and Auth Token
account_sid = os.getenv('SID')
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)

# School User and Pass
username = os.getenv('USER') 
password = os.getenv('PASSWORD') 

chrome_options = Options()
#chrome_options.add_experimental_option("detach", True) # Window doesn't auto close when script is done
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) # Removes a bunch of useless logs in the terminal when something happens
driver = webdriver.Chrome(executable_path=r"D:\Coding\Course-Scraper\drivers\chromedriver.exe", options=chrome_options)
#driver.set_page_load_timeout(30)

# Url to the site you want to scrape
url = "https://www.beartracks.ualberta.ca/psc/uahebprd_7/EMPLOYEE/HRMS/c/SSR_STUDENT_FL.SSR_MD_SP_FL.GBL?Action=U&MD=Y&GMenu=SSR_STUDENT_FL&GComp=SSR_START_PAGE_FL&GPage=SSR_START_PAGE_FL&scname=CS_SSR_MANAGE_CLASSES_NAV"
driver.get(url)
# Waits for webpage to finish loading before continuing script
WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)
print("Waiting for webpage to load...")

# Inputs username/password and submits
driver.find_element(By.ID, "username").send_keys(username)
driver.find_element(By.ID, "user_pass").send_keys(password)
driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/form/input[3]').click()
print("Logging in...")

# Wait for webpage to load after logging in
print("Waiting for webpage to load...")
WebDriverWait(driver=driver, timeout=20).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)
print("Logged in!")

WebDriverWait(driver=driver, timeout=20).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)

try: 
    # If there happens to be an error (this one specifically is "Cookies are not enabled" error), then retry login)
    if driver.find_element(By.ID, "error"):
        print("Failed to login. trying again...")
        driver.find_element(By.ID, "ccid").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/form/fieldset/p[2]/input[1]").click()
        WebDriverWait(driver=driver, timeout=20).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )
        driver.find_element(By.XPATH, "/html/body/form/div[2]/div[4]/div[2]/div/div/div/div/div[4]/section/div/div[3]/div[3]/div/div[3]/div/div[2]/div/div/div/div[1]/div[1]/div/div[2]").click()
        print("Manage Classes")
except:
    print("No error message")

# Wait for webpage to load properly
time.sleep(5)
driver.find_element(By.XPATH, "/html/body/form/div[2]/div[4]/div[1]/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/section/ul/li[2]/div[1]/div/span/a").click()
print("Shopping Cart")

while (True):
    time.sleep(5)
    # Trying to get status of specified class, otherwise error has occurred and script exits
    try:
        status = driver.find_element(By.XPATH, "/html/body/form/div[2]/div[4]/div[2]/div/div/div/div/div/div/div[3]/div[4]/div/div[1]/div/div[1]/div[1]/div[2]/div/div/table/tbody/tr[1]/td[2]/div/div/span").text.lower()
    except:
        message = client.messages \
                        .create(
                            body="An error has occurred.",
                            from_='+13512228493',
                            to='+17806959160'
                        )
        print(message.sid)
        driver.quit()
    if status == "open":
        #Send text via Twilio 
        message = client.messages \
                        .create(
                            body="ITS OPEN GOGOGOGO",
                            from_='+13512228493',
                            to='+17806959160'
                        )
        print(message.sid)
    # This part is unnecessary
    # elif status == "full":
    #     #Send text via Twilio
    #     message = client.messages \
    #                     .create(
    #                         body="still full :(",
    #                         from_='+13512228493',
    #                         to='+17806959160'
    #                     )
    #     print(message.sid)
    ref_time = random.randint(600, 1200) # Refreshes the webpage every 10-20 minutes
    time.sleep(ref_time)
    driver.refresh()
    print("Refreshing page")