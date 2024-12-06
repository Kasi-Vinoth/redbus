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

def scrapedetails(bus_data_list,route_link,route_title,state_link):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(route_link)
    time.sleep(5)
    bus_container = WebDriverWait(driver, 10).until(
EC.presence_of_all_elements_located((By.XPATH, "//ul/div/li"))
)   
    # print("route_link : \n",route_link)
    # print("BUS CONTAINER: \n",bus_container)
    # bus_items = bus_container.find_elements(By.CSS_SELECTOR, "ul.bus-items li.row-sec.clearfix")


    # Iterate through each bus item and extract required details
    for bus_item in bus_container[1:]:
        bus_info = {}

        # Helper function to handle missing elements
        def get_text_or_default(element, by, value, default=""):
            try:
                el = element.find_element(by, value)
                return el
            except Exception:
                return default

        bus_info['route_title'] = route_title
        bus_info['state_link'] = state_link
        bus_info['route_link'] = route_link
        
        # 1st element: Bus name
        bus_name_element = get_text_or_default(bus_item, By.CSS_SELECTOR, "div.column-two.p-right-10.w-30.fl div.travels.lh-24.f-bold.d-color")
        bus_info['Bus Name'] = bus_name_element.text if bus_name_element else None
        # print("Bus Name :", bus_info['Bus Name'])
        
        # Bus type
        bus_type_element = get_text_or_default(bus_item, By.CSS_SELECTOR, "div.column-two.p-right-10.w-30.fl div.bus-type.f-12.m-top-16.l-color.evBus")
        bus_info['Bus Type'] = bus_type_element.text if bus_type_element else None
        # print("Bus Type :", bus_info['Bus Type'])

        # 2nd element: Start time
        start_time_element = get_text_or_default(bus_item, By.CSS_SELECTOR, "div.column-three.p-right-10.w-10.fl div.dp-time.f-19.d-color.f-bold")
        bus_info['Start Time'] = start_time_element.text if start_time_element else None
        
        # Starting point
        starting_point_element = get_text_or_default(bus_item, By.XPATH, "//*[contains(@class, 'dp-loc') and contains(@class, 'l-color') and contains(@class, 'w-wrap') and contains(@class, 'f-12')]")
        bus_info['Starting Point'] = starting_point_element.text if starting_point_element else None
        
        # 3rd element: Duration
        duration_element = get_text_or_default(bus_item, By.CSS_SELECTOR, "div.column-four.p-right-10.w-10.fl div.dur.l-color.lh-24")
        bus_info['Duration'] = duration_element.text if duration_element else None
        
        # 4th element: Reaching time
        reaching_time_element = get_text_or_default(bus_item, By.CSS_SELECTOR, "div.column-five.p-right-10.w-10.fl div.bp-time.f-19.d-color.disp-Inline")
        bus_info['Reaching Time'] = reaching_time_element.text if reaching_time_element else None
        
        # Destination
        destination_element = get_text_or_default(bus_item, By.CSS_SELECTOR, "div.column-five.p-right-10.w-10.fl div.bp-loc.l-color.w-wrap.f-12")
        bus_info['Destination'] = destination_element.text if destination_element else None
        
        # 5th element: Rating
        rating_element = get_text_or_default(bus_item, By.CSS_SELECTOR, "div.column-six.p-right-10.w-10.fl")
        bus_info['Rating'] = rating_element.text if rating_element else None
        
        # 6th element: Starting price
        starting_price_element = get_text_or_default(bus_item, By.CSS_SELECTOR, "div.column-seven.p-right-10.w-15.fl div.seat-fare div.fare.d-block")
        bus_info['Starting Price'] = starting_price_element.text if starting_price_element else None
        
        # 7th element: Available seats
        available_seats_element = get_text_or_default(bus_item, By.CSS_SELECTOR, "div.column-eight.w-15.fl div.seat-left")
        bus_info['Available Seats'] = available_seats_element.text if available_seats_element else None
        
        # Single seats
        single_seats_element = get_text_or_default(bus_item, By.CSS_SELECTOR, "div.column-eight.w-15.fl div.window-left")
        bus_info['Single Seats'] = single_seats_element.text if single_seats_element else None
        
        # Append bus info to the list
        bus_data_list.append(bus_info)
    # Close the browser
    driver.quit()

    # Print the extracted bus details
    # for bus in bus_details:
    #     print(bus)
        # except:
        #     print("error found\nbus details available:\n",bus_lst)
    return bus_data_list