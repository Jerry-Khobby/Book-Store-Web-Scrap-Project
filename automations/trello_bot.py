from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from datetime import date
import os
import json

option = webdriver.ChromeOptions()
driver = webdriver.Chrome(options = option)







# defining the function to enable me login 
def login():
    with open('config.json') as configFile:
        credentials = json.load(configFile)
        time.sleep(2)
        driver.find_element(By.XPATH,value="//a[text()='Log in']").click()
        time.sleep(2)
        username_input = driver.find_element(By.CSS_SELECTOR, "#username")
        username_input.send_keys(credentials['USERNAME'])
        time.sleep(5)
        # Locate and click the "Continue" button using its CSS selector
        driver.find_element(By.CSS_SELECTOR, "#login-submit").click()
        time.sleep(5)
        #I want to locate the password field 
        password_input = driver.find_element(By.CSS_SELECTOR, "#password")
        password_input.send_keys(credentials['PASSWORD'])  #
        time.sleep(5)
        #finally I will be smashing it on that login button 
         # Locate and click the "Log in" button using its CSS selector
        login_button = driver.find_element(By.CSS_SELECTOR, "#login-submit")
        login_button.click()
        time.sleep(20)


        



#I will have to define a main function to take care of my other functions for me 
def main():
    try:
        driver.get('https://trello.com/home')
        login()
        driver.close()
    except Exception as e:
        print(e)
        driver.close()






if __name__=="__main__":
    main()