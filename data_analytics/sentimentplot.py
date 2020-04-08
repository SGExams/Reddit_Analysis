from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
analyser = SentimentIntensityAnalyzer()
sns.set(color_codes=True, rc={'figure.figsize':(20,20)})

def sentiment_analyzer_compound(sentence):
    score = analyser.polarity_scores(sentence)
    #print("{:-<40} {}".format(sentence, str(score)))
    return score['compound']

def search(df, term):
    filteredposts = pd.DataFrame()
    mask1 = (df['post_title'].str.contains(str(term))) 
    mask2 = (df['post_body'].str.contains(str(term)))
    filteredposts = df[mask1 | mask2]
    print(filteredposts.info())
    #create an array of text strings for every post, which consists of post body and comment bodies
    #create an array of scores for every post, which consists of post scores and comment scores
    #alternatively, just get compound scores for each line of text
    #start with post firsts, simpler
    
    postweightedsentiment = pd.Series()
    try:
        postweightedsentiment = filteredposts['post_body'].apply(sentiment_analyzer_compound)*filteredposts['post_score']
    except TypeError:
        print('Error with post text')
        pass
    #I need to evaluate the comment bodies because they are in df as string
    comment_array = filteredposts['comment_body'].apply(eval)
    score_array = filteredposts['comment_score'].apply(eval)
    listofcomments = []
    listofscores = []
    
    for i in comment_array:
        #print(str(i) + '\n')
        listofcomments += i
    for score in score_array:
        listofscores += score
    print('Length of comment list is\n' + str(len(listofcomments)))
    
    
    print('Length of comment score list is\n' + str(len(listofscores)))
    
    assert len(listofcomments) == len(listofscores), 'Data lengths not equal!'
    listofsentiments = []
    for comment in listofcomments:
        try:
            listofsentiments.append(sentiment_analyzer_compound(comment))
        except TypeError:
            print('Error with comment text')
            continue
    print('Length of sentiment list is\n' + str(len(listofsentiments)))
    
    commentweightedsentiment = np.array(listofsentiments) * np.array(listofscores)
    
    overallsentimentarray = np.append(postweightedsentiment.array,commentweightedsentiment)
    
    
    return overallsentimentarray

def plotcurve(array,term):
    
    sns.distplot(array)
    sns.kdeplot(array, bw=5, label= "Sentiments of Reddit to: " + str(term),shade = True, color = 'blue')

def drive(df,term):
    array = search(df,term)
    plotcurve(array,term)