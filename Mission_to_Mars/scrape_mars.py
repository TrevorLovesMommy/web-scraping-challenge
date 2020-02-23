from splinter import Browser
from bs4 import BeautifulSoup
import time

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
    
    #set URL
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    
    #scrape html with beautiful soup
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    nasa_title = soup.find('div', class_='content_title').text
    #set delay to allow time for page to load
    time.sleep(20)
    nasa_paragraph = soup.find('div', class_='article_teaser_body').text
       
    #------------ scrape jpl mars news site for featured image ------------------
        
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
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    #set delay so page can load before scraping
    time.sleep(20)
    tw_weather = soup.find('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").find('span').text

   
    #---------------- scrape space-facts.com for table content ------------

    #set url of site
    space_fact_url = 'https://space-facts.com/mars/'

    #set delay to allow time for page to load
    time.sleep(10)

    #read html tables with pandas
    tables = pd.read_html(space_fact_url)
    facts_table=tables[0].to_html()

    #------------------ 4 hemisphere images ------------------
    
    hemisphere_image_urls=[
    {"title":"Cerberus Hemisphere", "img_url":"https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg"},
    {"title":"Schiaparelli Hemisphere", "img_url":"https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg"},
    {"title":"Syrtis Major Hemisphere", "img_url":"https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg"},
    {"title":"Valles Marineris Hemisphere", "img_url":"https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg"}]
    
    #---------------- create dictionary of scraped content ------------
    agg_dictionary = {"nasa_title": nasa_title,
                        "nasa_paragraph": nasa_paragraph,
                        "featured_image_url": featured_image_url,
                        "weather": tw_weather,
                        "facts_table":  facts_table,
                        "hemisphere_images": hemisphere_image_urls}


    return(agg_dictionary);
