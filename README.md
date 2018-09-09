# scrape
The repository contains set of Python scripts that I wrote to scrape approximately 10k properties in Booking.com for academic purposes

---
##### Features extracted for each property
1. Name of the property
2. Property Address
3. Property facilities
4. Property Geo-coordinates
5. Property Since
6. Pricing information
7. Rating information
8. Review information

---

##### Main Python libraries used to build the model

* Pandas
* Numpy
* Selenium
* BeautifulSoup

##### An overview on how I built the model

1. Get main page urls for each district

**getpages.ipynb**

Extract district names from https://en.wikipedia.org/wiki/Districts_of_Sri_Lanka. Once the names are extracted, you need to enter the district name in the where you are going box along with the check-in and check-out dates.Store the resulting pages urls as values and name of the districts as keys in a Python dictionary. The notebook futher explains on how to extract all the property urls for each district.

**booking.ipynb**  

This notebook was used to extract the actual property features. Note that I was running the script 1,000 properties at a time at different intervals with sufficient time sleeps between each request not to impede the performance of the site's web server.    

**processing.ipynb**

The notebook was used to preprocess some of the data extracted for each property. I have used the glob library to concat all the 
  







