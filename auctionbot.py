
from ast import Return
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException

goods = ["lego"]


driver = webdriver.Firefox()
driver.get("https://www.onlineliquidationauction.com/")

search_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ls-global"]/body/div[2]/div[4]/div/div/form/div[2]/input'))).click()



def search() :    
    se = driver.find_element(By.XPATH, '//*[@id="ls-global"]/body/div[2]/div[4]/div/div/form/div[2]/input')
    for good in goods:
        print(good)
        se.send_keys(good)
        se.send_keys(Keys.RETURN)
        time.sleep(5)
        if driver.find_elements(By.CSS_SELECTOR, '.alert'):
            print("results found")
            results = driver.find_elements(By.CLASS_NAME, 'owl-wrapper-outer')
            for r in results:
                print(r.get_attribute("href"))
                r.context_click().perform()
            print(results)
        else:
            print("no results found")

search()