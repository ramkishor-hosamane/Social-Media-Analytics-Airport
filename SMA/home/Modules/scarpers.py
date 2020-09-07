from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd



Positions_slot = {"pos1":[0,0,False],
					"pos2":[1200,0,False]

					}

def GmapScrap(path,a=20,airport_name="Bengaluru", airport_link='https://www.google.com/maps/place/Kempegowda+International+Airport+Bengaluru/@13.1986348,77.7044041,17z/data=!3m1!4b1!4m7!3m6!1s0x3bae1cfe75446265:0x296c70e9a129418e!8m2!3d13.1986348!4d77.7065928!9m1!1b1'):  # here a is no of scrolls
    global Positions_slot
    a = int(a)

    def scroll():
        scrollable_div = driver.find_element_by_css_selector('div.section-layout.section-scrollbox.scrollable-y.scrollable-show')
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)

    def more():
        links = driver.find_elements_by_xpath('//button[@class=\'section-expand-review blue-link\']')
        for l in links:
            l.click()

    pos_now = 0
    driver = webdriver.Firefox()
    for pos in Positions_slot:
        if  not Positions_slot[pos][2]:
            Positions_slot[pos][2] = True
            driver.set_window_size(750, 850)

            driver.set_window_position(Positions_slot[pos][0], Positions_slot[pos][1])
            print(Positions_slot[pos][0], Positions_slot[pos][1])
            pos_now = pos

            break	
    #driver.set_window_size(400, 468)

    print("Positioning done for ",airport_name,'-->',pos_now)    
    driver.get(airport_link)
    time.sleep(2)

    #driver.maximize_window()




    htmlstring = driver.page_source


    for i in range(1,(a+1)):
        print("scroll "+str(i)+" finished")
        time.sleep(3)

        scroll()
        more()
        time.sleep(3)

        htmlstring = driver.page_source

    soup = BeautifulSoup(htmlstring, "html.parser")
    mydivs = soup.findAll("div", {"class": "section-review-content"})
    counter = 0
    driver.close()
    Positions_slot[pos_now][2] = False

    Reviwer_data = {'Reviewer Name': [], 'Reviewer Rating': [], 'Reviewer Profile URL': [], 'Review': [], 'Time': []}
    for a in mydivs:
        Reviwer_data['Reviewer Name'].append(a.find("div", class_="section-review-title").text)
        Reviwer_data['Reviewer Rating'].append(str(a.find("span", class_="section-review-stars")))
        Reviwer_data['Reviewer Profile URL'].append(str(a.find("a").get('href')))
        Reviwer_data['Review'].append(a.find("span", class_="section-review-text").text)
        Reviwer_data['Time'].append(a.find("span", class_="section-review-publish-date").text)
        counter = counter + 1
    print("Total reviews scraped for"+airport_name+":" + str(counter))
    if airport_name=="Bengaluru":
        pd.DataFrame(Reviwer_data).to_csv(path+'/Scrapped Reviews/gmap_reviews.csv', index=0)
    elif airport_name.split('.')[0]=="food":
        pd.DataFrame(Reviwer_data).to_csv(path+'/Scrapped Reviews/'+airport_name.split('.')[1]+'.csv', index=0)

    else:
        pd.DataFrame(Reviwer_data).to_csv(path+'/Scrapped Reviews/OtherAirports/'+airport_name+'.csv', index=0)
 
    

    
    return 'Google Maps' , len(Reviwer_data["Review"]),airport_name



