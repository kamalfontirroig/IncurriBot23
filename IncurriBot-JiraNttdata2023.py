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

## Visit https://github.com/kamalfontirroig/IncurriBot23/ for the lastest version
## You need selenium and webdriver_manager packages install for this bot to run
#######
#######
## Add your user Credentials
## Else, leave it as it is and manually enter your credentials when the site login opens
userLogin = "usuario"
userPassword = "contraseña"

## TODO: Load the days we are incurring form CSV into the tuple daysToIncurr
## TODO: The bot should incurr into multiple Jiras by setting them in the daysToIncurr array 

## The bot will take the date, hours to incurr, and jobDescription from this array of tuples. 
## Day must start with 0 if it's lower than 
## Month must be set as the first 3 letters of the Month name, in lower case.
## Be sure of your daysToIncurr array before running the bot, it will not rollback what has been already incurred before failure.
## You can set multiple incurring data for the same date, by adding a tuple with the same date
## For Example:
## [('12/ene/2023 9:00 AM','6h','Worked Hard'), ('12/ene/2023 3:00 PM','2h','Worked kinda hard'), ('12/ene/2023 6:00 PM','1h','Picked my belly button')]
## ATM job descriptions are not being added to  the incurred days, LEAVE EMPTY
daysToIncurr = [ ('07/mar/2023 8:00 AM','9h',''), ('08/mar/2023 8:00 AM','9h',''), ('09/mar/2023 8:00 AM','9h',''), ('10/mar/2023 8:00 AM','9h',''),
('13/mar/2023 8:00 AM','9h',''), ('14/mar/2023 8:00 AM','9h',''), ('15/mar/2023 8:00 AM','9h',''), ('16/mar/2023 8:00 AM','9h',''), ('17/mar/2023 8:00 AM','9h',''),
('20/mar/2023 8:00 AM','9h',''), ('21/mar/2023 8:00 AM','9h',''), ('22/mar/2023 8:00 AM','9h',''), ('23/mar/2023 8:00 AM','9h',''), ('24/mar/2023 8:00 AM','9h','')]

##This is the site where the bot will incurr the above daysToIncurr array
## For example: "https://umane.everis.com/jiraito/browse/HPCCHILE-96" <- Proyecto
## Availability: "https://umane.everis.com/jiraito/browse/HPCCHILE-1472" <- Availability
jiraToIncurrUrl = "https://umane.everis.com/jiraito/browse/HPCCHILE-1472"

## if Two Factor Aunthentication (2FA) is set - as it should be :judgy_eyes: - the bot will only start after it is succesfully login.
## For this, it uses a loginProof, that can be any element's xpath that will be present in the page we are redirected to after succesful 2FA
## For example: "//a[@data-issue-key='HPCCHILE-84']" <- Proyecto
## Availability: "//a[@data-issue-key='HPCCHILE-355']" <- Staffing Pool - Availavility

loginProof = "//a[@data-issue-key='HPCCHILE-355']"
##########
##########


##Bot starts here
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver = webdriver.Chrome(chrome_options=options)

driver.get(jiraToIncurrUrl)

## Login In
WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'userNameInput')))
userInput = driver.find_element("xpath","//input[@id='userNameInput']")
userInput.send_keys(userLogin)
passwordInput = driver.find_element("xpath","//input[@id='passwordInput']")
passwordInput.send_keys(userPassword)
## Submit login
driver.find_element("xpath","//span[@id='submitButton']").click()

## Loop until we have logged in with 2FA
twoFANotDone = True
while twoFANotDone :
    print("Waiting for 2FA completion")
    time.sleep(1)
    try:
        if type(driver.find_element("xpath",loginProof)) is WebElement :
            twoFANotDone = False
    except NoSuchElementException:
        twoFANotDone = True        
print("NEO: We are in")

## Now incurr the loaded days into Jira
print("Incurring Started")
for incurringDay, workedHours, jobDescription in daysToIncurr :
    try:
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'opsbar-operations_more')))
        driver.find_element("xpath","//a[@id='opsbar-operations_more']").click()
        driver.find_element("xpath","//aui-item-link[@id='log-work']").click()
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'log-work-time-logged')))
        driver.find_element("xpath","//input[@id='log-work-time-logged']").clear()
        driver.find_element("xpath","//input[@id='log-work-time-logged']").send_keys(workedHours)
        driver.find_element("xpath","//input[@id='log-work-date-logged-date-picker']").clear()
        driver.find_element("xpath","//input[@id='log-work-date-logged-date-picker']").send_keys(incurringDay)
        
        ### TODO: It should be able to send keys to Job Description
        ### at this point it fails to interact with the element
        #WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'tinymce')))
        #textArea = driver.find_element("xpath","//body[@id='tinymce']")
        #textArea.click()
        #time.sleep(1)
        #textArea = driver.find_element("xpath","//body[@id='tinymce']/p")
        #textArea.click()
        #innerHtml = f"arguments[0].innerText = '{jobDescription}'"
        #driver.execute_script(innerHtml, textArea)
        ##driver.find_element("xpath","//body[@id=''tinymce]/p']").clear()
        ##driver.find_element("xpath","//body[@id=''tinymce]/p]").send_keys(jobDescription)
        ### 

        ##Here it submits the logged work (incurring)
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'log-work-submit')))
        time.sleep(1)
        driver.find_element("xpath","//input[@id='log-work-submit']").click()
        print (f'Incurred {incurringDay} - Hours {workedHours}')
        ## Sleeping is needed for the page to load after submiting work
        time.sleep(5)
    except TimeoutException:
        print("Did the log work window open?")

## Script is done
print("Hey! We are done incurring")   
driver.quit()
