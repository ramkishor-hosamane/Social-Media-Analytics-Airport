
import time
import io
from spacy import load as spacy_loader
from . import preprocesser
from pickle import load as pickle_loader

def get_catogarized_review(df):
    from spacy.matcher import Matcher

    nlp = spacy_loader('en_core_web_sm')
    text_clf_lsvc = pickle_loader(open('Data_tools/model.sav', 'rb'))

    patterns = {
            'Food/Shopping':[
                             [{'LOWER':'food'}],
                             [{'LOWER':'restaurants'}],
                             [{'LOWER':'shop'}],
                             [{'LOWER':'dine'}],
                             [{'LOWER':'cafe'}],
                             [{'LOWER':'samosa'}],
                             [{'LOWER':'coffee'}],
                             [{'LOWER':'tea'}],
                             [{'LOWER':'cookies'}],
                             [{'LOWER':'eat'}],
                             [{'LOWER':'drink'}],
                             [{'LOWER':'water'}],

                             [{'LOWER':'bill'}],
                                
                            ],
            'Infrastructures':[
                             [{'LOWER':'signage'}],
                             [{'LOWER':'sign'}],
                             [{'LOWER':'wifi'}],
                             [{'LOWER':'facilities'}],
                             [{'LOWER':'boarding'}],
                             [{'LOWER':'baggage'}],
                             [{'LOWER':'air conditioner'}],
                             [{'LOWER':'ac'}],
                             [{'LOWER':'signposting'}],
                             [{'LOWER':'sitting area'}],
                             [{'LOWER':'infrastructure'}],
                             [{'LOWER':'buisness class'}],
                             [{'LOWER':'aircondition'}],
                             [{'LOWER':'emergency'}],
                             [{'LOWER':'otp'}],
        


                            
                            ],
    
            'Maintenance/Clean':[
                             [{'LOWER':'maintenance'}],
                             [{'LOWER':'maintain'}],
                             [{'LOWER':'maintained'}],
                             [{'LOWER':'clean'}],
                             [{'LOWER':'washroom'}],
                             [{'LOWER':'washrooms'}],
                             [{'LOWER':'restroom'}],
                             [{'LOWER':'restrooms'}],
                             [{'LOWER':'cookies'}],
                             [{'LOWER':'repainting'}],
                             [{'LOWER':'paint'}],
                             [{'LOWER':'painting'}],
                             [{'LOWER':'toilet'}],
                             [{'LOWER':'toilets'}],
                             [{'LOWER':'paint'}],
                             [{'LOWER':'painting'}],
                             [{'LOWER':'unhygienic'}],
                             [{'LOWER':'hygiene'}],
                             [{'LOWER':'unhygiene'}],
                             [{'LOWER':'dirty'}],
                             [{'LOWER':'dirt'}],
                             [{'LOWER':'bathroom'}],
                             [{'LOWER':'Leakage'}],
                             [{'LOWER':'Leak'}],
                             [{'LOWER':'sanitizer'}],
                             
        
                            ],                              
            'Security/Staff':[
                            [{'LOWER':'staff'}],
                            [{'LOWER':'security'}],
                            [{'LOWER':'guard'}],
                            [{'LOWER':'customs'}],
                            [{'LOWER':'Staff'}],
                            [{'LOWER':'officer'}],
                            [{'LOWER':'misbehave'}],
                            [{'LOWER':'misplace'}],
                            [{'LOWER':'theft'}],
                            [{'LOWER':'custom'}],
        
        
                            ]
            }

    t1 = time.time()

    final_res = {top:[] for top in patterns}
    length = len
    Tuple  = tuple
    List = list

    for topic in patterns:
        matcher = Matcher(nlp.vocab)
        pat = patterns[topic]
        res = set()
        matcher.add(topic,None,*pat)
        for i,review in enumerate(df.Review.values):#(df['Reviewer Name'],df['Reviewer Profile URL'],df['Review']):
            doc = nlp(review.lower())
            for sent in doc.sents:
                doc = nlp(preprocesser.Lemmatization(sent))
                f = matcher(doc)
                if length(f)>0:
                        res.add(Tuple((df.iloc[i][0],df.iloc[i][2],sent.text)))

        final_res[topic]=List(res)[:]
    
    t2 = time.time()
    print(t2-t1)
    
    return final_res




def get_Sentiment(df):
    final_ans = []
    text_clf_lsvc = pickle_loader(open('Data_tools/model.sav', 'rb'))
    nlp = spacy_loader('en_core_web_sm')

    for review in df['Review'].values:
        review = review.lower()
        review = preprocesser.RemoveAbbrivations_and_typos(review)
        doc = nlp(review)
        sentiment = 0
        for sent in doc.sents:

            filtered_sent=  preprocesser.RemoveStopWords(sent)
            s = preprocesser.Lemmatization(filtered_sent)
            if len(s.split())<2:
                continue
            ans = text_clf_lsvc.predict([s])[0]
            if ans =='pos':
                sentiment+=1
            elif ans =='neg':
                sentiment-= 1
        if sentiment >= 0:
            final_ans.append('pos')

        elif sentiment < 0:
            final_ans.append('neg')
    return final_ans




def getCompundScore(text):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sid = SentimentIntensityAnalyzer()

    return sid.polarity_scores(text)['compound']
def get_catogarized_topic_sentiment_review(final_res):
    catogarized_final_res = {topic:{'pos':[],'neg':[]} for topic in final_res}
    nlp = spacy_loader('en_core_web_sm')

    def Catogarize(doc,person,personURL,topic):
        z.append(doc)
        text = ''.join(preprocesser.Lemmatization(doc))
        s = getCompundScore(text)
        if(s >0.1):
            catogarized_final_res[topic]['pos'].append(tuple((person,personURL,doc)))
        elif s < -0.1:
            catogarized_final_res[topic]['neg'].append(tuple((person,personURL,doc)))
        else:
            catogarized_final_res[topic][text_clf_lsvc.predict([text])[0]].append(tuple((person,personURL,doc)))
    for topic in final_res:
        for person,personURL,review in final_res[topic]:
            doc  =  nlp(review)
            Catogarize(doc,person,personURL,topic)

    for topic in catogarized_final_res:
            for sentiment in catogarized_final_res[topic]:
                catogarized_final_res[topic][sentiment] =list(catogarized_final_res[topic][sentiment]) 
    return catogarized_final_res

