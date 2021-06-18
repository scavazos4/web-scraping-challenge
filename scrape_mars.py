# Seting up dependacies for MongoDB and Flask application

from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import pymongo
import requests
import time

def init_browser():
    return Browser('chrome', headless=False)

def scrape():
    browser = init_browser()

    # NASA Mars News define and retrive
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    titles = soup.find_all('div', class_= "slide")
    soup = bs(response.text, 'html.parser')
    time.sleep(1)
    headlines = []
    teasers = []

    for result in titles:
        try:
            title = result.find('div', class_="content_title").text
            teaser = result.find("div", class_="rollover_description_inner").text

            if (title and teaser):
                print('-------------')
                print(title)
                print(teaser)
                print('-------------')
                headlines.append(title)
                teasers.append(teaser)
        except AttributeError as e:
            print(e)





    # Mars Facts
    # Have pandas read any tables on mars facts page
    url2= 'https://space-facts.com/mars/'
    table = pd.read_html(url2)
    # Filter to table I want to work with
    factsTable = table[0]
    factsTable_df = pd.DataFrame(factsTable)
    factsTable_df = factsTable_df.rename({0:"Describe" , 1:"Mars"}, axis =1)
    # Convert to html string & clean
    factsTableHtml = factsTable_df.to_html()

    # Mars Hemispheres
    # Set up for retriving browser
    url3 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url3)
    html = browser.html
    soup = bs(html, "html.parser")
    # Setting up bucket
    hemisImages = []
    # Base image url
    url4 = "https://astrogeology.usgs.gov/"
    # Set up soup
    hemis = bs.find_all('div', class_='item')
    # Setting up loop to get title and url
    for hemi in hemis:
        title = hemi.find('h3').text
    
        browser.click_link_by_partial_text("Hemisphere Enhanced")
        img_html = browser.html
        img_soup = bs(img_html, "html.parser")
        imgsUrl = img_soup.find('img', class_='wide-image')['src']
    
        images_url = url4+imgsUrl
        hemisImages.append({"title": title, "img_url": images_url})
    





    # Close browser after scraping
    browser.quit()
    
    # Creating dictionary for all of the scrapped info
    mars={
        "Mars_news_headlines": title,
        "Mars_News_Teasers": teaser,
        "Featured_Mars_Image": "Not Available",
        "Mars_Facts": factsTableHtml,
        "Mars_Hemispheres": hemisImages,
        }
    # mars_dic = "Hello World"
    return mars

if __name__ == "__main__":
    data = scrape()
    print(data)