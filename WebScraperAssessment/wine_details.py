import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from locators import PRODUCT_PRICE,PRODUCT_RATING,PRODUCT_NOTE,PRODUCT_NAME


def wine_details(driver,url):
    
    details={}
    try:
        driver.get(url)
    except TimeoutException:
        print(f"Page load timeout for:{url}")
        driver.execute_script("window.stop();")
        return details
        
    wait = WebDriverWait(driver, 10)

    #Name
    try:
        name = wait.until(ec.presence_of_element_located((By.XPATH,PRODUCT_NAME)))
        details["name"] = name.text.strip()
    except (TimeoutException, NoSuchElementException):
        details["name"] = None
    

    #Price
    try:
        price=driver.find_element(By.XPATH,PRODUCT_PRICE)
        price1=price.text.strip()
        details["price"]=price1
    except NoSuchElementException:
        details["price"] = None
    
    #Rating
    try:
        rating=driver.find_element(By.XPATH,PRODUCT_RATING)
        rating1=rating.text.strip()
        details["rating"]=rating1
    except NoSuchElementException:
        details["rating"] = None
      

    #Product Note
    try:
        product_note=driver.find_element(By.XPATH,PRODUCT_NOTE)
        product_note1= product_note.text.strip()  
        details["product_note"]=product_note1
    except NoSuchElementException:
        details["product_note"] = None

    wanted_labels = {
        "Release Date",
        "Alcohol/Vol",
        "Made In",
        "By",
        "Sugar Content",
        "Varietal",
    }

    #Taste Profile
    try:
        # Find all rows inside the Taste Profile section
        rows = driver.find_elements(By.XPATH,"//div[contains(@class,'foodParings')]//li")
        for row in rows:
            try:
                label = row.find_element(By.XPATH, ".//div[@class='label']").text.strip()
                key = label.lower().replace(" ", "_")
                value_div = row.find_element(By.XPATH, ".//div[@class='value']")

                # Case: textual flavours list
                if value_div.get_attribute("aria-label") is None:
                    details[key] = value_div.text.strip()

                # Case: numeric rating
                else:
                    aria = value_div.get_attribute("aria-label")
                    m = re.search(r'(\d+)', aria)      # extract first number
                    rating = int(m.group(1)) if m else None
                    details[key] = rating

            except Exception:
                continue

    except Exception:
        pass

    # More Details
    try:
        rows = driver.find_elements(By.XPATH, "//ul/li")
        for row in rows:
            try:
                label = row.find_element(By.XPATH, ".//div[@class='label']")
                value = row.find_element(By.XPATH, ".//div[@class='value'][1]")

                label1 = label.text.strip()
                value1 = value.text.strip()

                if not label1 or not value1:
                    continue
                #only keep rows we care about
                if label1 not in wanted_labels:
                    continue

                # keys formatted
                key = (
                    label1.lower()
                    .strip()
                    .replace(" ", "_")
                    .replace("/", "_")
                    .replace(":", "")
                )

                details[key]=value1

            except Exception:
                continue

    except Exception:
        pass

    #--------------------------------
    return details    
       

