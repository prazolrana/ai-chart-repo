**Stock Investment Growth Animation**
main.py:

Description
This Python project allows users to visualize the growth of a stock investment over time using animated line graphs. The script takes a CSV file containing stock price data, prompts the user for an initial investment amount, and calculates the investment value over time.The animation illustrates how the investment would have grown based on historical stock prices.

Features

- Load stock data from a CSV file.
- Ask the user for the column representing stock prices.
- Request an initial investment amount from the user.
- Calculate the investment's value over time.
- Generate an animated line graph showing the investment growth.
- Save the animation as an MP4 file



**Data Scraper for Stock Price History**

Description
This project is a web scraper that extracts historical stock price data from ShareSansar. It automates the process of collecting stock price history, processes the data, and saves it in a clean CSV format for analysis.


Features
- Dynamic URL Input: Allows users to specify any ShareSansar stock page URL.
- Automated Web Scraping: Uses Selenium to navigate and extract data since it is not in a HTML format file. 
- Handles Pagination: Automatically clicks "Next" to scrape all available pages.
- Data Cleaning: Removes empty or null rows to ensure data integrity.
- CSV Export: Saves cleaned data in stock_data_cleaned.csv.


Usage
Run the script: datascraper.py
Enter the stock page URL from merosansar.py when prompted.
The script will scrape the data, clean it, and save it as stock_data_cleaned.csv.

Functionality Breakdown
scrape_stock_data(url, output_file):
  - Navigates to the given URL.
  - Clicks on the "Price History" tab.
  - Extracts stock prices (Date, Open, High, Low, LTP).
  - Iterates through all pages.
  - Cleans and saves the data.

clean_data(df):
  - Replaces empty values with NaN.
  - Drops rows with missing values.

