# Getting Reddit Client ID and Client Secret
import os
REDDIT_CLIENT = os.environ.get('REDDIT_CLIENT')
REDDIT_SECRET = os.environ.get('REDDIT_SECRET')
REDDIT_USER_PW = os.environ.get('REDDIT_USER_PW')
REDDIT_USER_NAME= os.environ.get('REDDIT_USER_NAME')

# Testing if the config exists
assert REDDIT_CLIENT != None; assert REDDIT_SECRET != None; assert REDDIT_USER_NAME != None; assert REDDIT_USER_PW != None
print(f'This is your client_id: {REDDIT_CLIENT}.\nThis is your client_secret: {REDDIT_SECRET}.')
print(f'This is your reddit username: {REDDIT_USER_NAME}.\nThis is your reddit password: {REDDIT_USER_PW}.\n')

# Importing libraries for scraping
import pandas as pd
import praw
import time

# Import Datapack
import data_dict
reddit_data = data_dict.reddit_data


# Reddit API Login
def reddit_api_login(REDDIT_CLIENT, REDDIT_SECRET, REDDIT_USER_NAME, REDDIT_USER_PW):
  """ Reddit API Login Credentials.
  Parameters:
  REDDIT_CLIENT (str): Reddit Client ID,
  REDDIT_SECRET (str): Reddit Client Secret,
  REDDIT_USER_NAME (str): Reddit Username,
  REDDIT_USER_PW (str): Reddit User Password
  
  Returns:
  class: praw.reddit.Reddit
  """
  reddit = praw.Reddit(client_id=REDDIT_CLIENT,
                       client_secret=REDDIT_SECRET,
                       password=REDDIT_USER_PW,
                       user_agent='SGExams Reddit Scraper',
                       username=REDDIT_USER_NAME)
  return reddit

# Reddit User
REDDIT_USER = reddit_api_login(REDDIT_CLIENT, REDDIT_SECRET, REDDIT_USER_NAME, REDDIT_USER_PW)

# Subreddit
SGEXAMS = REDDIT_USER.subreddit("SGExams")

# Sorting
post_counter = 1
for post in SGEXAMS.new(limit=10):
  comment_counter = 1

  try:
    print(f'SGExams Subreddit Post {post_counter}\n')
    print(f'Reddit Post Title: {post.title}\n')
    reddit_data['post']['title'].append(post.title)
    print(f'Flair: {post.link_flair_text}\n')
    reddit_data['post']['flair'].append(post.link_flair_text)
    print(f'Created At (UTC): {post.created_utc}\n')
    reddit_data['post']['created_at'].append(post.created_utc)
    print('Post Content:\n')
    print(f'{post.selftext}\n')
    reddit_data['post']['body'].append(str(post.selftext))
    print(f'Post URL: {post.url}\n')
    reddit_data['post']['url'].append(post.url)
    print(f'Post Score: {post.score}\n')
    reddit_data['post']['score'].append(float(post.score))

  except:
    print('Error Encountered During Post Scraping')
    continue

  print('Comment Section:\n')
  temp_comment = []
  temp_comment_createdat = []
  temp_comment_scores = []
  post.comments.replace_more(limit=None)
  for comment in post.comments.list():
    print(f'Comment {str(comment_counter)}:\n')
    print(f"{str(comment.body)}\n")
    temp_comment.append(str(comment.body))
    print(f'Comment {comment_counter} was created at {comment.created_utc}\n')
    temp_comment_createdat.append(comment.created_utc)
    print(f'Comment {comment_counter} Score: {comment.score}')
    temp_comment_scores.append(float(comment.score))
    print()
    comment_counter += 1
    
    

  reddit_data['comment']['body'].append(list(temp_comment))
  reddit_data['comment']['created_at'].append(list(temp_comment_createdat))
  reddit_data['comment']['score'].append(list(temp_comment_scores))
  time.sleep(0.1)
  post_counter += 1

reddit_df = pd.DataFrame({'post_title': reddit_data['post']['title'],
                          'post_flair': reddit_data['post']['flair'],
                          'post_created_at': reddit_data['post']['created_at'],
                          'post_body': reddit_data['post']['body'],
                          'post_url': reddit_data['post']['url'],
                          'post_score': reddit_data['post']['score'],
                          'comment_body': reddit_data['comment']['body'],
                          'comment_created_at': reddit_data['comment']['created_at'],
                          'comment_score': reddit_data['comment']['score']})

reddit_df = reddit_df.drop_duplicates(subset=['post_url'], keep='first')

reddit_df.to_csv('./storage/test.csv', index=False)