from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime
def fetch_nifty50_data():
        
        
        # Set up Chrome WebDriver with additional options
    options = webdriver.ChromeOptions()
    # Comment out the headless option to see the browser window for debugging
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.page_load_strategy = 'eager'  # Use 'eager' to wait for the DOM to be ready

    # Set up the WebDriver (Make sure ChromeDriver is installed and in your PATH)
    driver = webdriver.Chrome(options=options)

    # URL for Nifty 50 stocks
    url = "https://www.nseindia.com/market-data/live-equity-market?symbol=NIFTY%2050"
    driver.get(url)

    # Explicit wait for the table to load
    try:
        # Wait for the table with the ID 'equityStockTable' to be present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "equityStockTable"))
        )
        
        # Locate the table using the ID 'equityStockTable'
        table = driver.find_element(By.ID, "equityStockTable")
        print(table)
        time.sleep(5)
        # Locate the rows inside the table (skipping the header row)
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]

        # Extract symbols from the table
        symbols = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells:
                symbol = cells[0].text  # The first cell contains the stock symbol
                symbols.append(symbol)

        # Convert the list of symbols into a DataFrame for easier manipulation
        df = pd.DataFrame(symbols, columns=["Symbol"])
        print(df)
        current_date = datetime.now().strftime('%Y%m%d_%H%M')
        df.to_csv(f'nifty_50{current_date}.csv',index=False)

    finally:
        # Close the WebDriver
        driver.quit()
        return df
