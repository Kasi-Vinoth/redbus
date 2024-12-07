from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bus_detail_extract1 import scrapedetails
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import time

def extract_route(bus_data_list, Transport_Name, state_transport_link):
    # Initialize WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:    
        # Open the target website
        driver.get(state_transport_link)

        # Wait for the page to load fully
        driver.implicitly_wait(10)

        # Find the pagination table container
        pagination_table = driver.find_element(By.CLASS_NAME, "DC_117_paginationTable")

        # Find all page elements
        page_elements = pagination_table.find_elements(By.CLASS_NAME, "DC_117_pageTabs")


        for page in page_elements:
            # Check if the page is active (currently visible)
            is_active = "DC_117_pageActive" in page.get_attribute("class")

            # Wait for the <div id="root"> to be present in the DOM
            root_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'root'))
            )

            # Step 2: Go deeper under <div class="D117_main D117_container">
            main_container = root_div.find_element(By.CLASS_NAME, 'D117_main.D117_container')
            
            # Step 3: Locate <div class="route_link">
            route_links = main_container.find_elements(By.CLASS_NAME, 'route_link')
            # Extract information from each `route_link`
            for route_link in tqdm(route_links):
                try:
                    # Locate <div class="route details"> and extract href and title
                    route_details = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(route_link.find_element(By.CLASS_NAME, 'route_details')))
                    a_tag = route_details.find_element(By.TAG_NAME, 'a')
                    href = a_tag.get_attribute('href')
                    title = a_tag.get_attribute('title')
                    
                    #call func
                    bus_data_list = scrapedetails(bus_data_list,href,title,Transport_Name,state_transport_link)
                except:
                    print(href, '-- no buses found.!')
                    return bus_data_list
            if not is_active:
                # Scroll to the page to ensure it is in view
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", page)
                time.sleep(1)  # Small delay to allow scroll action to complete

                # Click on the page to navigate to next page
                page.click()
                time.sleep(2)
            else:
                # print(f"Already on page: {page.text}")
                pass
    except:
        print(state_transport_link, '-- no routes found.!')
        return bus_data_list
    finally:
        # Close the browser
        driver.quit()
    return bus_data_list