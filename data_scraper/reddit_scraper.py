# Getting Reddit Client ID and Client Secret
import config
reddit_credentials = config.reddit_credentials

REDDIT_CLIENT = reddit_credentials['client_id']
REDDIT_SECRET = reddit_credentials['client_secret']
REDDIT_USER_PW = reddit_credentials['user_pw']
REDDIT_USER_NAME= reddit_credentials['username']

# Testing if the config exists
assert REDDIT_CLIENT != None; assert REDDIT_SECRET != None; assert REDDIT_USER_NAME != None; assert REDDIT_USER_PW != None
print(f'This is your client_id: {REDDIT_CLIENT}.\nThis is your client_secret: {REDDIT_SECRET}.')
print(f'This is your reddit username: {REDDIT_USER_NAME}.\nThis is your reddit password: {REDDIT_USER_PW}.\n')

# Importing libraries for scraping
import pandas as pd
import praw
import time

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

# Reddit Data
reddit_posts = []
reddit_comments = []

# Sorting
post_counter = 1
for post in SGEXAMS.new(limit=1000):
  comment_counter = 1
  try:
    print(f'SGExams Subreddit Post {post_counter}\n')
    print(f'Reddit Post Title: {post.title}\n')
    print(f'Flair: {post.link_flair_text}\n')
    print(f'Created At (UTC): {post.created_utc}\n')
    print('Post Content:\n')
    print(f'{post.selftext}\n')
    print(f'Post URL: {post.url}\n')
    print(f'Post Score: {post.score}\n')
    reddit_posts.append([post.title, post.link_flair_text, post.created_utc, post.selftext, post.url, post.score])
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
    print(f'{str(comment.body)}\n')
    temp_comment.append(str(comment.body))
    print(f'Comment {comment_counter} was created at {comment.created_utc}\n')
    temp_comment_createdat.append(comment.created_utc)
    print(f'Comment {comment_counter} Score: {comment.score}')
    temp_comment_scores.append(float(comment.score))
    print()
    comment_counter += 1

  reddit_comments.append([temp_comment, temp_comment_createdat, temp_comment_scores])  

  post_counter += 1

reddit_post_df = pd.DataFrame(reddit_posts, columns=['post_title', 'post_flair', 'post_created_at', 'post_body', 'post_url', 'post_score'])
reddit_comment_df = pd.DataFrame(reddit_comments, columns=['comment_body', 'comment_created_at', 'comment_score'])

reddit_post_info = pd.concat([reddit_post_df, reddit_comment_df], axis=1)
reddit_post_info.to_csv('./storage/testidk.csv', index=False)