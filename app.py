from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    # Setup WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Open Twitter Trending page
    driver.get("https://twitter.com/explore/tabs/trending")

    # Wait for the page to load
    time.sleep(3)

    # Scrape trending topics (hashtags)
    trends = driver.find_elements(By.XPATH, "//div[@data-testid='trend']")

    # Extract trend names (top 5 trends starting with '#')
    top_5_trends = [trend.text.split("\n")[0] for trend in trends[:5] if trend.text.startswith('#')]

    # Close the WebDriver
    driver.quit()

    # Return the HTML template with scraped data
    return render_template("index.html", trends=top_5_trends)

if __name__ == '__main__':
    app.run(debug=True)
