import matplotlib.pyplot as plt
import io,base64
import urllib


def word_cloud(df,path):
    from nltk.corpus import stopwords
    from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
    from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer

    count_vectorizer = CountVectorizer(ngram_range=(1, 2),  
                                    stop_words=stopwords.words('english') + ['airport'], 
                                    token_pattern="\\b[a-z][a-z]+\\b",
                                    lowercase=True,
                                    max_df = 0.6, max_features=4000)
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2),  
                                    stop_words=stopwords.words('english') + ['airport'], 
                                    token_pattern="\\b[a-z][a-z]+\\b",
                                    lowercase=True,
                                    max_df = 0.6, max_features=4000)

    cv_data = count_vectorizer.fit_transform(df.Review)
    tfidf_data = tfidf_vectorizer.fit_transform(df.Review)
    for_wordcloud = count_vectorizer.get_feature_names()
    for_wordcloud = for_wordcloud
    for_wordcloud_str = ' '.join(for_wordcloud)

    wordcloud = WordCloud(width=800, height=400, background_color ='black',
                        min_font_size = 7).generate(for_wordcloud_str)

    plt.figure(figsize=(20, 10), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    print("in vis ",path)
    plt.savefig(path+"/Output/Wordcount.png")


    buf = io.BytesIO()
    plt.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    return url

def star_rating(df,path):
    counts= {'5':0,'4':0,'3':0,'2':0,'1':0,}
    for rat in df['Reviewer Rating'].values:
        counts[str(rat)]+=1
    x = list(counts.keys())
    y = list(counts.values())
    title='Categorised Ratings'
    plt.subplots(figsize=(7,6))

    x_pos = [i for i in range(5)]
    y = y[::-1]
    x=x[::-1]
    plt.barh(x_pos,y,color=['#FF0000','#FFFF33','#FFFF33','#006D2C','#006D2C'],height=0.4)
    plt.ylabel("Ratings")
    plt.xlabel("Counts")
    plt.title(title)
    plt.yticks(x_pos, x)
    plt.tight_layout()
    plt.style.use('ggplot')
    plt.savefig(path+"/Output/star_rating.png")


    buf = io.BytesIO()
    plt.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    return url
def pie_pos_neg(df,path):
    labels = ['Good','Bad']
    sizes = [df['sentiment'].value_counts()['pos'],df['sentiment'].value_counts()['neg']]
    fig, ax = plt.subplots(figsize=(7,6))
    
    ax.pie(sizes, colors=["#006D2C","#FF0000"],labels=labels, autopct='%1.1f%%',shadow=True,wedgeprops   = { 'linewidth' : 1.2,'edgecolor' : "black" })
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

    plt.savefig(path+"/Output/pos_and_neg.png")


    buf = io.BytesIO()
    plt.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    return url
def pie_topic(final_res,path):
    labels = [topic for topic in final_res]
    sizes = [len(final_res[topic]) for topic in final_res]
    fig, ax = plt.subplots(figsize=(8,7))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=True,wedgeprops   = { 'linewidth' : 1.2,'edgecolor' : "black" })
    ax.axis('equal') 
    ax.set_title('categorization of topics')
    plt.savefig(path+"/Output/Catgorized.png")


    buf = io.BytesIO()
    plt.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    return url

def bar_categarized_topic_pos_neg(catogarized_final_res,path):
    import numpy as np
    pos = tuple([len(catogarized_final_res[topic]['pos']) for topic in catogarized_final_res])
    neg = tuple([len(catogarized_final_res[topic]['neg']) for topic in catogarized_final_res])
    n_groups = len(catogarized_final_res)
    # create plot
    fig, ax =plt.subplots(figsize=(8,6))
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 1

    rects1 = plt.bar(index, pos, bar_width,
    alpha=opacity,
    color='#006D2C',
    label='Positve')

    rects2 = plt.bar(index + bar_width, neg, bar_width,
    alpha=opacity,
    color='#f92c18',
    label='Negative')
    plt.xlabel('Topics')
    plt.ylabel('Number of Comments')
    plt.title('Count of Positive and Negative comments based on Topic')
    plt.xticks(index-0.15 + bar_width, tuple([t for t in catogarized_final_res]),rotation=1 )
    #plt.yticks(range(0,max(pos)+300,100))
    plt.legend()
    plt.tight_layout()

    plt.savefig(path+"/Output/catogarized_pos_neg.png")


    buf = io.BytesIO()
    plt.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    return url

