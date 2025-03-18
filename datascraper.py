""" This program helps you to automate scraping the data from merosharesansar.com and to filter it as well"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

      

def cleandata(df): 
  """This function removes any rows with empty values in the datasets"""
  df_cleaned=df.replace("",pd.NA).dropna()
  return df_cleaned


def scrape_price_history(url, output_csv="stock_price_history.csv"):
    """Scrapes stock price history from ShareSansar and saves it to a CSV file."""
    
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=options)
    
    try:
        # Open the given URL
        driver.get(url)

        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tab-content"))
        )

        # Click on the "Price History" tab
        price_history_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Price History')]"))
        )
        price_history_tab.click()
        time.sleep(3)  # Allow time for content to load

        # Ensure the table is loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-bordered tbody tr"))
        )

        # List to store all scraped data
        all_data = []

        # Extract table data function
        def extract_table():
            rows = driver.find_elements(By.CSS_SELECTOR, "table.table-bordered tbody tr")
            data = []
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 5:  # Ensure there are enough columns
                    row_data = [
                        cols[1].text.strip(),  # Date
                        cols[2].text.strip(),  # Open
                        cols[3].text.strip(),  # High
                        cols[4].text.strip(),  # Low
                        cols[5].text.strip(),  # LTP (Last Traded Price)
                    ]
                    data.append(row_data)
            return data

        # Get table headers
        headers = ["Date", "Open", "High", "Low", "LTP"]

        # Pagination handling
        while True:
            print("Scraping page...")
            
            # Extract and store table data
            all_data.extend(extract_table())

            # Find "Next" button dynamically
            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'paginate_button next')]"))
                )
                if "disabled" in next_button.get_attribute("class"):
                    break  # Stop if "Next" is disabled
                next_button.click()
                time.sleep(3)  # Allow time for new data to load
            except:
                print("No more pages.")
                break

        # Convert to DataFrame and save to CSV
        df = pd.DataFrame(all_data, columns=headers)
        df.to_csv(output_csv, index=False)
        output_csv=df_cleaned(output_csv) #removed rows with empty columns for more accurate data
        print(f"Scraping complete! Data saved to {output_csv}")

    finally:
        # Close browser
        driver.quit()


# User inputs the stock page URL
user_url = input("Enter the ShareSansar stock page URL: ")
scrape_price_history(user_url)




  
  
