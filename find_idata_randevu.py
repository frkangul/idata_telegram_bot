import time

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select

MAX_RETRIES = 5  # Maximum number of retry attempts

def click_button_by_xpath(xpath, driver, retry=0):
    if retry >= MAX_RETRIES:
        raise NoSuchElementException("Max retries exceeded for element: {}".format(xpath))

    try:
        button = driver.find_element(By.XPATH, xpath)
        button.click()
        # print("Button clicked successfully.")
    except (NoSuchElementException, StaleElementReferenceException):
        # print("Element not found or stale, retrying...")
        time.sleep(1)
        click_button_by_xpath(xpath, driver, retry=retry + 1)
        
def solve_capcha():
    # Set up Firefox options
    options = Options()

    # Specify the path to your Firefox profile
    options.profile = r'C:\Users\frkan\AppData\Roaming\Mozilla\Firefox\Profiles\cei9p2k2.idata'

    # Create a new instance of the Firefox driver with the specified profile
    driver = webdriver.Firefox(options=options)

    # Open the webpage
    driver.get("https://ita-schengen.idata.com.tr/tr")

    # Wait for 10 seconds
    time.sleep(10)

    # Find the element by CSS selector
    try:
        # Click the button
        click_button_by_xpath('//*[@id="confirmationbtn"]', driver)
    except NoSuchElementException:
        print("Randevu al butonu yok.")

    time.sleep(2)

    try:
        # Click the button
        click_button_by_xpath('/html/body/div[4]/div[7]/div/button', driver)
    except NoSuchElementException:
        print("Tamam butonu yok.")

    time.sleep(2)
    
    # Get the current URL
    current_url = driver.current_url

    capcha_error_counter = 0
    while current_url == "https://ita-schengen.idata.com.tr/tr":
        if capcha_error_counter > MAX_RETRIES:
            capcha_error_counter = 0
            print("driver refresh edildi!")
            driver.refresh()
        # Wait for 10 seconds to complete captcha by nopecha
        time.sleep(10)

        # Find the element by CSS selector
        try:
            # Click the button
            click_button_by_xpath('//*[@id="confirmationbtn"]', driver)
        except NoSuchElementException:
            print("In-While, Randevu al butonu yok.")

        time.sleep(2)

        try:
            # Click the button
            click_button_by_xpath('/html/body/div[4]/div[7]/div/button', driver)
        except NoSuchElementException:
            print("In-While, Tamam butonu yok.")
            
        time.sleep(2)
        
        # Get the current URL
        current_url = driver.current_url
        
        capcha_error_counter = capcha_error_counter + 1
    return driver

def fill_form(driver, ofis="8"): # 8 altunizade, 1 gayrettepe
    ikametgah_dropdown = Select(driver.find_element(By.XPATH, '//*[@id="city"]'))
    ikametgah_dropdown.select_by_value("34")
    # Wait for a moment to see the selection
    time.sleep(1)

    ofis_dropdown = Select(driver.find_element(By.XPATH, '//*[@id="office"]'))
    ofis_dropdown.select_by_value(ofis) # 8 altunizade, 1 gayrettepe
    # Wait for a moment to see the selection
    time.sleep(1)

    amac_dropdown = Select(driver.find_element(By.XPATH, '//*[@id="getapplicationtype"]'))
    amac_dropdown.select_by_value("2") # turistik
    # Wait for a moment to see the selection
    time.sleep(1)

    hizmet_dropdown = Select(driver.find_element(By.XPATH, '//*[@id="officetype"]'))
    hizmet_dropdown.select_by_value("1") # 1 standart, 4 prime
    # Wait for a moment to see the selection
    time.sleep(1)

    kisi_dropdown = Select(driver.find_element(By.XPATH, '//*[@id="totalPerson"]'))
    kisi_dropdown.select_by_value("2") # 2 kişi
    # Wait for a moment to see the selection
    time.sleep(1)    
    
def find_randevu():
    APPOINTMENT_FOUND = 0
    APPOINTMENT_LOC = ""
    while APPOINTMENT_FOUND == 0:
        driver = solve_capcha()

        # 19 dakika içinde denemeler yapabilirsin
        # Record the start time
        start_time = time.time()
        # Define the duration (in seconds) for the function to run
        duration = 10 * 60  # 12 minutes * 60 seconds
        # Run the function repeatedly every minute for the specified duration
        while (time.time() - start_time) < duration:
            fill_form(driver)
            try:
                message = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div/form/div/div[1]/div[3]/div[7]/div').text
                # print(f"For altunizade: {message}")
                # print("-"*50)
                if message.split("\n")[0] != "Uygun randevu tarihi bulunmamaktadır.":
                    if message.split("\n")[0] == "":
                        print("message is empty")
                        APPOINTMENT_LOC = "ALTUNIZADE"
                        APPOINTMENT_FOUND = -1
                        break
                    else:
                        print("APPOINTMENT FOUND IN ALTUNIZADE!")
                        APPOINTMENT_LOC = "ALTUNIZADE"
                        APPOINTMENT_FOUND = 1
                        break    
            except Exception:
                print("message is not available")
            time.sleep(2)  # Sleep for 10 seconds before calling the function again
            
            fill_form(driver, ofis="1")
            try:
                message = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div/form/div/div[1]/div[3]/div[7]/div').text
                # print(f"For gayrettepe: {message}")
                # print("-"*50)
                if message.split("\n")[0] != "Uygun randevu tarihi bulunmamaktadır.":
                    if message.split("\n")[0] == "":
                        print("message is empty")
                        APPOINTMENT_LOC = "GAYRETTEPE"
                        APPOINTMENT_FOUND = -1
                        break
                    else:                    
                        print("APPOINTMENT FOUND IN GAYRETTEPE!")
                        APPOINTMENT_LOC = "GAYRETTEPE"
                        APPOINTMENT_FOUND = 1
                        break
            except Exception:
                print("message is not available")
            time.sleep(10)  # Sleep for 10 seconds before calling the function again
            # driver.refresh()  
        driver.quit()
    driver.quit()
    return APPOINTMENT_LOC, APPOINTMENT_FOUND
    
    
if __name__ == "__main__":
    find_randevu()
