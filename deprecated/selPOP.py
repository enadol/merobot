from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.transfermarkt.es/borussia-dortmund/transfers/verein/16")
WebDriverWait(driver, 10)
iframe = driver.find_elements(By.TAG_NAME, 'div[@id="notice"]')
driver.switch_to.frame(iframe)
cookieAccept = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Aceptar y continuar']")))
cookieAccept.click()

driver.switch_to.default_content()

#//*[@id="notice"]/div[3]/div[1]/div/button