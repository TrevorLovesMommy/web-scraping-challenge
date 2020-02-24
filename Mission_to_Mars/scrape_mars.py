from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    
    #Scrape 4 sites and aggregate all data into one dictionary

    #set browser for scraping
    browser = init_browser()
    
    #declare dictionary to append to:
    master_dictionary={}
    
    #------------scrape nasa mars news site ------------------
    
    print("scraping for mars news")

    #set URL
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    
    #scrape html with beautiful soup
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    nasa_title = soup.find('div', class_='content_title').text

    #set 10 sec delay to finish scraping above content
    time.sleep(40)

    nasa_paragraph = soup.find('div', class_='article_teaser_body').text

    print(nasa_title)
    print(nasa_paragraph)
    #------------ scrape jpl mars news site for featured image ------------------
        
    print("scraping for featured image")    
    #set url of site
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    
    #click on full image button
    browser.click_link_by_partial_text('FULL')
    #set delay to allow time for page to load
    time.sleep(10)
    #click on "more info" button on next pag3
    browser.click_link_by_partial_text('more info')
    #set delay to allow time for page to load
    time.sleep(10)
    
    #scrape image data information with beautiful soup and store in featured_image_url
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    result = soup.find('figure')  
    result = soup.find('figure').find('img')['src'] 
    featured_image_url = f'https://www.jpl.nasa.gov{result}'
    
    #------------ scrape mars weather from twitter  ------------------
    
    #set twitter url
    print("scraping twitter")
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    #set delay so page can load before scraping
    time.sleep(20)
    tw_weather = soup.find('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").find('span').text

   
    #---------------- scrape space-facts.com for table content ------------

    #scrape table and convert into html string
    #set url of site
    space_fact_url = 'https://space-facts.com/mars/'

    time.sleep(10)

    #read html tables with pandas
    tables = pd.read_html(space_fact_url)
    facts_table = (tables[0])
    facts_table.columns=["Description", "Value"]

    facts_table=facts_table.to_html(index=False).replace('\n','')

    #------------------ 4 hemisphere images ------------------
    
    #set url
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #Scrape images
    browser.visit(url)
    browser.click_link_by_partial_text('Cerberus')
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    cerberus_img_url = soup.find('body').find('img', class_ = 'wide-image')['src']
    cerberus_img_url = f"https://astrogeology.usgs.gov{cerberus_img_url}"

    browser.visit(url)
    browser.click_link_by_partial_text('Schiaparelli')
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    schiaparelli_img_url = soup.find('body').find('img', class_ = 'wide-image')['src']
    schiaparelli_img_url = f"https://astrogeology.usgs.gov{schiaparelli_img_url}"

    browser.visit(url)
    browser.click_link_by_partial_text('Syrtis')
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    syrtis_img_url = soup.find('body').find('img', class_ = 'wide-image')['src']
    syrtis_img_url = f"https://astrogeology.usgs.gov{syrtis_img_url}"

    browser.visit(url)
    browser.click_link_by_partial_text('Valles')
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    valles_img_url = soup.find('body').find('img', class_ = 'wide-image')['src']
    valles_img_url = f"https://astrogeology.usgs.gov{valles_img_url}"

    hemisphere_image_urls=[
        {"title":"Cerberus Hemisphere", "img_url":cerberus_img_url},
        {"title":"Schiaparelli Hemisphere", "img_url":schiaparelli_img_url},
        {"title":"Syrtis Major Hemisphere", "img_url":syrtis_img_url},
        {"title":"Valles Marineris Hemisphere", "img_url":valles_img_url}
    ]

    #---------------- create dictionary of scraped content ------------
    agg_dictionary = {"nasa_title": nasa_title,
                        "nasa_paragraph": nasa_paragraph,
                        "featured_image_url": featured_image_url,
                        "weather": tw_weather,
                        "facts_table":  facts_table,
                        "hemisphere_images": hemisphere_image_urls}


    return(agg_dictionary);
