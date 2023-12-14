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





#when it is done you can screen shot the success for me 
def screenshotpage():
    time.sleep(2)
    date_str = date.today().strftime("%m-%d-%Y")
    fpath = os.path.join(os.getcwd(), 'downloads/{}.png'.format(date_str))
    driver.get_screenshot_as_file(fpath)
# defining the function to enable me login 
def login():
    with open('config.json') as configFile:
        credentials = json.load(configFile)
        time.sleep(2)
        driver.find_element(By.XPATH,value="//a[text()='Log in']").click()
        time.sleep(5)
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

# creating a function that will navigate through the board 
def navigateboard():
    # Locate and click the Trello board anchor tag using its XPath
    time.sleep(5)
    board_link = driver.find_element(By.XPATH, "//a[@class='board-tile']")
    board_link.click()
    time.sleep(10)  # Add a sleep to wait for the page to load or use WebDriverWait


def addnewtask():
    # Locate and click the "Add a card" button using its XPath
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[@data-testid='list-add-card-button']").click()
    time.sleep(10)
    #after this I will have to set a value for the field 
    # Locate the textarea using its XPath
    textarea = driver.find_element(By.XPATH, "//textarea[@data-testid='list-card-composer-textarea']")
    textarea.clear()
    time.sleep(2)
    # Write "Bot Made successfully" into the textarea
    textarea.send_keys("Bot Made successfully")
    time.sleep(5)
    # Locate and click the "Add card" button using its XPath
    driver.find_element(By.XPATH, "//button[@data-testid='list-card-composer-add-card-button']").click()
    time.sleep(10)
    # Locate and click the "Cancel" button using its XPath
    driver.find_element(By.XPATH, "//button[@data-testid='list-card-composer-cancel-button']").click()
    time.sleep(5)



        



#I will have to define a main function to take care of my other functions for me 
def main():
    try:
        driver.get('https://trello.com/home')
        login()
        navigateboard()
        addnewtask()
        screenshotpage()
        driver.close()
    except Exception as e:
        print(e)
        driver.close()






if __name__=="__main__":
    main()