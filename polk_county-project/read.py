import gspread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
import time
# selenium 3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

fileName = input('Enter a file name')
gc = gspread.service_account()
wks = gc.open_by_url(fileName).sheet1

# # Input for sheet url
# fileName = input('Enter a google sheet url')
# gc = gspread.service_account()

# # opening sheet with given url
# wks = gc.open_by_url(fileName).sheet1

# Opnening and installing web driver
driver = webdriver.Chrome(ChromeDriverManager().install())

# selecting 4th column
col_1 =wks.col_values(4)
print(col_1[0])
a=len(wks.col_values(4))
print(a)


for i in range(1,a+1):
    
    driver.get('https://www.polkpa.org/CamaDisplay.aspx?OutputMode=Input&searchType=RealEstate&page=FindByAddress')
    element = WebDriverWait(driver, 40).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@class='text ui-autocomplete-input']")) )

    element.send_keys(f'{col_1[i]}')
    searchBtn = WebDriverWait(driver, 40).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@id='searchRE_address']")) )
    searchBtn.click()
    try:
        parcelID = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "(//td)[12]")) ).text
        print(parcelID)
        parcelDate = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "(//td)[14]")) ).text
        print(parcelDate)
        wks.update(f'AB{i+1}',f'{parcelID}')
        wks.update(f'AC{i+1}',f'{parcelDate}')
    except:
        wks.update(f'AB{i+1}','Address not found')
        wks.update(f'AC{i+1}','Address not found')
        continue
    