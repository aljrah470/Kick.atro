from flask import Flask
import threading
import os
import time
import random
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

USERNAME = "aljrah48"
PASSWORD = "123456789Mmm."
STREAM_URL = "https://kick.com/atro"

def save_cookies(driver, path="cookies.pkl"):
    with open(path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver, path="cookies.pkl"):
    with open(path, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

def login(driver):
    driver.get("https://kick.com/login")
    time.sleep(5)
    
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]")
    
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    login_button.click()
    
    time.sleep(8)
    save_cookies(driver)

def random_human_behavior(driver):
    """يحرك الماوس بشكل خفيف وعشوائي داخل الصفحة"""
    actions = ActionChains(driver)
    for _ in range(random.randint(1, 3)):  # يحرك عدة مرات خفيفة
        x_offset = random.randint(-100, 100)
        y_offset = random.randint(-100, 100)
        try:
            actions.move_by_offset(x_offset, y_offset).perform()
            actions.reset_actions()
            time.sleep(random.uniform(1, 3))
        except Exception as e:
            print("تحريك الماوس فشل:", e)

def start_bot():
    print("جاري تشغيل البوت ومحاولة الدخول إلى البث...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://kick.com/")
        time.sleep(5)
        
        if os.path.exists("cookies.pkl"):
            load_cookies(driver)
            driver.refresh()
            time.sleep(5)
        else:
            login(driver)
        
        driver.get(STREAM_URL)
        print("تم الدخول إلى البث بنجاح!")
        
        start_time = time.time()
        while time.time() - start_time < 7 * 60 * 60:  # يراقب 7 ساعات
            random_human_behavior(driver)
            time.sleep(random.randint(30, 60))  # كل نصف دقيقة إلى دقيقة يحرك الماوس
        
        print("انتهى الوقت المحدد. جاري إغلاق البوت...")

    except Exception as e:
        print("حدث خطأ أثناء تشغيل البوت:", e)
    finally:
        if driver:
            driver.quit()

@app.route('/')
def home():
    return "البوت شغال وداخل بث Atro!"

if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
