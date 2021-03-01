
#import dependencies
def scrape()
    from bs4 import BeautifulSoup as bs
    import pandas as pd
    from splinter import Browser
    from webdriver_manager.chrome import ChromeDriverManager


    #paths

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # # MARS NEWS


    #URL DATA
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)


    #parsing
    html = browser.html
    soup = bs(html, "html.parser")

    #get news text 
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    print(news_title)
    print(news_p)


    # # MARS IMAGES


    #Image scraping

    base_img_url = "https://data-class-jpl-space.s3.amazonaws.com/"
    index_img_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(index_img_url)
    img_button = browser.links.find_by_partial_text('FULL IMAGE')
    img_button.click()


    # parsing
    image_html = browser.html
    img_soup = BeautifulSoup(image_html, 'html.parser')



    img_url = img_soup.select_one('img.fancybox-image').get("src")
    featured_image_url = base_img_url + img_url
    featured_image_url


    # ## MARS FACTS

    #facts url
    facts_url= "https://space-facts.com/mars/"
    browser.visit(facts_url)



    #parsing
    html = browser.html
    soup = bs(html, "html.parser")



    #fact table - rough to DF
    facts = pd.read_html(facts_url)
    facts



    #cleanup, renatme columns, set index
    mars_facts = facts[0]
    mars_facts.columns = ["Description", "Value"]
    mars_facts.set_index('Description', inplace=True)
    mars_facts.head() #final check



    #convert table to HTML
    mars_facts.to_html('table.html')


    # # HEMISPHERES


    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)





    ##Created list manually
    hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    html = browser.html

    #variable for holding list of URLs
    list_urls = list()
    browser.visit(hemispheres_url)


    for h in hemispheres:
            
            browser.click_link_by_partial_text(f"{h}")
            
            images_hemi = browser.html
            soup_hemi = BeautifulSoup(images_hemi, 'lxml')
            
            # chunk of text for title, remove extra words
            title = soup_hemi.find("h2", class_="title").text
            img_url = soup_hemi.find("div", class_="downloads").find("a")["href"]

            full_title = title.split(" Enhanced")
            trim_title = full_title[0]
        
            # dictionary list
            hemisphere_urls.append({"title":title_clean, "img_url":img_url})
            
        
            #back to look for another hemisphere
            browser.back()

    browser.quit()

return_dict = {
        'news': {'news_title': news_title, 'news_pp': news_p},
        'featured_image': featured_image_url,
        'mars_facts_table': mars_facts,
        'hemisphere_image_urls': hemisphere_urls
    }

    return return_dict





