from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
# Wait for the elements to be present in the DOM using a robust XPath

import time

# Setup WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
# Initialize WebDriverWait
wait = WebDriverWait(driver, 10)
url = "https://www.redbus.in/bus-tickets/khammam-to-hyderabad?fromCityId=401&toCityId=124&fromCityName=Khammam&toCityName=Hyderabad&busType=Any&onward=02-Dec-2024"
driver.get(url)
# Pause for 10 seconds
time.sleep(10)

# bus_container = wait.until(EC.presence_of_all_elements_located(By.CLASS_NAME,'/html/body/section/div[2]/div[4]/div/div[2]/div/div[2]/div[2]/div[3]/ul/div[1]/li'))
busdata = []
def scrapedetails():
    # for i in range(10):
    bus_container = WebDriverWait(driver, 10).until(
EC.presence_of_all_elements_located((By.XPATH, "//ul/div/li"))
)
    print("bus_container",bus_container)
    print("bus_container",len(bus_container))
    for bus in bus_container:
        print("bus :",bus.text)
        bus_lst = bus.text.split('\n')
        busdata.append(
            {
            'bus name': bus_lst[0],
            'Type':bus_lst[1],
            'Depature Time':bus_lst[2],
            'Starting point':bus_lst[3],
            'Duration': bus_lst[4],
            'Arrival Time':bus_lst[5],
            'Date':bus_lst[6],
            'Destination':bus_lst[7],
            'Rating':bus_lst[8],
            'Start Price':bus_lst[10],
            'Total available seats':bus_lst[11],
            'Seat details':bus_lst[12]
            })


        

        #     busname = bus.find_element(By.CLASS_NAME, 'travels 1h-24 f-bold d-color').text
        #     bustype = bus.find_element(By.CLASS_NAME, 'bus-type f-12 m-top-16 1-color evBus').text
        #     busdep = bus.find_element(By.CLASS_NAME, 'dp-time f-19 d-color f-bold').text
        #     busarr = bus.find_element(By.CLASS_NAME, 'bp-time f-19 d-color disp-Inline').text
        #     busdur = bus.find_element(By.CLASS_NAME, 'dur 1-color 1h-24').text
        #     busprice = bus.find_element(By.CLASS_NAME, 'f-19 f-bold').text
        #     busdata.append({'busname':busname, 'bustype':bustype, 'busdep':busdep, 'busarr':busarr, 'busdur':busdur,'busprice':busprice})
        # driver.execute("arguments.[0].scrollIntoView();",bus)
        # time.sleep(1)

    
    df = pd.DataFrame(busdata)
    # bus_container = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'/html/body/section/div[2]/div[4]/div/div[2]/div/div[2]/div[2]/div[3]/ul/div[1]/li')))
    return df

df = scrapedetails()
print(df)