# SGExams HBL Sentiment Analysis (Reddit Data)
## Brief Description of the Data
We gathered reddit data based on PRAW's API and decided to collect these columns which are ``post_title``, ``post_flair``, ``post_createdat``, ``post_body``, ``post_url``, ``post_score``, ``comment_body``, ``comment_createdat`` and ``comment_score``.

Here is the first five rows of the data:

![image](https://user-images.githubusercontent.com/51396102/79226662-55057480-7e91-11ea-8c37-66f2c4c3437c.png)

## Data Collection

We used ``PRAW's`` API for the data collection. Basically, we collected a batch of 1000 posts (``rate limiting issue``) (i.e. We cannot scrape more than 1000 posts at a time for ``PRAW``) for 5 days straight to collect as much HBL related data as possible. 

**We are planning to implement better code to bypass the rate limiting while exploring Pushshift to see if it better suits our needs.*

## Data Cleaning

After we collected these batches, we realised there might be a posibility that some data has been repeated. Therefore, we used the pandas function ``drop_duplicate`` to drop the data based on the subset ``post_url`` as it is unique.

Furthermore, we used regular expressions to filter out the flairs in the post titles so that it won't be included in the word cloud below. 

Lastly, we changed the datetime from seconds to proper timing a.k.a. (year, month, day, hour, minute, seconds)

## Filtering HBL Related Posts

We basically implemented a regex function for filtering multiple keywords at the same time. The keywords that we have filtered are ``hbl``, ``home based learning`` and ``e learning``. 

All these have been set to non-case sensitive filtering. We did three conditions for the filtering which are ``post_title``, ``post_body`` and ``post_comments``. So, whenever we filter the data, the code will check for keywords that are either in title, body or comments so that we get more accurate data output.

In total, we had 132 posts relating to HBL after the strict filtering.

## Data Visualization 

We did a few wordclouds and a distribution of the 
sentiment scores. 

<p align='center' style='font-size: 25px'>HBL Post Titles</p>

![hbl_title](https://user-images.githubusercontent.com/51396102/79229085-0bb72400-7e95-11ea-8265-42c45bc88c9c.png)

<p align='center' style='font-size: 25px'>HBL Post Body</p>

![HBL_body](https://user-images.githubusercontent.com/51396102/79229835-3eade780-7e96-11ea-9bd7-0afebc0f1eca.png)

<p align='center' style='font-size: 25px'>HBL Post Comments</p>

![HBL_comments](https://user-images.githubusercontent.com/51396102/79229886-54231180-7e96-11ea-98ce-a68dc2f9abeb.png)

<p align='center' style='font-size: 25px'>HBL Sentiment Analysis</p>

![sentiment_analysis](https://user-images.githubusercontent.com/51396102/79230228-d7dcfe00-7e96-11ea-8b22-e1844a4cf479.png)

## Data Analysis

``VADER`` (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media. 

The ``Compound`` score is a metric that calculates the sum of all the lexicon ratings which have been normalized between ``-1(most extreme negative) and +1 (most extreme positive)``.

It is assumed that each ``comment`` and ``submission`` carry ``independent sentiments``. The weighted score of a comment/submission is thus the text's ``compound score`` multiplied by its ``individual score``.

A ``density plot`` (gaussian normalised) of scores are then plotted.