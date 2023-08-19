from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd

# NASA Exoplanet URL
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Webdriver
service = Service(executable_path="D:/V2 Python/C127/chromedriver.exe")
options = webdriver.ChromeOptions()

browser = webdriver.Chrome(service=service, options=options)
browser.get(START_URL)

time.sleep(10)

planets_data = []

def scrape():
    for i in range(1,2):
        while True:
            time.sleep(2)

            soup = BeautifulSoup(browser.page_source, "html.parser")

            # Check page number    
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))

            #XPATH- helps move from one page to another
            #i- page (1-2) of for loop
            #Why did we add two XPath to the program? makes sure i==current page, helps to move to current page i, by moving back and forward
            if current_page_num < i:
                browser.find_element(By.XPATH,value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num > i:
                browser.find_element(By.XPATH,value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            else:
                break

            

        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")

            # Get Hyperlink Tag
            #Hyperlink-- link in which another page(website) is stored (under li_tag)-- found under "a" tag
            #href-- a link is stored here
            hyperlink_li_tag=li_tags[0]

            temp_list.append("https://exoplanets.nasa.gov"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            
            planets_data.append(temp_list)
            
            #XPATH-- navigates from one page to another

        browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

        print(f"Page {i} scraping completed")


# Calling Method
scrape()

# Define Header
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink"]

# Define pandas DataFrame 
planet_df_1 = pd.DataFrame(planets_data, columns=headers)

# Convert to CSV
#csv- comma separated file (elements of table separated by commas)
planet_df_1.to_csv('updated_scraped_data.csv',index=True, index_label="id")