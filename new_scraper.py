from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import requests
import time
import pandas as pd

# NASA Exoplanet URL
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Webdriver
service = Service(executable_path="./chromedriver_win32/chromedriver.exe")
options = webdriver.ChromeOptions()

browser = webdriver.Chrome(service=service, options=options)
browser.get(START_URL)

time.sleep(10)

new_planets_data = []

def scrape_more_data(hyperlink):
    #if there is an error, except block will work
    try:
        #requests-- api call to get information
        page = requests.get(hyperlink)
        #parser-helps to get relation from the webpage
        soup = BeautifulSoup(page.content, "html_parser")
        temp_list = []
        
        #tr- access row, td- access column
        #in attrs, class of tag is written (same as from inspect button)
        for tr_tag in soup.find_all("tr", attrs={"class":"fact_row"}):
            #td_tags-- accesses every cell of table
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class":"value"})[0].content)
                except:
                    temp_list.append("")
                    
            new_planets_data.append(temp_list)


    except:
        time.sleep(1)
        scrape_more_data(hyperlink)


planet_df_1 = pd.read_csv("updated_scraped_data.csv")

# Call method
#extracting values using index row by row using hyperlink
for index, row in planet_df_1.iterrows():

    print(row['hyperlink'])
    scrape_more_data(row['hyperlink'])

    print(f"Data Scraping at hyperlink {index+1} completed")

print(new_planets_data)

# Remove '\n' character from the scraped data
scraped_data = []

for row in new_planets_data:
    replaced = []
    
    #el -- local variable, access elements in row
    for el in row:
        el = el.replace("\n","")
        replaced.append(el)
    scraped_data.append(replaced)
print(scraped_data)


    
    

headers = ["planet_type","discovery_date", "mass", "planet_radius", "orbital_radius", 
           "orbital_period", "eccentricity", "detection_method"]

new_planet_df_1 = pd.DataFrame(scraped_data,columns = headers)

# Convert to CSV
#index = sequence
#if index=False, no need for index_label
#id = index label of first column (serial number)
new_planet_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")

