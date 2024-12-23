import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pickle

driver = webdriver.Chrome()
driver.get("https://www.mtbproject.com/featured/rides/top-rated")
wait = input("Press enter when the user is authenticated")
pages = []
sources = []
sources.append(driver.page_source)
while driver.current_url not in pages:
    pages.append(driver.current_url)
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        elem = driver.find_elements(By.CSS_SELECTOR, "[src='/img/arrows/next.svg']")[-1]
        elem.click()
        time.sleep(3)
        sources.append(driver.page_source)
    except Exception as exc:
        break

driver.close()

dbfile = open('sources.pkl', 'wb')
pickle.dump(sources, dbfile)
dbfile.close()