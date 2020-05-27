from textblob import TextBlob 
import pandas as pd
stopwords= ['a', 'about', 'an', 'and', 'are', 'as', 'at', 'be', 'been', 'but', 'by', 'can', \
             'even', 'ever', 'for', 'from', 'get', 'had', 'has', 'have', 'he', 'her', 'hers', 'his', \
             'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'me', 'my', 'of', 'on', 'or', \
             'see', 'seen', 'she', 'so', 'than', 'that', 'the', 'their', 'there', 'they', 'this', \
             'to', 'was', 'we', 'were', 'what', 'when', 'which', 'who', 'will', 'with', 'you','take', 'ten', 'than', 'that', 'the', 'their', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these', ]
abbr_df = pd.read_csv('Data_tools/Spell.csv')
abbrivations = {abbr:fullform for abbr,fullform in zip(abbr_df.ShortForms.values,abbr_df.FullForms.values)}

def RemoveAbbrivations_and_typos(review):
    for i,word in enumerate(review):
        if abbrivations.get(word)!=None:
            review[i] = abbrivations.get(word)
    tb = TextBlob(review)
    tb = tb.correct()
    return str(tb)
            

def RemoveStopWords(doc):
    filtered_sent=[]

    for word in doc:
        #print(word.text)
        if word.text in list('\n\n!""-#$%&()--.*+,-/:;<=>?@[\\]^_`{|}~\t\n.') and word.is_alpha!=True:
            continue
        if word.text not in stopwords:    
            filtered_sent.append(word)

    return filtered_sent
def Lemmatization(doc):
    lemmas = [token.lemma_ for token in doc if token.pos_!='-PRON-']
    return ' '.join(lemmas)


def preprocess(df):
    try:
        df['Reviewer Rating'] = [x[19:20] for x in df['Reviewer Rating'].values]  
    except:
        pass

    df.dropna(inplace=True)
    blanks = []
    for revw in df.itertuples():    
        if type(revw) == str:
            if revw.isspace():
                blanks.append(i)
    df.drop(blanks,inplace=True)
    return df