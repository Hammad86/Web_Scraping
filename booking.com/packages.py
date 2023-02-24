from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import chromedriver_autoinstaller as chromedriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    try:
        url = input('Please Enter The URL: ')
        driver = webdriver.Chrome(chromedriver.install())

        driver.get(url)
        wait = WebDriverWait(driver,5)
        range_ = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@role='group']//li)[6]"))).text
        
        for i in range(int(range_)):
            print('page:',(i+1))
            time.sleep(5)
            titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='title']")))
            for count, ele in enumerate(titles):
                print(ele.text)
            btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Next page']")))
            btn.click()
        time.sleep(3600)
    except Exception as e:
        print(e)
        pass