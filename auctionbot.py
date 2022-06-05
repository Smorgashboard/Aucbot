
from ast import Return
from codecs import escape_encode
from multiprocessing.spawn import old_main_modules
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException

goods = ["renogy"]


driver = webdriver.Firefox()
driver.get("https://www.onlineliquidationauction.com/")
original_window = driver.current_window_handle
wait = WebDriverWait(driver, 10)

search_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ls-global"]/body/div[2]/div[4]/div/div/form/div[2]/input'))).click()

class Item:
    def __init__(self, name, price, endDate):
        self.name = name
        self.price = price
        self.endDate = endDate
        

def doMath(olaPrice, ebayPrice):
    cost = (olaPrice * .13) + (olaPrice * .0675) + olaPrice
    print(cost)
    revenue = ebayPrice * .90
    print(revenue)
    profit = revenue - cost
    if profit >= 10:
        print(f"You could make {profit} dollars!") 
    else:
        print("Dont buy it")
        
    

def gatherIntel() :
    time.sleep(5)
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
    print(driver.current_url)
    itemName = driver.find_element(By.CSS_SELECTOR, 'div.name.roboto.bold.title-text-color.no-side-scroll.ng-binding').get_attribute('innerText')
    itemName = itemName[6:]
    itemPrice = driver.find_element(By.CSS_SELECTOR, 'div.max-bid.col-xs-5.col-sm-5.roboto.black.small.ellipsis.ng-binding.ng-scope').get_attribute('innerText')
    itemPrice = itemPrice.strip("Asking [$")
    itemPrice = itemPrice.replace("]", "")
    itemPrice = int(itemPrice)
    print(itemPrice)
    itemEndDate = driver.find_element(By.CSS_SELECTOR, 'div.reminder.col-xs-6.col-sm-6.roboto.black.small.ellipsis').get_attribute('innerText')
    print(itemEndDate)
    i1 = Item(itemName, itemPrice, itemEndDate)
    print(i1.name)
    print(i1.price)
    print(i1.endDate)
    olaSearchWindow = driver.current_window_handle
    ebayPrice = searchEbay(i1.name, olaSearchWindow)
    doMath(itemPrice, ebayPrice)
    driver.close()
    driver.switch_to.window(original_window)

def searchEbay(i1Name, olaSearchWindow):
    driver.switch_to.new_window('tab')
    driver.get("https://www.ebay.com/sch/ebayadvsearch")
    ebaySearchBar = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="_nkw"]'))).click()
    ese = driver.find_element(By.XPATH, '//*[@id="_nkw"]')
    soldListingsButton = driver.find_element(By.XPATH, '//*[@id="LH_Sold"]')
    soldListingsButton.click()
    ese.send_keys(i1Name)
    time.sleep(5)
    ese.send_keys(Keys.RETURN)
    time.sleep(5)
    ebayPrice = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[1]/div/w-root/div/div/ul/li[2]/ul[1]/li[1]/span').get_attribute('innerHTML')
    ebayPrice = ebayPrice.replace('$', '')
    ebayPrice = ebayPrice.replace('"', '')
    ebayPrice = ebayPrice[:-3]
    ebayPrice = ebayPrice.strip()
    ebayPrice = int(ebayPrice)
    print (ebayPrice)
    driver.close()
    driver.switch_to.window(olaSearchWindow)
    return ebayPrice



def search() :    
    se = driver.find_element(By.XPATH, '//*[@id="ls-global"]/body/div[2]/div[4]/div/div/form/div[2]/input')
    for good in goods:
        print(good)
        se.send_keys(good)
        se.send_keys(Keys.RETURN)
        time.sleep(5)
        if driver.find_elements(By.CSS_SELECTOR, '.alert'):
            print("results found")
            results = driver.find_elements(By.CSS_SELECTOR, 'div.col-md-5.col-sm-6.col-xs-12')
            for r in results:
                r.click()
                gatherIntel()
                
            print(results)
        else:
            print("no results found")

search()