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
    with open("config.json") as configFile:
        credentials=json.load(configFile)
        time.sleep(2)
        driver.find_element(By.XPATH, value="//a[text()='Log in']").click()
        time.sleep(2)
        


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