def facebookScrap(path,a=20):
    a=int(a)
    if(a==0):
        return 0

    def scroll():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    driver = webdriver.Firefox()
    #driver.maximize_window()
    driver.set_window_size(800, 850)
    driver.set_window_position(1400,0)

    		
    #driver.set_window_size(400, 468)

    driver.get('https://www.facebook.com/pg/BLRairport/reviews/?ref=page_internal')
    time.sleep(2)
    print("Positioning done for facebook")


    htmlstring = driver.page_source
    afterstring = ""
    for i in range(1,(a+1)):
        print("scroll "+str(i)+" finished")
        afterstring = htmlstring
        scroll()
        htmlstring = driver.page_source
        if afterstring == htmlstring:
            scroll()
            htmlstring = driver.page_source

        time.sleep(2)
    soup = BeautifulSoup(htmlstring, "html.parser")
    counter = 0
    driver.close()

    Reviwer_data = {'Reviewer Name':[],'Reviewer Rating': [], 'Reviewer Profile URL': [], 'Review': [], 'Time': []}
    for i in soup.find_all(class_='_5pcr userContentWrapper'):
        e = i.find(class_="clearfix y_c3pyo2ta3")
        e1 = e.get('title')
        if(i.find('a').get('title')):
            Reviwer_data['Reviewer Name'].append(i.find('a').get('title'))
        elif(e1):
            Reviwer_data['Reviewer Name'].append(e.get('title'))
        else:
            Reviwer_data['Reviewer Name'].append(e.find('span').get('title'))
        Reviwer_data['Reviewer Rating'].append(i.find('u'))
        l=i.find(class_='fsm fwn fcg')
        Reviwer_data['Reviewer Profile URL'].append('https://www.facebook.com'+l.find('a').get('href'))
        Reviwer_data['Review'].append(i.find('p'))
        Reviwer_data['Time'].append(i.find(class_="timestampContent").get_text())
        counter = counter + 1
    print("Total reviews scraped:" + str(counter))
    pd.DataFrame(Reviwer_data).to_csv(path+'/Scrapped Reviews/facebook_reviews.csv', index=0)
    return "Facebook",len(Reviwer_data["Review"])


class TwitterScrapper:

    def Scrape_Twitter(self, Consumer_Key, Consumer_Secret, Access_Token, Access_Token_Secret, tag, limit=20, lang='en',path="/"):
        import operator,tweepy,re
        print("Starting Scrapping Twitter")

        consumerKey = Consumer_Key
        consumerSecret = Consumer_Secret
        accessToken = Access_Token
        accessTokenSecret = Access_Token_Secret

        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        tweets = tweepy.Cursor(api.search, q=tag, lang=lang).items(limit)

        hashtags = {}
        lst = []
        Reviewer_data = {'Reviewer Name': [], 'Reviewer Profile URL': [], 'Review': [],'Time': []}
        for tweet in tweets:
            Reviewer_data['Reviewer Name'].append(tweet.user.name)
            Reviewer_data['Reviewer Profile URL'].append('https://www.twitter.com/'+tweet.user.screen_name)
            text1 = tweet.text.lower()
            text=re.sub(r"rt\s@\w+:", " ", text1)
            #if(text not in lst):
                #lst.append(text)
            Reviewer_data['Review'].append(text)
            Reviewer_data['Time'].append(tweet.user.created_at)

            for tag in text.split():
                if tag.startswith("#"):
                    if tag[1:] not in hashtags:
                        hashtags[tag[1:]] = 1
                    elif tag[1:] in hashtags:
                        hashtags[tag[1:]] = hashtags[tag[1:]] + 1
                else:
                    pass

        hashtags = sorted(hashtags.items(), key=operator.itemgetter(1), reverse=True)
        hastag_data = {'hastag': [], 'frequency': []}
        for tag in hashtags:
            hastag_data['hastag'].append(tag[0])
            hastag_data['frequency'].append(tag[1])

        time.sleep(1)

        print("Closing Twitter")    
        pd.DataFrame(hastag_data).to_csv(path+'/Scrapped Reviews/Trending_hastag.csv', index=0)
        pd.DataFrame(Reviewer_data).to_csv(path+'/Scrapped Reviews/twitterdata.csv', index=0)
        return limit



