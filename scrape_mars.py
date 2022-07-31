
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# init_browser
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    # Scrape Nasa News
    browser = init_browser()
    news = "https://redplanetscience.com/"
    browser.visit(news)
    html = browser.html
    soup = bs(html, "html.parser")
    latest_title = soup.find("div",class_="content_title").text
    lates_paragraph = soup.find("div",class_="article_teaser_body").text
    browser.quit()

    # Scrape Featured Image
    browser = init_browser()
    image = "https://spaceimages-mars.com/"
    browser.visit(image)
    html = browser.html
    soup2 = bs(html,"html.parser")
    featured_img_url = image + soup2.find("img",class_ = "headerimage")["src"]
    browser.quit()

    # Scrape Mars Fact Table
    fact = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(fact)
    df = tables[0]
    df.columns = df.iloc[0]
    df = df.iloc[1:,:]
    df.set_index("Mars - Earth Comparison",inplace=True)

    # save it to HTML
    fact_table = df.to_html()

    # Scrape Hemisphere image
    browser = init_browser()
    hemisphere = "https://marshemispheres.com/"
    browser.visit(hemisphere)

    hemisphere_lis = []
    hemisphere_title = []
    hemisphere_img = []

    # grab the title 
    html = browser.html
    soup4 = bs(html,"html.parser")
    hemisphere_title = [result.text for result in soup4.find_all("h3")]
    browser.quit()

    # grab the image  
    for title in hemisphere_title[:4]:
        browser = init_browser()      
        hemisphere = "https://marshemispheres.com/"
        browser.visit(hemisphere)
        
        search = title.split(" ")[0].lower()
        image_url = browser.links.find_by_partial_href(f"{search}").first["href"]
        browser.visit(image_url)
        html = browser.html
        soup_ = bs(html,"html.parser")
        
        hemisphere_img.append(hemisphere + soup_.find("img",class_ = "wide-image")["src"])
        browser.quit()

    # form the dictionary
    for i in range(len(hemisphere_img)):
        x = hemisphere_title[i]
        y = hemisphere_img[i]
        input_ = {"title":x,"img":y}
        hemisphere_lis.append(input_)

    Mars = {
        "NewsTitle":latest_title,
        "NewsParagraph":lates_paragraph,
        "FeaturedImage":featured_img_url,
        "FactsTable":fact_table,
        "Hemisphere":hemisphere_lis
    }

    return Mars