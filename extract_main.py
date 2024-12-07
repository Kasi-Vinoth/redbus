from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from extract_route import extract_route
import pandas as pd
from tqdm import tqdm


def main(main_url):
    # Initialize Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(main_url)

    rtc_directory = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.rtcHeadViewAll"))
    )

    anchor = rtc_directory.find_element(By.TAG_NAME, "a")
    rtc_directory_url = anchor.get_attribute("href")
    # print('url : ',rtc_directory_url)

    # State directory URL
    driver.get(rtc_directory_url)

    # Wait for the page to load fully
    driver.implicitly_wait(10)

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")    
    # Initialize the list to store results
    result_list = []

    # Locate the main container <div class="D113_ul_rtc">
    main_container = driver.find_element(By.CLASS_NAME, "D113_ul_rtc")

    # Find all <ul class="D113_ul_region_rtc"> inside the main container
    ul_elements = main_container.find_elements(By.CLASS_NAME, "D113_ul_region_rtc")

    # Loop through each <ul> element
    for ul in ul_elements:
        # Find all <li class="D113_item_rtc"> inside the current <ul>
        li_elements = ul.find_elements(By.CLASS_NAME, "D113_item_rtc")

        # Extract href and text from each <li>
        for li in li_elements:
            try:
                # Extract href if available
                anchor = li.find_element(By.TAG_NAME, "a")
                href = anchor.get_attribute("href")
                text = anchor.text.strip()  # Extract the visible text

                # Append the dictionary to the list
                result_list.append({"Transport Name": text, "href": href})
            except Exception as e:
                print(f"Error processing an <li>: {e}")

    # Close the browser
    driver.quit()

    # Print the extracted list
    # print(result_list)
    bus_data_list = []
    for link in tqdm(result_list):
        Transport_Name = link['Transport Name']
        # print(Transport_Name)
        bus_data_list = extract_route(bus_data_list, Transport_Name, link['href'])
    
    return bus_data_list

if __name__ == "__main__":
    main_url = "https://www.redbus.in"
    bus_data_list = main(main_url)
    df = pd.DataFrame(bus_data_list)
    df.to_csv("redbus.csv")
    print("Saved Successfully")