def tripAdvisorScrap(path,a=20):
    import io
    import bs4
    import requests
    a = int(a)
    if(a==0):
        return 0

    all_links=['https://www.tripadvisor.in/Attraction_Review-g297628-d16644814-Reviews-Kempegowda_International_Airport_Bengaluru-Bengaluru_Bangalore_District_Kar.html#REVIEWS','https://www.tripadvisor.in/Attraction_Review-g297628-d16644814-Reviews-or5-Kempegowda_International_Airport_Bengaluru-Bengaluru_Bangalore_District_Kar.html#REVIEWS','https://www.tripadvisor.in/Attraction_Review-g297628-d16644814-Reviews-or10-Kempegowda_International_Airport_Bengaluru-Bengaluru_Bangalore_District_Kar.html#REVIEWS','https://www.tripadvisor.in/Attraction_Review-g297628-d16644814-Reviews-or15-Kempegowda_International_Airport_Bengaluru-Bengaluru_Bangalore_District_Kar.html#REVIEWS','https://www.tripadvisor.in/Attraction_Review-g297628-d16644814-Reviews-or20-Kempegowda_International_Airport_Bengaluru-Bengaluru_Bangalore_District_Kar.html#REVIEWS','https://www.tripadvisor.in/Attraction_Review-g297628-d16644814-Reviews-or25-Kempegowda_International_Airport_Bengaluru-Bengaluru_Bangalore_District_Kar.html#REVIEWS','https://www.tripadvisor.in/Attraction_Review-g297628-d16644814-Reviews-or30-Kempegowda_International_Airport_Bengaluru-Bengaluru_Bangalore_District_Kar.html#REVIEWS','https://www.tripadvisor.in/Attraction_Review-g297628-d16644814-Reviews-or35-Kempegowda_International_Airport_Bengaluru-Bengaluru_Bangalore_District_Kar.html#REVIEWS','https://www.tripadvisor.in/Attraction_Review-g297628-d16644814-Reviews-or40-Kempegowda_International_Airport_Bengaluru-Bengaluru_Bangalore_District_Kar.html#REVIEWS','https://www.tripadvisor.in/Attraction_Review-g297628-d16644814-Reviews-or45-Kempegowda_International_Airport_Bengaluru-Bengaluru_Bangalore_District_Kar.html#REVIEWS']
    res=requests.get('https://www.tripadvisor.in/Attraction_Review-g297628-d16644814-Reviews-Kempegowda_International_Airport_Bengaluru-Bengaluru_Bangalore_District_Kar.html#REVIEWS')
    soup= bs4.BeautifulSoup(res.text,'lxml')
    links=[]
    for i in soup.select('.pageNumbers'):
        j=i.find_all('a')
        for k in j:
            links.append('https://www.tripadvisor.in'+k.get('href'))
    Reviwer_data = {'Review Heading': [], 'Date': [],'username':[],'rating':[],'Review': []}
    textdoc = io.open(path+"/Scrapped Reviews/tripreview.txt", "a", encoding="utf-8")
    o=0
    for link in all_links:
        print("Data scrapping started..."+"page "+str(o))
        o+=1
        t = []
        date = []
        username=[]
        rating=[]
        res = requests.get(link)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        for a in soup.select('.location-review-review-list-parts-ReviewTitle__reviewTitle--2GO9Z'):
            t.append(a.find('span').get_text())
        for m in soup.select('.social-member-event-MemberEventOnObjectBlock__event_type--3njyv'):
            username.append(m.find('a').get('href'))
            date.append(m.find('span').get_text())
        for n in soup.select('.location-review-review-list-parts-RatingLine__bubbles--GcJvM'):
            rating.append(n.find('span').get('class'))
        j=0
        k=0
        for i in soup.select('.location-review-review-list-parts-ExpandableReview__reviewText--gOmRC'):
            textdoc.write("\n"+"["+t[j]+"]"+"\n")
            textdoc.write("{"+date[k]+"}"+"\n")
            textdoc.write("("+i.find('span').get_text()+")"+"\n")
            Reviwer_data['Review Heading'].append(t[j])
            Reviwer_data['Date'].append(date[k])
            Reviwer_data['username'].append('https://www.tripadvisor.in'+username[k])
            Reviwer_data['rating'].append(rating[k])
            Reviwer_data['Review'].append(i.find('span').get_text())
            j+= 1
            k+=1
    print("Data scrapping stopping...")
    textdoc.close()
    pd.DataFrame(Reviwer_data).to_csv(path+'/Scrapped Reviews/tripadvisor_reviews.csv',index=0)
    return "TripAdvisor",len(Reviwer_data["Review"])









def twitterScrap(path,a,hashtag):

    a = int(a)*2
    if(a==0):
        return 0
    consumerKey = 'Y2x9rnSVirom9p4aP4j4GmWGy'
    consumerSecret = 'peCyxeqB68YvMrcdjXilHbzbWe3KXZKD4cE6NzHnjxTd2GCm9u'
    accessToken = '2186053585-zX6VlzWtTr9nNg72SXk9q0TWe6yV6VDyI0TCaxF'
    accessTokenSecret = 'T3NAV6vXeOzHXLwBRulUXyBxRQUP8cjdbepFkeFzQyMgh'
    twitter = TwitterScrapper()
    return "Twitter", twitter.Scrape_Twitter(Consumer_Key=consumerKey, Consumer_Secret=consumerSecret, Access_Token=accessToken,
                        Access_Token_Secret=accessTokenSecret, tag=hashtag, limit = a, lang='en',path=path)





