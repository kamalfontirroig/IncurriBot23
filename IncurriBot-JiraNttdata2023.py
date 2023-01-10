from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time 

## User Credentials
userLogin = "usuario"
userPassword = "contraseña"

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver = webdriver.Chrome(chrome_options=options)

driver.get("https://umane.everis.com/jiraito/browse/HPCCHILE-96")

## Login In
userInput = driver.find_element("xpath","//input[@id='userNameInput']")
userInput.send_keys(userLogin)
passwordInput = driver.find_element("xpath","//input[@id='passwordInput']")
passwordInput.send_keys(userPassword)
## Submit login
driver.find_element("xpath","//span[@id='submitButton']").click()

## Loop until we have logged in with 2FA
## loginProof can be any element from the page we are redirected after succesful 2FA
loginProof = "//a[@data-issue-key='HPCCHILE-84']"
twoFANotDone = True
while twoFANotDone :
    print("Waiting for 2FA completion")
    try:
        if type(driver.find_element("xpath",loginProof)) is WebElement :
            twoFANotDone = False
    except NoSuchElementException:
        twoFANotDone = True        
print("We are in")

## TODO: Load the days we are incurring form CSV into the tuple daysToIncurr
daysToIncurr = [('12/ene/2023 9:00 AM','9h'),('13/ene/2023 9:00 AM','9h'),('16/ene/2023 9:00 AM','9h'),('17/ene/2023 9:00 AM','9h'),('18/ene/2023 9:00 AM','9h')]

## Now incurr the loaded days into Jira
print("Incurring Started")
for incurringDay, workedHours in daysToIncurr :
    try:
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'opsbar-operations_more')))
        driver.find_element("xpath","//a[@id='opsbar-operations_more']").click()
        driver.find_element("xpath","//aui-item-link[@id='log-work']").click()
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'log-work-time-logged')))
        driver.find_element("xpath","//input[@id='log-work-time-logged']").clear()
        driver.find_element("xpath","//input[@id='log-work-time-logged']").send_keys(workedHours)
        driver.find_element("xpath","//input[@id='log-work-date-logged-date-picker']").clear()
        driver.find_element("xpath","//input[@id='log-work-date-logged-date-picker']").send_keys(incurringDay)
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'log-work-submit')))
        time.sleep(1)
        driver.find_element("xpath","//input[@id='log-work-submit']").click()
        print (f'Incurred {incurringDay} - Hours {workedHours}')
        ## Sleeping is needed for the page to load after submiting work
        time.sleep(5)
    except TimeoutException:
        print("Did the incurring window open?")

## Script is done
print("Hey! We are done incurring")   
driver.quit()
