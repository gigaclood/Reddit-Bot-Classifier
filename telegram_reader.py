import json
from collections import Counter
from nltk.stem.snowball import SnowballStemmer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.pipeline import Pipeline
import pandas as pd
from pandas.io.json import json_normalize
import seaborn as sns
import matplotlib.pyplot as plt

telegram_json_path = '/Users/gigaclood/git/Reddit-Bot-Classifier/result.json'
interested_chat_name= 'Acquesi Sparsi'
i = 0

def readChatMessages(filename, chatname):
    interested_chat = None
    with open(filename, 'r', encoding='utf-8') as f:
        result = json.load(f)
    for chat in result.get('chats').get('list'):
        if (chat.get('name') == chatname):
            interested_chat = chat
            print('Chat ', chatname, 'found')

    if interested_chat  :
        tmessages = []
        for message in interested_chat.get('messages'):
            if message.get('type') == 'message' and isinstance(message.get('text'), str):
                tmessages.append({
                    'author': message.get('from'),
                    'text': message.get('text'),
                    'islink':False
                })
            else:
                if isinstance(message.get('text'), list):
                    if isinstance(message.get('text')[0], str):
                        tmessages.append({
                            'author': message.get('from'),
                            'text': message.get('text')[0],
                            'islink':True
                        })
                    elif isinstance(message.get('text')[0].get('text'), str):
                        tmessages.append({
                            'author': message.get('from'),
                            'text': message.get('text')[0].get('text'),
                            'islink':True
                        })
        return tmessages
    else:
        print('Chat', chatname, 'not found!!')
        return None


def classify(jdata):
    #print(jdata)
    df = pd.DataFrame.from_dict(json_normalize(jdata))
    print(df.head(2))
    #sns.lmplot("author", "num msg", data=df, hue="gears", fit_reg=False, col='modelLine', col_wrap=2)
    df['author'].value_counts().plot(kind = 'bar')

    df_plot = df.groupby(['author', 'islink']).size().reset_index().pivot(columns='islink', index='author', values=0)
    df_plot.plot(kind='bar', stacked=True)
    #authors_keys = df.groupby(by='author')
    #pd.value_counts(authors_keys).plot(kind="bar")
    text_clf = Pipeline(
        [
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0))
        ])
    print ('pipeline ready')


if __name__ == "__main__":
    plt.show(block=True)
    tmessages = readChatMessages(filename=telegram_json_path, chatname = interested_chat_name)
    if tmessages:
        print('numero messaggi puliti' , len(tmessages))        
    classify(tmessages)
            

