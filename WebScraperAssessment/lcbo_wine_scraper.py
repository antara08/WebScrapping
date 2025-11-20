import os
import pandas as pd
import wine_details as wd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# Base URL for LCBO
BASE_URL = "https://www.lcbo.com/en/products/wine/red-wine#t=clp-products-wine-red_wine&sort=relevancy&layout=card"
CARD = "//*[@id='coveo-result-list2']//a[contains(@class,'CoveoResultLink') and not(contains(@href, '#'))]"

def main():
    options=Options()
    options.add_argument("--start-maximized")
    driver= webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.set_page_load_timeout(30)
    wine_urls=[]
    all_wine_details = []


    #Create folder on desktop to store the Excel sheet
    desktop=os.path.join(os.path.expanduser("~"),"Desktop")
    folder=os.path.join(desktop,"Wine_Details")

    #Create folder if it does not exist
    os.makedirs(folder,exist_ok=True)

    #Excel file path
    excel_path=os.path.join(folder,"wine_details.xlsx") 



    try:
        #opening the base url for red wine page
        print("opening chrome and launching LCBO")
        driver.get(BASE_URL)   
        wait=WebDriverWait(driver,20)   
        wait.until(ec.presence_of_all_elements_located((By.XPATH, CARD)))
        wines=driver.find_elements(By.XPATH,CARD)
        for wine in wines:
          href=wine.get_attribute("href")
          if href and href not in wine_urls :
              wine_urls.append(href)
        
        #df=pd.DataFrame(wine_urls,columns=['url'])
        for url in wine_urls:
            try:
                details=wd.wine_details(driver,url)
                all_wine_details.append(details)
            except TimeoutError:
                print(f"Timeout while scraping: {url}")
                continue

    except Exception as e:
        print("Exception:",e)
       

    finally:
        driver.quit()

    print("Total wines scraped:", len(all_wine_details))

    #converting dictionary to pandas dataframe
    df_wines = pd.DataFrame(all_wine_details)

    #converting column names in dataframe
    df_wines=df_wines.rename(columns={
     "name": "Wine Name",
    "price": "Price",
    "rating": "Rating",
    "product_note": "Tasting Note",
    "flavours": "Flavours",
    "sweetness": "Sweetness",
    "body": "Body",
    "flavour_intensity": "Flavour Intensity",
    "tannins": "Tannins",
    "release_date": "Release Date",
    "alcohol_vol": "Alcohol/Vol",
    "made_in": "Made In",
    "by": "By",                    
    "sugar_content": "Sugar Content",
    "varietal": "Varietal",
    })

    # Delete old file if exists
    if os.path.exists(excel_path):
        os.remove(excel_path)

    #Write to sheet
    with pd.ExcelWriter(excel_path,engine="openpyxl") as writer:
        df_wines.to_excel(writer,sheet_name="Wine List",index=False)
    


if __name__=="__main__":
    main()