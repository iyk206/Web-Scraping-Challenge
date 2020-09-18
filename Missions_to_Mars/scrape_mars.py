#Import the libraries. We will be using BeautifulSoup to 
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import re
import time

# def browser():

    # return browser
def scrape_data():
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    #Visiting the NASA website for news
    url = "http://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(5)
    
    #We will convert the html from the browser to a soup object
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    element = soup.select_one("li.slide")
    
    #Find Title of the page under "div" and class of "content_title" and save it into titles
    titles = element.find("div", class_="content_title").get_text()
    
    #Find the article text using "div" with class of "article_teaser_body" and save it into article
    article = element.find("div", class_="article_teaser_body").get_text()

    #Visit the Mars Image website and open it using chromedriver
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)

    #Use Splinter to navigate the page and find the current Featured Mars Image
    image_element = browser.find_by_id("full_image")
    image_element.click()

    #Click on "more info" button
    browser.is_element_present_by_text("more info")
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    #Use Beautiful soup and parser to parse the html page
    html = browser.html
    soup_image = BeautifulSoup(html, "html.parser")
    
    image_url = soup_image.select_one("figure.lede a img").get("src")


    featured_image_url = f"https://www.jpl.nasa.gov{image_url}"
    featured_image_url

    #Visit the Mars weather Twitter to scrape Mars weather Info
    url= "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(1)
    #Use Beautiful soup and parser to parse the html page
    html = browser.html
    soup_weather = BeautifulSoup(html, "html.parser")

    #Find the tweet with "Mars Weather" using soup.find_all
    tweet = soup_weather.find_all("article", role="article")[0]

    #Save the weather data into mars_weather variable
    mars_weather = tweet.find_all("span")[4].text

    #Use Pandas to read html dataframe
    #For some reason, I kept getting errored out. I could not find a fix,
    #so I hard coded the info myself since the info is unlikely to change.

    # url = "https://space-facts.com/mars/"
    # browser.visit(url)
    # df = pd.read_html(url)
    # df.columns = ["Facts", "Measurements"]
    # df.set_index("Facts", inplace=True)
    # df

    data = [["Equatorial Diameter:", "6,792 km"], ["Polar Diameter:", "6,752 km"],
       ["Mass:","6.39 × 10^23 kg (0.11 Earths)"], ["Moons:", "2 (Phobos & Deimos)"],
       ["Orbit Distance:", "227,943,824 km(1.38 AU)"], ["Orbit Period:", "687 days (1.9 years)"],
       ["Surface Temperature:", "-87 to -5 °C"], ["First Record:", "2nd millennium BC"],
       ["Recorded By:", "Egyptian astronomers"]]
    df = pd.DataFrame(data, columns= ["Facts", "Measurements"])

    df_html = df.to_html()
    
    #Visit the astrogeology.usgs.gov website and open it using chromedriver
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    time.sleep(1)

    #Use Beautiful soup and parser to parse the html page
    html = browser.html
    soup_hemisphere = BeautifulSoup(html, "html.parser")

    #Scrape the page details
    hemisphere_element = soup_hemisphere.find_all("div", class_="item")

    #Create Empty list to store the image urls
    hemisphere_image_urls = []

    #The href tag is missing the base Url link that comes before the contents in href url.
    #Therefore, we should add the base url to the href url before storing it into our empty list.
    base_url = "https://astrogeology.usgs.gov"

    #We will loop through each of the divs to store the relevant information into our empty list
    for image in hemisphere_element:
        #find the titles and save it into a variable
        title = image.find("h3").text
        
        #We will get the links under href tag and store into a variable
        added_url = image.find("a", class_="itemLink product-item")["href"]
        
        #Visit the Url
        browser.visit(base_url + added_url)
        
        #Use Beautiful soup and parser to parse the html page
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        
        #Get the image url by going under src tag and adding it to the base url
        image_url = base_url + soup.find("img", class_='wide-image')["src"]
        
        #Append the our url list
        hemisphere_image_urls.append({"title" : title, "image_url" : image_url })

    hemisphere_image_urls
    
    #Quit the Browser
    browser.quit()

    final_data = {"news_title": title, "news_article": article,
                  "featured_image" : featured_image_url, "mars_weather" : mars_weather,
                  "mars_facts" : df_html, "mars_hemisphere" : hemisphere_image_urls}
    
    return final_data

# if __name__ == "__main__":





