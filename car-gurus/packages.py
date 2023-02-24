from selenium import webdriver
import chromedriver_autoinstaller as chromedriver
from selenium.webdriver import ActionChains
import time
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(chromedriver.install(),options=options)
    # to maximize the browser window
    driver.maximize_window()
    driver.get("https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip=78154&showNegotiable=true&sortDir=ASC&sourceContext=untrackedExternal_false_0&distance=100&sortType=DEAL_RATING_RPL")
    wait = WebDriverWait(driver,5)
    try:
        btn = wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@role='slider'])[2]")))
        move = ActionChains(driver)
        move.click_and_hold(btn).move_by_offset(-35, 0).release().perform()
        time.sleep(5)
        check_1 = wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@type='checkbox'])[1]")))
        driver.execute_script("arguments[0].click();", check_1)
        time.sleep(5)
       
        btn2 = wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@role='slider'])[3]")))
        #if milage is still more then 60,000 then increase the value -197.5 to 198 
        move.click_and_hold(btn2).move_by_offset(-197.5, 0).release().perform()
        time.sleep(2)
        min_year = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@aria-label='Select Minimum Year']/option[@value='2020']")))
        min_year.click()
        time.sleep(2)
        max_year = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@aria-label='Select Maximum Year']/option[@value='2023']")))
        max_year.click()

        radius = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='select-filter']/option[@value='25']")))
        radius.click()
        time.sleep(5)
        check_2 = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='DEAL_RATING-GREAT_PRICE']")))
        driver.execute_script("arguments[0].click();", check_2)
        time.sleep(5)
        check_3 = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='HAS_PHOTOS']")))
        move.move_to_element(check_3).perform()
        time.sleep(5)
        driver.execute_script("arguments[0].click();", check_3)
        check_5 = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='IS_SINGLE_OWNER']")))
        move.move_to_element(check_5).perform()
        time.sleep(2)
        driver.execute_script("arguments[0].click();", check_5)
        
        check_4 = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='HAS_RECENT_PRICE_DROPS']")))
        move.move_to_element(check_4).perform()
        time.sleep(2)
        driver.execute_script("arguments[0].click();", check_4)
        time.sleep(2)
        rating = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='FOUR_STAR_AND_MORE']")))
        move.move_to_element(rating).perform()
        time.sleep(2)
        driver.execute_script("arguments[0].click();", rating)
        
    except:
        pass

    try:
        flag = True
        myList = ['PRIORITY', 'FEATURED']
        while flag:
            try:
                time.sleep(5)
                links = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@data-cg-ft='car-blade-link']")))
                try:
                    wait.until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Close']"))).click()
                except:
                    pass
                with open('data.csv', 'a+', encoding='utf-8-sig', newline='') as f:
                    writer = csv.writer(f)
                    for i in range(1,len(links)+1):
                        try:
                            link = wait.until(EC.presence_of_element_located((By.XPATH, f"(//a[@data-cg-ft='car-blade-link'])[{i}]"))).get_attribute('href')
                        except:
                            link = 'N/A'
                        try:
                            name = wait.until(EC.presence_of_element_located((By.XPATH, f"(//a[@data-cg-ft='car-blade-link'])[{i}]//h4"))).text
                        except:
                            name = 'N/A'
                        try:   
                            price = wait.until(EC.presence_of_element_located((By.XPATH, f"(//a[@data-cg-ft='car-blade-link'])[{i}]//h4//span"))).text
                        except:
                            price = 'N/A'
                        try:
                            mile = wait.until(EC.presence_of_element_located((By.XPATH, f"(//a[@data-cg-ft='car-blade-link'])[{i}]//p//span[2]"))).text
                        except:
                            mile = 'N/A'
                        try:
                            img = wait.until(EC.presence_of_element_located((By.XPATH, f"(//a[@data-cg-ft='car-blade-link'])[{i}]//img"))).get_attribute('src')
                        except:
                            img = 'N/A'
                        #print(link)
                        #print(name)
                        #print(price)
                        #print(mile)
                        #print(img)
                        #print(i,'=============================')
                        if any(x in link for x in myList):
                            pass
                        else:
                            writer.writerow([name,price,mile,link,img])
                    time.sleep(5)
                    wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-cg-ft='page-navigation-next-page']"))).click()
            except:
                flag = False
                break
                
    except Exception as e:
        print(e)
        pass
    return driver
        
