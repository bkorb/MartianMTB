import pickle
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import time

dbfile = open('sources.pkl', 'rb')
sources = pickle.load(dbfile)
dbfile.close()

def get_details(details):
    details = [span.text.strip() for span in details.select('span[class*="metric"]')]
    return {'length': details[0], 'ascent': details[1], 'descent': details[2]}

def get_stars(stars):
    count = 0
    for star in stars.select('img'):
        if star.get('src') == '/img/stars/starRed.svg':
            count += 1
        elif star.get('src') == '/img/stars/starRedHalf.svg':
            count += 0.5
    return count

def extract_data(source):
    soup = bs4.BeautifulSoup(source, 'html5lib')
    cards = soup.select('div[class*="card-container"]')
    routes = []
    for card in cards:
        difficulty = card.select('span[class*="difficulty-text"]')[0].text.strip()
        title = card.select('h4[class*="card-title"]')[0].text.strip()
        details = get_details(card.select('p[class*="technical-details"]')[0])
        stars = get_stars(card.select('span[class*="scoreStars"]')[0])
        location = card.select('span[class*="city-state"]')[0].text.strip()
        link = card.select('a')[0].get('href')
        routes.append({'difficulty': difficulty, 'title': title, 'location': location, 'link': link, 'stars': stars, 'details': details})
    return routes

routes = sum([extract_data(source) for source in sources], [])

download_dir = "/Users/bkorb/Projects/MartianMTB/EarthRoutes/temp"
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
})
driver = webdriver.Chrome(options=options)
driver.get("https://www.mtbproject.com/featured/rides/top-rated")
input("Press enter when user is authenticated")

def wait_for_download(directory, timeout=30):
    for _ in range(timeout):
        files = os.listdir(directory)
        for file in files:
            if str(file).endswith(".gpx"):
                return file
        time.sleep(1)
    return None

for route in routes:
    link = route['link']
    id = link.split("/")[-2]
    driver.get(link)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    download = driver.find_element(By.XPATH, "//*[contains(text(), 'Download GPX File')]")
    download.click()
    file = wait_for_download(download_dir)
    if file is not None:
        path = download_dir + "/" + file
        route['id'] = id
        os.rename(path, f"/Users/bkorb/Projects/MartianMTB/EarthRoutes/route_{id}.gpx")
    else:
        route['id'] = None
    time.sleep(3)

driver.quit()

dbfile = open('routes.pkl', 'wb')
sources = pickle.dump(routes, dbfile)
dbfile.close()