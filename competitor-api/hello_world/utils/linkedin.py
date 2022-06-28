from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import re as re



competitor = []
dates = []
content = []
likes = []
comments = []
shared = []
views = []
media = []
followers = []

with open ('inputs/linkedin.txt' , 'r') as users:
    for pages in users:
        company_name = pages[33:-1]
    users.close()

with open("inputs/linkedin_cred.txt","r") as cresentials
    contents = cresentials.read()
    username = contents.replace("=",",").split(",")[1]
    password = contents.replace("=",",").split(",")[3]
    credentials.close()


def sign_in():
    #accessing Chromedriver
    browser = webdriver.Chrome('chromedriver')


    #Open login page
    browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    #hide browser page

    #Enter login info:
    elementID = browser.find_element_by_id('username')
    elementID.send_keys(username)

    elementID = browser.find_element_by_id('password')
    elementID.send_keys(password)
    elementID.submit()

def scroll_page():
    #Go to company post webpage
    for i in pages:
        browser.get(i + 'posts/')


        #Simulate scrolling to capture all posts
        SCROLL_PAUSE_TIME = 1.5

        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


def load_linkedin_data():
    company_page = browser.page_source

    #Check out page source code
    linkedin_soup = bs(company_page.encode("utf-8"), "html")
    linkedin_soup.prettify()

    containers = linkedin_soup.findAll("div",{"class":"occludable-update ember-view"})
    for container in containers:

        try:
            competitor = container.find("span", {"class":"feed-shared-actor__name"})
            posted_date = container.find("span",{"class":"visually-hidden"})
            text_box = container.find("div",{"class":"feed-shared-update-v2__description-wrapper"})
            text = text_box.find("span",{"dir":"ltr"})
            post_shares = container.findAll("li", {'class':["social-details-social-counts__item--with-social-proof","social-details-social-counts__comments social-details-social-counts__item"]})
            new_likes = container.findAll("li", {'class':["social-details-social-counts__item--with-social-proof","social-details-social-counts__item"]})
            new_comments = container.findAll("li", {"class": "social-details-social-counts__item social-details-social-counts__comments social-details-social-counts__item--with-social-proof"})
            followers = container.find("span", {"class":"feed-shared-actor__description"})

            competitors_name.append(competitor.text.strip())
            post_dates.append(posted_date.text.strip())
            post_texts.append(text.text.strip())
            total_followers.append(followers.text.strip())

        try:
                video_box = container.findAll("div",{"class": "feed-shared-update-v2__content feed-shared-linkedin-video ember-view"})
                video_link = video_box[0].find("video", {"class":"vjs-tech"})
                media_links.append(video_link['src'])
                media_type.append("Video")
            except:
                try:
                    image_box = container.findAll("div",{"class": "feed-shared-image__container"})
                    image_link = image_box[0].find("img", {"class":"ivm-view-attr__img--centered feed-shared-image__image feed-shared-image__image--constrained lazy-image ember-view"})
                    media_links.append(image_link['src'])
                    media_type.append("Image")
                except:
                    try:
                        #mutiple shared images
                        image_box = container.findAll("div",{"class": "feed-shared-image__container"})
                        image_link = image_box[0].find("img", {"class":"ivm-view-attr__img--centered feed-shared-image__image lazy-image ember-view"})
                        media_links.append(image_link['src'])
                        media_type.append("Multiple Images")
                    except:
                        try:
                            article_box = container.findAll("div",{"class": "feed-shared-article__description-container"})
                            article_link = article_box[0].find('a', href=True)
                            media_links.append(article_link['href'])
                            media_type.append("Article")
                        except:
                            try:
                                video_box = container.findAll("div",{"class": "feed-shared-external-video__meta"})          
                                video_link = video_box[0].find('a', href=True)
                                media_links.append(video_link['href'])
                                media_type.append("Youtube Video")   
                            except:
                                try:
                                    poll_box = container.findAll("div",{"class": "feed-shared-update-v2__content overflow-hidden feed-shared-poll ember-view"})
                                    media_links.append("None")
                                    media_type.append("Other: Poll, Shared Post, etc")
                                except:
                                    media_links.append("None")
                                    media_type.append("Unknown")
        try:
                post_likes.append(new_likes[0].text.strip())
            except:
                post_likes.append(0)
                pass

            try:
                post_comments.append(new_comments[0].text.strip())                           
            except:                                                           
                post_comments.append("0")
                pass

            try:
                post_shared.append(post_shares[1].text.strip())                           
            except:                                                           
                post_shared.append("0")
                pass

        except:
            pass