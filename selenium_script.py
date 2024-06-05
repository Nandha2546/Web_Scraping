from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from datetime import datetime
import uuid
from fetch_proxy import get_free_proxy  # Ensure this line correctly references fetch_proxy.py

TWITTER_USERNAME = "Nandhakumar2536"
TWITTER_PASSWORD = "Nandha@143"

# Specify the path to the ChromeDriver executable
CHROME_DRIVER_PATH = r"C:\Users\MY-PC\Desktop\chrome-win64\chromedriver.exe"  # Ensure this path includes chromedriver.exe

def get_trending_topics(use_sample_data=False):
    if use_sample_data:
        # Sample trending topics
        topics = ["NEET", "Aboard Study", "#NRI", "Election Results", "Zoho"]
        ip_address = "123.45.67.89"  # Sample IP address
        unique_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # Store results in MongoDB
            client = MongoClient("mongodb://localhost:27017/")
            db = client["twitter_trends"]
            collection = db["trending_topics"]
            document = {
                "unique_id": unique_id,
                "trend1": topics[0],
                "trend2": topics[1],
                "trend3": topics[2],
                "trend4": topics[3],
                "trend5": topics[4],
                "date_time": timestamp,
                "ip_address": ip_address
            }
            collection.insert_one(document)
            return document
        except Exception as e:
            print(f"Error inserting document into MongoDB: {e}")
            return {"error": str(e)}

    proxy = get_free_proxy()
    if not proxy:
        return {"error": "No suitable proxy found"}

    options = webdriver.ChromeOptions()
    options.add_argument(f'--proxy-server=http://{proxy}')
    
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options)
    
    try:
        driver.get("https://twitter.com/login")
        username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "session[username_or_email]")))
        password_input = driver.find_element(By.NAME, "session[password]")
        username_input.send_keys(TWITTER_USERNAME)
        password_input.send_keys(TWITTER_PASSWORD + Keys.RETURN)
        
        # Check for successful login
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Timeline: Trending now']")))
        trending_topics = driver.find_elements(By.XPATH, "//div[@aria-label='Timeline: Trending now']//span")[:5]
        topics = [topic.text for topic in trending_topics]
        
        driver.get("https://api.ipify.org?format=text")
        ip_address = driver.find_element(By.TAG_NAME, "body").text
        
        unique_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            client = MongoClient("mongodb://localhost:27017/")
            db = client["twitter_trends"]
            collection = db["trending_topics"]
            document = {
                "unique_id": unique_id,
                "trend1": topics[0] if len(topics) > 0 else "",
                "trend2": topics[1] if len(topics) > 1 else "",
                "trend3": topics[2] if len(topics) > 2 else "",
                "trend4": topics[3] if len(topics) > 3 else "",
                "trend5": topics[4] if len(topics) > 4 else "",
                "date_time": timestamp,
                "ip_address": ip_address
            }
            collection.insert_one(document)
            return document
        except Exception as e:
            print(f"Error inserting document into MongoDB: {e}")
            return {"error": str(e)}
    
    except Exception as e:
        print(f"Error during Twitter login: {e}")
        return {"error": str(e)}
    
    finally:
        driver.quit()

if __name__ == "__main__":
    result = get_trending_topics(use_sample_data=True)
    print(result)
