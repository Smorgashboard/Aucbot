from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException

#goods = ["dewalt", "lego", "apple", "Nexstar", "Renogy", "makita", "milwaukee", "rigid", "victron", "dometic", "yeti", "nintendo", "microsoft", "xbox", "ps5", "playstation", "pokemon", "Magic", "Yugioh", "hp", "meta", "quest", "dell", "raspberry pi", "dji"]
goods = ["makita", "lego"]
ebaysearches = 0

driver = webdriver.Firefox()
driver.get("https://www.onlineliquidationauction.com/")
original_window = driver.current_window_handle
wait = WebDriverWait(driver, 10)

search_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ls-global"]/body/div[2]/div[4]/div/div/form/div[2]/input'))).click()
products = []

class Item:
    def __init__(self, name, price, endDate, auction, itemNumber, itemUrl, profit):
        self.name = name
        self.price = price
        self.endDate = endDate
        self.auction = auction
        self.itemNumber = itemNumber
        self.itemUrl = itemUrl
        self.profit = profit

def gatherForReview(name, price, endDate, auction, itemNumber, itemUrl, profit):
    products.append( Item(name,price,endDate,auction,itemNumber,itemUrl,profit))


def doMath(olaPrice, ebayPrice):
    if ebayPrice == 0:
        print("Could not find on Ebay")
    cost = (olaPrice * .13) + (olaPrice * .0675) + olaPrice
    print(cost)
    revenue = ebayPrice * .90
    print(revenue)
    profit = revenue - cost
    if profit >= 30:
        print("profit") 
    else:
        print("Dont buy it")
    return profit

def gatherIntel() :
    time.sleep(5)
    olaSearchWindow = driver.current_window_handle
    itemName = driver.find_element(By.CSS_SELECTOR, 'div.name.roboto.bold.title-text-color.no-side-scroll.ng-binding').get_attribute('innerText')
    itemNumber = itemName[:4]
    itemNumber = itemNumber.strip('#')
    itemName = itemName[6:]
    itemPrice = driver.find_element(By.CSS_SELECTOR, 'div.max-bid.col-xs-5.col-sm-5.roboto.black.small.ellipsis.ng-binding.ng-scope').get_attribute('innerText')
    itemPrice = itemPrice.strip("Asking [$")
    itemPrice = itemPrice.replace("]", "")
    itemPrice = int(itemPrice)
    itemEndDate = driver.find_element(By.CSS_SELECTOR, 'div.reminder.col-xs-6.col-sm-6.roboto.black.small.ellipsis').get_attribute('innerText')
    auction = driver.find_element(By.CSS_SELECTOR, 'div.roboto.bold.header.ellipsis.header-primary-text-color').get_attribute('innerText')
    url = driver.current_url
    ebayPrice = searchEbay(itemName, olaSearchWindow)
    profit = doMath(itemPrice, ebayPrice)
    i1 = Item(itemName, itemPrice, itemEndDate, auction, itemNumber, url, profit)
    gatherForReview(i1.name, i1.price, i1.endDate, i1.auction, i1.itemNumber, i1.itemUrl, i1.profit)
    driver.close()
    for window_handle in driver.window_handles:
        if window_handle != olaSearchWindow:
            driver.switch_to.window(olaSearchWindow)
            break
    

def searchEbay(i1Name, olaSearchWindow):
    global ebaysearches
    ebaysearches = ebaysearches + 1
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
    try: 
        ebayPrice = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[1]/div/w-root/div/div/ul/li[2]/ul[1]/li[1]/span').get_attribute('innerHTML')
        ebayPrice = ebayPrice.replace('$', '')
        ebayPrice = ebayPrice.replace('"', '')
        ebayPrice = ebayPrice[:-3]
        ebayPrice = ebayPrice.strip()
        ebayPrice = int(ebayPrice)
        print (ebayPrice)
    except NoSuchElementException:
        ebayPrice = 0
    driver.close()
    driver.switch_to.window(olaSearchWindow)
    return ebayPrice
    

def resultsFound():
    results = driver.find_elements(By.CSS_SELECTOR, 'div.col-md-5.col-sm-6.col-xs-12')
    for r in results:
        r.click()
        gatherIntel()
    try:
        nextPage = driver.find_element(By.XPATH, '//*[@id="main-content-top"]/div/div[1]/div[7]/div/ul/li[3]/a')
        nextPage.click()
        resultsFound()
    except NoSuchElementException:
        print("No more pages.")
        se = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div/form/div[2]/input")
        se.click()

def search():
    se = driver.find_element(By.XPATH, '//*[@id="ls-global"]/body/div[2]/div[4]/div/div/form/div[2]/input') 
    for good in goods:
        print(good)
        se.send_keys(good)
        se.send_keys(Keys.RETURN)
        time.sleep(5)
        if driver.find_elements(By.CSS_SELECTOR, '.alert'):
            print("results found")
            resultsFound()
        else:
            print("no results found")
            se = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div/form/div[2]/input")
        
def allAuctions() :
    driver.get("https://www.onlineliquidationauction.com/")
    allAucs = driver.find_elements(By.CSS_SELECTOR, 'div.col-md-5.col-sm-6.col-xs-12')
    for x in allAucs:
        x.click()
        clickHere = driver.find_elements(By.CSS_SELECTOR, 'a.btn-u.btn-u-lg.btn-block.btn-default.rounded.margin-bottom-20')
        for click in clickHere:
            print(click)
            click.click()
            auctionItemsWindow = driver.current_window_handle
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
            time.sleep(15)
            print("waking up")
            allItems = driver.find_elements(By.CSS_SELECTOR, 'div.roboto.medium-gray.description.ng-binding')
            print(allItems)
            for item in allItems:
                item.click()
                print("nested for")
                time.sleep(7)
                gatherIntel()


search()

#allAuctions()

print(ebaysearches)
print(products)