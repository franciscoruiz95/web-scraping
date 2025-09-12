from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
 
def iniciar_driver():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    return driver, wait
 
def cerrar_driver(driver):
    driver.quit()
    print("✅ Navegador cerrado.")