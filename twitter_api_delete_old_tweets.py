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
            # # debug help
            # print(dir(tweet))
            # for attrib in tweet.__dict__:
            #     print(attrib)
            # print(type(tweet._json))
            # print(type(json.dumps(tweet._json)))
            # json_str = json.dumps(tweet._json)
            # print(json_str)
            # print("\n\n\n\n\n")    
            
            # Determine the age of the tweet
            tweet_age = (datetime.utcnow() - tweet.created_at).days
            # Do logic based on tweet age.
            if tweet_age < 3:
                print("This tweet is new and doesn't need to be purged. >:)")
                self.newer_tweets += 1
            elif tweet_age > 3 and tweet_age < 30:
                # This tweet is middle aged. My tweets will always stay but if it's a retweet that's not mine, kill it.
                print("Wow, this is middle aged. It can stay if it belongs to me or is a retweet of myself but otherwise it needs to go.")
                self.old_tweets += 1
                if tweet.retweeted == True:
                    self.api.unretweet(id=tweet.id)
            else:
                # These tweets are old. If they're not interacted with just delete them...
                print("wow this tweet is ancient!")
                if self.tweet_interaction_checker(tweet):
                    print("Well, someone interacted with this tweet or it IS interaction, might as well keep it :-)")
                else:
                    # If it's my own and has no interactions then delete it
                    self.api.destroy_status(id=tweet.id)
                self.old_tweets += 1


    def tweet_interaction_checker(self, tweet):
        """
        Checks to see if the tweet has had any interaction with it.
        Returns True if someone it's in response to someone's tweet, mentions other users, has retweets or has likes.
        If none of those conditions are met then it returns False.
        """
        if not isinstance(tweet, Status):
            print("Please only use tweets from the Tweepy Python package with this function.")
            return False
        elif not tweet.in_reply_to_status_id:
            return False
        elif not tweet.in_reply_to_user_id:
            return False    
        elif not tweet.in_reply_to_screen_name:
            return False
        elif tweet.retweet_count == 0:
            return False
        elif tweet.favorite_count == 0:
            return False
        return True

script = TwitterCleanUp(tweets_to_go_back, 'taiyoushounen')
script.execute()
