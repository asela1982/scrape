# import libraries
import pandas as pd
import numpy as np
from datetime import datetime
import re
import ast
import glob

# load all the csvs to a dataframe
df = pd.concat(
    [pd.read_csv(f, index_col=0) for f in glob.glob('output/df*.csv')],
    ignore_index=True)

# extract geo-coordinates

def generate_lat(row):
    """
    compute latitude
    """
    lat1 = float(row.split(',')[1])
    lat2 = float(row.split(',')[3])
    lat = np.mean([lat1, lat2])
    return lat

def generate_lon(row):
    """
    compute longitude
    """
    lon1 = float(row.split(',')[0])
    lon2 = float(row.split(',')[2])
    lon = np.mean([lon1, lon2])
    return lon

# extract latitude and longitude information from the HotelGeoCoordinates field
df['Processed_HotelGeoCoordinates_lat'] = df['HotelGeoCoordinates'].apply(
    generate_lat)
df['Processed_HotelGeoCoordinates_lon'] = df['HotelGeoCoordinates'].apply(
    generate_lon)


# apply regex on fields HotelStars and HotelReviews to extract the number of stars and number of reviews 
df['Processed_HotelStars'] = df['HotelStars'].str.extract('(\d+)')
df['Processed_HotelReviews'] = df['HotelReviews'].str.extract('(\d+)')

# extract hotel since
def extract_date(row):
    """
    regex to extract the date part of a string
    """
    match = re.search("(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sept(ember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{1,2},\s+\d{4}", row)
    extract = (match.group(0))
    extract = extract.replace('Sept','Sep')
    extract_date = datetime.strptime(extract, '%b %d, %Y')
    return extract_date

# extract date part information from the HotelSince field
df['Processed_HotelSince']=df['HotelSince'].apply(extract_date)

# number of facilities
def failities_main(row):
    """
    function to get the number of keys in a dictionary
    """
    keys = len(ast.literal_eval(row))
    return keys

# extract the number of main facilities from the HotelDetailedFacilities field
df["Proceesed_facilities_main_count"] = df['HotelDetailedFacilities'].apply(failities_main)

# extract pricing information
def pricing_min(row): 
    """
    function to get the minimum value from a list of values
    """
    list_min = ast.literal_eval(row)
    list_min = [int(item.replace(",","")) for item in list_min]
    try:
        value_min = min(list_min)
    except:
        value_min = np.nan
    return value_min

def pricing_max(row): 
    """
    function to get the max value from a list of values
    """
    list_max = ast.literal_eval(row)
    list_max = [int(item.replace(",","")) for item in list_max]
    try:
        value_max = max(list_max)
    except:
        value_max = np.nan
    return value_max

def pricing_avg(row): 
    """
    function to get the avg value from a list of values
    """
    list_avg = ast.literal_eval(row)
    list_avg = [int(item.replace(",","")) for item in list_avg]
    try:
        value_avg = np.mean(list_avg)
    except:
        value_avg = np.nan
    return value_avg

# extract the prices from the HotelPrices field
df['Proceesed_prices_min'] = df['HotelPrices'].apply(pricing_min)
df['Proceesed_prices_max'] = df['HotelPrices'].apply(pricing_max)
df['Proceesed_prices_avg'] = df['HotelPrices'].apply(pricing_avg)

# clean the HotelReviewText and HotelReviewScore field
for index, row in df.iterrows():
    if row['HotelReviewText']=='Cleanliness':
        df.set_value(index,'HotelReviewScore',np.nan)
        df.set_value(index,'HotelReviewText',None)
        
    elif row['HotelReviewText']=='Review score':
        df.set_value(index,'HotelReviewText','Not Yet Reviewed')
        
    elif pd.isnull(row['HotelReviewText']):
        df.set_value(index,'HotelReviewScore',np.nan)
        df.set_value(index,'HotelReviewText',None)