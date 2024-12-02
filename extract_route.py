import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
from bus_detail_extract import scrapedetails
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
from tqdm import tqdm

def main_program(state_list_link):
    # Initialize WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 10)
    
    bus_data_list = []
    try:
        for state_link in state_list_link:
            # Open the target website
            driver.get(state_link)  # Replace with the actual URL of the website

            # Wait for the page to load (adjust if necessary)
            time.sleep(3)

            # Step 1: Locate the <div id="root">
            root_div = driver.find_element(By.ID, 'root')

            # Step 2: Go deeper under <div class="D117_main D117_container">
            main_container = root_div.find_element(By.CLASS_NAME, 'D117_main.D117_container')

            # Step 3: Locate <div class="route_link">
            route_links = main_container.find_elements(By.CLASS_NAME, 'route_link')
            bus_data = []
            # Extract information from each `route_link`
            for route_link in tqdm(route_links):
                # print(f"Route Link {index + 1}:")
                
                # Locate <div class="route details"> and extract href and title
                route_details = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(route_link.find_element(By.CLASS_NAME, 'route_details')))
                a_tag = route_details.find_element(By.TAG_NAME, 'a')
                href = a_tag.get_attribute('href')
                title = a_tag.get_attribute('title')
                # Extract "price start" and "fare"
                p_tag = route_details.find_element(By.TAG_NAME, 'p')
                fare = p_tag.find_element(By.CLASS_NAME, 'fare').text
                # print(f"  Fare: {fare}")

                # Locate <div class="row2 D117_td"> for the span elements
                row2_td = route_link.find_element(By.CLASS_NAME, 'row2.D117_td')

                # Extract the 4 span values under 'row2 D117_td'
                span_1 = row2_td.find_elements(By.TAG_NAME, 'span')[0].text  # First totalRoutes span
                span_2 = row2_td.find_elements(By.TAG_NAME, 'span')[1].text  # Second totalRoutes span
                span_3 = row2_td.find_elements(By.TAG_NAME, 'span')[2].text  # Third totalRoutes span
 
                bus_data_list = scrapedetails(bus_data_list, driver,href,title,state_link)
        df = pd.DataFrame(bus_data_list)
        return df

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    state_list_link = ['https://www.redbus.in/online-booking/tsrtc/?utm_source=rtchometile','https://www.redbus.in/online-booking/jksrtc']
    df = main_program(state_list_link)