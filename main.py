from flask import Flask
import threading
import os
import time
import pickle
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

app = Flask(__name__)

def save_cookies(driver, filename):
    with open(filename, "wb") as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookies(driver, filename):
    with open(filename, "rb") as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)

def human_activity(driver):
    actions = ActionChains(driver)
    while True:
        try:
            # تحريك الماوس إلى مكان عشوائي
            width = driver.execute_script("return window.innerWidth;")
            height = driver.execute_script("return window.innerHeight;")
            x = random.randint(0, width)
            y = random.randint(0, height)
            actions.move_by_offset(x, y).perform()
            print(f"تحريك الماوس إلى ({x}, {y})")
            actions.reset_actions()
            
            # عمل سكرول خفيف لأعلى أو أسفل
            scroll_amount = random.randint(-300, 300)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            print(f"تم سحب الصفحة بمقدار {scroll_amount}px")
            
            # انتظار وقت عشوائي بين الحركات
            time.sleep(random.randint(30, 90))
        except Exception as e:
            print("خطأ أثناء محاكاة النشاط البشري:", e)
            break

def start_bot():
    print("جاري تشغيل البوت ومحاولة الدخول إلى البث...")
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")

    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get("https://kick.com/atro/chat")
        
        if not os.path.exists("cookies.pkl"):
            print("لا توجد كوكيز، سيتم تسجيل الدخول...")
            time.sleep(3)
            login_button = driver.find_element(By.LINK_TEXT, "Sign In")
            login_button.click()
            time.sleep(2)

            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")

            username_input.send_keys("aljrah48")
            password_input.send_keys("123456789Mmm.")
            password_input.send_keys(Keys.RETURN)

            time.sleep(10)
            save_cookies(driver, "cookies.pkl")
            print("تم حفظ الكوكيز!")
        else:
            print("تحميل الكوكيز...")
            driver.delete_all_cookies()
            load_cookies(driver, "cookies.pkl")
            driver.refresh()
            time.sleep(5)
            print("تم تسجيل الدخول باستخدام الكوكيز!")

        print("البوت الآن داخل البث!")

        # بدء محاكاة النشاط البشري في خيط ثاني
        threading.Thread(target=human_activity, args=(driver,)).start()

        time.sleep(7 * 60 * 60)  # مشاهدة لمدة 7 ساعات

    except Exception as e:
        print("حدث خطأ أثناء تشغيل البوت:", e)
    finally:
        if driver:
            driver.quit()

@app.route('/')
def home():
    return "البوت شغال حالياً!"

if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
