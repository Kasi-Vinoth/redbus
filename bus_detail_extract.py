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

def scrapedetails(bus_data_list,driver,route_link,route_title,state_link):
    driver.get(route_link)
    time.sleep(5)
    bus_container = WebDriverWait(driver, 10).until(
EC.presence_of_all_elements_located((By.XPATH, "//ul/div/li"))
)
    
    for bus in bus_container:
        bus_lst = bus.text.split('\n')
        try:
            busdata_dict = {
                            'state_link':state_link,
                            'route_title':route_title,
                            'route_link':route_link,
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
                            }
        except:
            print("error found\nbus details available:\n",bus_lst)
        bus_data_list.append(busdata_dict)
    return bus_data_list