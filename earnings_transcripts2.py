import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

import textstat
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV, KFold
from sklearn.metrics import confusion_matrix, average_precision_score, recall_score, precision_score,log_loss, make_scorer, roc_curve, plot_roc_curve, precision_score, auc
plt.style.use('ggplot')

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.tokenize import RegexpTokenizer

def LMdict(series,dictionary):
    positive_list = []
    negative_list = []
    uncertainty_list = []
    superfluous_list = []
    litigious_list = []
    tokenizer = RegexpTokenizer(r'\w+')
        
    positive = 0
    negative = 0
    uncertainty = 0
    superfluous = 0
    litigious = 0
    punc_be_gone = tokenizer.tokenize(series.upper())

    # print(punc_be_gone)

    print(dictionary.keys())

    for word in punc_be_gone:
        if word in dictionary.keys():
            negative += dictionary[word][0]
            positive += dictionary[word][1]
            uncertainty += dictionary[word][2]
            superfluous += dictionary[word][3]
            litigious += dictionary[word][4]
        else:
            continue
    positive_list.append(positive)
    negative_list.append(negative)
    uncertainty_list.append(uncertainty)
    superfluous_list.append(superfluous)
    litigious_list.append(litigious)

    return [positive_list, negative_list, uncertainty_list, superfluous_list, litigious_list]

def get_earnings_analysis(ticker):
    earnings_dates = requests.get("https://financialmodelingprep.com/api/v4/earning_call_transcript?symbol="+ticker+"&apikey=e812649ac124bbb4d773e2ff24a28f0d")
    ed_json = json.loads(earnings_dates.text)
    mrq_transcript = requests.get("https://financialmodelingprep.com/api/v3/earning_call_transcript/"+ticker+"?quarter="+str(ed_json[0][0])+"&year="+str(ed_json[0][1])+"&apikey=e812649ac124bbb4d773e2ff24a28f0d")
    mrq_transcript_json = json.loads(mrq_transcript.text)
    article = mrq_transcript_json[0]["content"]

    # readability test the higher the score, the harder the text is to read
    gunning_fog = textstat.gunning_fog(article)

    # Flesch Kincaid is a readability test designed to indicate how difficult a passage in English is to understand
    # 100 = very easy to read and 0 = very hard to read
    flesch_kincaid = textstat.flesch_reading_ease(article)

    # lexicon count = word count
    lexicon = textstat.lexicon_count(article)

    # "Simple Measure of Gobbledygook" = the higher the score the harder the text is to read
    smog = textstat.smog_index(article)

    words = article.split()
    print(len(words))

    print("gunning fog: ", gunning_fog)
    print("flesch kincaid: ", flesch_kincaid)
    print("smog index: ", smog)
    print("lexicon: ", lexicon)
    sentimental = pd.read_csv('LoughranMcDonald_MasterDictionary_2018.csv')
    sentimental = sentimental[['Word', 'Negative', 'Positive', 'Uncertainty', 'Superfluous', 'Litigious']]
    sentimental_dict = sentimental.to_dict()
    # print(json.dumps(sentimental_dict, indent=4))
    # print(sentimental.columns)
    LM_analysis = LMdict(article, sentimental_dict)
    sentiment_df = pd.DataFrame(LM_analysis).transpose()
    sentiment_df = sentiment_df.rename({0:'Positive', 
                      1:'Negative', 
                      2:'Uncertainty',
                      3:'Superfluous',
                      4:'Litigious'}, axis = 1)
    print(sentiment_df)

get_earnings_analysis('AAPL')


# can be deleted as not being used -- earnings_transcript is being used instead