from json import loads
import requests
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
import yaml
from datetime import datetime
import certifi

with open("creds.yaml", "r") as file:
    creds = yaml.safe_load(file)
EMAIL = creds['email']
USERNAME = creds['username']
PASSWORD = creds['password']

uri = creds['uri']
dbname = creds['dbname']
collection = creds['collection']
client = MongoClient(uri, tlsCAFile=certifi.where(), server_api=ServerApi('1'))
db = client[dbname]
collection = db[collection]

options = webdriver.ChromeOptions()
options.add_extension("proxy_auth_plugin.zip")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get("https://twitter.com/login")
    time.sleep(3)

    username_input = driver.find_element(By.XPATH, "//input[@autocomplete='username']")
    username_input.send_keys(EMAIL)
    username_input.send_keys(Keys.RETURN)
    time.sleep(3)

    try:
        username_input = driver.find_element(By.NAME, "text")
        username_input.send_keys(USERNAME)
        username_input.send_keys(Keys.RETURN)
        time.sleep(3)
    except TimeoutException:
        print("Twitter didnt ask for Username")

    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)
    driver.get("https://x.com/explore/tabs/trending")
    time.sleep(5)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@data-testid='trend']"))
    )

    trends = driver.find_elements(By.XPATH, "//div[@data-testid='trend']//span[contains(@class, 'css-1jxf684')]")
    if any("Promoted" in trend.get_attribute('innerHTML') for trend in trends[:4]):
        trends = trends[3:]
    else:
        pass

    top_5_trends_html = [trend.get_attribute('innerHTML') for trend in trends if trend.text.startswith('#')][:5]

    print("Top 5 Trending Topics in X Right Now:")
    for i, trend_html in enumerate(top_5_trends_html, 1):
        print(f"{i}. {trend_html}")

    driver.get("https://api64.ipify.org?format=json")
    time.sleep(1)
    ip_address = driver.find_element("tag name", "body").text
    ip_data = loads(ip_address)
    only_ip = ip_data["ip"]
    current_id = collection.count_documents({}) + 1
    timestamp = datetime.now()
    trend_data = {
        "_id": current_id,
        "ip_address" : only_ip,
        "date" : timestamp.strftime("%x"),
        "time": timestamp.strftime("%X"),
        "trends": top_5_trends_html
    }

    result = collection.insert_one(trend_data)
    print(f"Data inserted with ID: {result.inserted_id}")

finally:
    driver.quit()
