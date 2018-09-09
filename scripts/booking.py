#import dependencies
import requests
import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# import selenium and related libaries
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC

# set up the chrome driver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
dir_path = os.path.dirname(os.path.realpath("booking.ipynb"))
chromedriver = dir_path + "/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)

# fectch the urls
page_urls = pd.read_csv('pages.csv', index_col=0)
page_urls.rename(columns={'0': 'url'}, inplace=True)
URLS = list(page_urls['url'])
URLS = URLS[5001:6000]

# empty list to store the extracted data from each page
results = []

# loop through each url
for url in URLS:

    # load the url
    driver.get(url)
    time.sleep(2)  # Let the user actually see something!

    # scrape the page
    html_content = driver.page_source

    # parse the html and store the results in a beautifulsoup object
    soup = BeautifulSoup(html_content, 'lxml')

    # hotel geocordinates
    try:
        hotel_geo = soup.find(
            'span', class_="hp_address_subtitle")['data-bbox']
    except:
        hotel_geo = None

    # hotel name
    try:
        hotel_name = soup.find(
            'h2', class_='hp__hotel-name').get_text().strip()
    except:
        hotel_name = None

    # hotel address
    try:
        hotel_address = soup.find(
            'span', class_="hp_address_subtitle").get_text().strip()
    except:
        hotel_address = None

    # hotel stars
    try:
        hotel_stars = soup.find(
            'span', class_="hp__hotel_ratings__stars nowrap").find(
                'span', class_="invisible_spoken").get_text().strip()
    except:
        hotel_stars = None

    # hotel reviews
    try:
        hotel_review_text = soup.find(
            'span', class_="review-score-widget__body").find(
                'span', class_="review-score-widget__text").get_text().strip()
    except:
        hotel_review_text = None

    try:
        hotel_reviews = soup.find(
            'span', class_="review-score-widget__body").find(
                'span',
                class_="review-score-widget__subtext").get_text().strip()
    except:
        hotel_reviews = None

    try:
        hotel_review_score = soup.find(
            'span', class_="review-score-badge").get_text().strip()
    except:
        hotel_review_score = None

    # hotel since
    try:
        hotel_since = soup.find(
            'p', class_='summary').find(
                'span', class_='hp-desc-highlighted').get_text().strip()
    except:
        hotel_since = None

    # hotel facilities
    hotel_facilities = []
    for item in soup.find_all('div', class_='important_facility'):
        try:
            hotel_facilities.append(item.get_text().strip())
        except:
            hotel_facilities.append(None)

    # hotel prices
    hotel_prices = []
    for item in soup.find_all('span', class_='bui-price-display__value'):

        try:
            hotel_prices.append(item.get_text().strip().split()[1].strip())
        except:
            hotel_prices.append(None)

    for item in soup.find_all('span', class_='hprt-price-price-standard'):
        try:
            hotel_prices.append(item.get_text().strip().split()[1].strip())

        except:
            hotel_prices.append(None)

    # hotel all facilities
    hotel_all_facilities = {}
    for main in soup.find_all('div', class_='facilitiesChecklistSection'):
        try:
            main_facility = main.find('h5').get_text().strip()
        except:
            main_facility = None

        list_sub = []
        for sub in main.find_all('li'):
            try:
                sub_facility = sub.get_text().strip()
                list_sub.append(sub_facility)
                hotel_all_facilities[main_facility] = list_sub

            except:
                sub_facility = None
                list_sub.append(sub_facility)
                hotel_all_facilities[main_facility] = list_sub

    # construct the dictionary
    hotel = {
        'URL': url,
        'HotelName': hotel_name,
        'HotelAddress': hotel_address,
        'HotelGeoCoordinates': hotel_geo,
        'HotelStars': hotel_stars,
        'HotelReviewText': hotel_review_text,
        'HotelReviews': hotel_reviews,
        'HotelReviewScore': hotel_review_score,
        'HotelSince': hotel_since,
        'HotelPopularFacilities': hotel_facilities,
        'HotelPrices': hotel_prices,
        'HotelDetailedFacilities': hotel_all_facilities
    }

    # append the information to the the results
    results.append(hotel)

# save the results to a csv
df7 = pd.DataFrame(results)
df7.to_csv('output/df7.csv')