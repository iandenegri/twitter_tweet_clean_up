# Local import
import json
from datetime import datetime, timezone
# Third Party import
from tweepy.models import Status
import tweepy
# Local file used to store private data like keys, etc.
import twitter_config

tweets_to_go_back = twitter_config.tweets_to_go_back

if isinstance(tweets_to_go_back, str):
    tweets_to_go_back = int(tweets_to_go_back)


class TwitterCleanUp:

    def __init__(self, tweets_to_go_back, account_user_name):
        # Set up the API object.
        self.auth = tweepy.OAuthHandler(twitter_config.consumer_key, twitter_config.consumer_secret)
        self.auth.set_access_token(twitter_config.access_token_key, twitter_config.access_token_secret)
        self.api = tweepy.API(self.auth)
        # Script set up
        self.tweets_to_go_back = tweets_to_go_back
        self.account_user_name = account_user_name
        self.old_tweets = 0
        self.newer_tweets = 0
        self.age_limit_for_retweet = 1  # This is in days


    def execute(self):
        # Get tweets
        self.fetch_tweets()
        # Clean up tweets
        self.tweet_clean_up()
        # Log results.
        print("There were " + str(self.old_tweets) + " old tweets and " + str(self.newer_tweets) + " newer tweets.")


    def fetch_tweets(self):
        # Fetch the tweets we will be iterating over
        self.public_tweets = self.api.user_timeline(count=self.tweets_to_go_back)


    def tweet_clean_up(self):
        # Iterate through grabbed tweets
        for tweet in self.public_tweets:            
            # Determine the age of the tweet
            tweet_age = (datetime.utcnow() - tweet.created_at).days
            # Do logic based on tweet age.
            if tweet_age < self.age_limit_for_retweet:
                print("This tweet is new and doesn't need to be purged. >:)")
                self.newer_tweets += 1
                continue
            elif tweet_age > 3 and tweet.retweeted == True:
                # If the tweet is older than 3 days old and it's a retweeted tweet, get rid of it (-:s
                self.api.unretweet(id=tweet.id)
                continue

script = TwitterCleanUp(tweets_to_go_back, 'taiyoushounen')
script.execute()
