from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape_all():
    #Scrape all areas

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, par_text = scrape_mars_news(browser)

    featured_image_url= scrape_jpl(browser)

    mars_html_table= scrape_mars_table(browser)
    #call other functions


    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "par_text": par_text,
        "featured_image_url": featured_image_url,
        "mars_html_table": mars_html_table
    } 


    # Close the browser after scraping
    browser.quit()
    return mars_data


def scrape_mars_news(browser):


    # Visit Mars News Site
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #latest news title
    news_title = soup.find('div', class_='content_title').text

    #scrape paragraph text

    par_text= soup.find('div', class_='article_teaser_body').text



    # Close the browser after scraping
    browser.quit()

    # Return results
    return news_title, par_text


def scrape_jpl(browser):

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit Mars News Site
    url_jpl = "https://spaceimages-mars.com/"
    browser.visit(url_jpl)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #find relative image path
    relative_image_path = soup.find_all('img')[1]['src']


    #combine with url for featured image url
    featured_image_url = url_jpl + relative_image_path





    # Close the browser after scraping
    browser.quit()

    # Return results
    return featured_image_url


def scrape_mars_table(browser):

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit Mars News Site
    url_mars_facts = "https://galaxyfacts-mars.com/"
    browser.visit(url_mars_facts)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #convert scraped table into pandas df
    tables = pd.read_html(url_mars_facts)

    #Grab specific table that is desired
    mars_df= tables[0]

    #clean df
    new_header = mars_df.iloc[0] #grab the first row for the header
    mars_df = mars_df[1:] #take the data less the header row
    mars_df.columns = new_header #set the header row as the df header
    
    #convert cleaned df into html string
    html_table = mars_df.to_html()


    #---> further clean by dropping \n
    mars_html_table= html_table.replace('\n', '')



    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_html_table