def plot_shops(path,sub_df,ccd_df,tif_df,urb_df):
    sub_pos = sub_df["Sentiment"].value_counts()["pos"]
    sub_neg = sub_df["Sentiment"].value_counts()["neg"]
    ccd_pos = ccd_df["Sentiment"].value_counts()["pos"]
    ccd_neg = ccd_df["Sentiment"].value_counts()["neg"]
    tif_pos = tif_df["Sentiment"].value_counts()["pos"]
    tif_neg = tif_df["Sentiment"].value_counts()["neg"]
    urb_pos = urb_df["Sentiment"].value_counts()["pos"]
    urb_neg = urb_df["Sentiment"].value_counts()["neg"]

    labels = ['Subway', 'Tiffin Center','Cafe Coffe Day',"Urban"]
    sizes = [sub_pos+sub_neg, tif_pos+tif_neg,ccd_pos+ccd_neg,urb_pos+urb_neg]
    labels_sent = ['pos', 'neg']*4
    #labels_sent = [" "]*8
    sizes_sent = [sub_pos,sub_neg, tif_pos,tif_neg,ccd_pos,ccd_neg,urb_pos,urb_neg]
    colors = ['#FFB600', '#09A0DA','#3b5998','#ee00b4']
    plt.figure(figsize=(8,9)) 

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{v:d}'.format(p=pct,v=val)
        return my_autopct
    colors_vegefruit = ['#3CB371', '#FF7F50', '#3CB371', '#FF7F50']
    bigger = plt.pie(sizes, labels=labels, colors=colors,
                    startangle=0, frame=True)
    smaller = plt.pie(sizes_sent, labels=labels_sent,
                    colors=colors_vegefruit, radius=0.7,
                    startangle=0, labeldistance=0.7,autopct = make_autopct(sizes_sent))
    centre_circle = plt.Circle((0, 0), 0.4, color='white', linewidth=0)
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
        
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(path+"/Output/"+'shops_real_with_numbers.png')
    #plt.show()
    buf = io.BytesIO()
    plt.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    return url
    #plt.show()

def plot_comparision(path,pos1,neg1,pos2,neg2,airport1="BLR",airport2="KLK"):
    airport1 = airport1.capitalize()
    airport2 = airport2.capitalize()

    print(neg1)
    #pos1 = [len(blr_catogarized_final_res[topic]['pos']) for topic in blr_catogarized_final_res]
    #neg1 = [len(blr_catogarized_final_res[topic]['neg']) for topic in blr_catogarized_final_res]
    #pos2 = [len(pune_catogarized_final_res[topic]['pos']) for topic in pune_catogarized_final_res]
    #neg2 = [len(pune_catogarized_final_res[topic]['neg']) for topic in pune_catogarized_final_res]
    catogarized_final_res = (
            'Food/Shopping ',
            'Infrastructures',
            'Maintenance/Clean' ,                           
            'Security/Staff')
    plt.style.use("ggplot")

    # create plot
    fig, ax = plt.subplots(figsize=(10,7))
    n_groups = 4

    index = np.arange(n_groups)
    bar_width = 0.35
    opacity1 = 1
    opacity2 = 0.8

    plt.bar(0,0, bar_width,
            alpha=opacity1,
            color='#006D2C',
            label=airport1+' Positve')
    plt.bar(0, 0, bar_width,
            alpha=opacity2,
            color='#3CB371',
            label= airport2+' Positve')

    plt.bar(0 + bar_width, 0, bar_width,
    alpha=opacity2,
    color='#FF7F50',
    label=airport2+' Negative',)

    plt.bar(0+ bar_width, 0, bar_width,
    alpha=opacity1,
    color='#FF0000',
    label=airport1+' Negative')

    for i in range(len(index)):
        if pos1[i] > pos2[i]:
            plt.bar(index[i], pos1[i], bar_width,
            alpha=opacity1,
            color='#006D2C',
            )

            plt.bar(index[i], pos2[i], bar_width,
            alpha=opacity2,
            color='#3CB371')
            

            
        else:
            plt.bar(index[i], pos2[i], bar_width,
            alpha=opacity2,
            color='#3CB371')

            plt.bar(index[i], pos1[i], bar_width,
            alpha=opacity1,
            color='#006D2C')
            
        if neg1[i] > neg2[i]:
            plt.bar(index[i]+ bar_width, neg1[i], bar_width,
            alpha=opacity1,
            color='#FF0000',
            )

            plt.bar(index[i]+ bar_width, neg2[i], bar_width,
            alpha=opacity2,
            color='#FF7F50')
            

            
        else:
            plt.bar(index[i]+ bar_width, neg2[i], bar_width,
            alpha=opacity2,
            color='#FF7F50')

            plt.bar(index[i]+ bar_width, neg1[i], bar_width,
            alpha=opacity1,
            color='#FF0000')
            
    





    plt.xlabel('Categories')
    plt.ylabel('Number of Comments')
    plt.title('Count of Positive and Negative comments based on Categories')
    plt.xticks(index-0.15 + bar_width, catogarized_final_res,rotation=0 )
    #plt.yticks(range(0,800,100))

    plt.legend()
    plt.style.use('ggplot')
    plt.style.context('dark_background')
    plt.tight_layout()
    plt.savefig(path+"/Output/"+airport2+'_vs_blore_catogarized_pos_neg.png')
    #plt.show()

    buf = io.BytesIO()
    plt.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    return url





def plot_count_scrapped_reviews(path,all_blr_scraped_res):
    names=[]
    size = []
    for airport in all_blr_scraped_res:
        if all_blr_scraped_res[airport]!=0:
            names.append(airport)
            size.append(all_blr_scraped_res[airport])
    print(names)
    plt.subplots(figsize=(8,7))
    my_circle=plt.Circle( (0,0), 0.7, color='white')
    plt.pie(size,autopct='%1.1f%%',labels=names, colors=['#27ae60','#3b5998','#f5b041','#00acee'])
    p=plt.gcf()
    plt.title("Number of Reviews scrapped from Multiple platforms")
    plt.tight_layout()
    p.gca().add_artist(my_circle)
    plt.savefig(path+"/Output/Total_reviews scarapped.png")


    buf = io.BytesIO()
    plt.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    return url
    #plt.show()