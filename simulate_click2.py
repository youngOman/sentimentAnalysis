import time
import re
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By



# selenium V4寫法
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
driver.get('https://user.gamer.com.tw/login.php')
# print(driver.title) 
# print(driver.page_source)

username = "Young0921000"
password = "young0921"

login_form=driver.find_element(By.ID, "form-login")
print(login_form)
driver.find_element(By.NAME, "userid").send_keys(username)
time.sleep(2)
driver.find_element(By.NAME, "password").send_keys(password)
time.sleep(2)
driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-border").click()
driver.find_element(By.ID, "btn-login").click()


time.sleep(5)
driver.close()
