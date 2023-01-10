from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_experimental_option('debuggerAddress', 'localhost:9014')
driver = webdriver.Chrome(options=options)

try:
    #driver.find_element("xpath","//input[@id='log-work-time-logged']").clear()
    #driver.find_element("xpath","//input[@id='log-work-time-logged']").send_keys("sup?")
    #wait = WebDriverWait(driver, 10)
    #element = wait.until(EC.element_to_be_clickable((By.XPATH, "//textarea[@id='comment']")))
    #textArea = driver.find_element("xpath", "//textarea[@id='comment']")
    #driver.execute_script("arguments[0].focus();", textArea)
    #textArea.click()
    driver.switch_to.frame(driver.find_element("xpath","//iframe[@id='mce_0_ifr']"))
    textArea = driver.find_element("xpath", "//iframe[@id='mce_0_ifr']")
    textArea.click()
    textArea.send_keys("Hola Mundo")
    #driver.switch_to.default_content()
finally:
    driver.quit()
    