import tweepy
import json
import random
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

class MotivationalTwitterBot:
    def __init__(self):
        """Initialize the Twitter bot with API credentials"""
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        # Validate credentials
        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            raise ValueError("Missing Twitter API credentials in environment variables")
        
        # Initialize Twitter API client
        self.client = tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
            wait_on_rate_limit=True
        )
        
        logging.info("Twitter bot initialized successfully")
    
    def load_quotes(self):
        """Load quotes from JSON file"""
        try:
            with open('data/quotes.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data['quotes']
        except FileNotFoundError:
            logging.error("Quotes file not found")
            return []
        except json.JSONDecodeError:
            logging.error("Error parsing quotes JSON file")
            return []
    
    def get_random_quote(self):
        """Get a random motivational quote"""
        quotes = self.load_quotes()
        if not quotes:
            return "Stay motivated and keep pushing forward! 💪 #Motivation #Success"
        
        return random.choice(quotes)
    
    def add_hashtags(self, quote):
        """Add relevant hashtags to the quote"""
        hashtags = [
            "#Motivation", "#Inspiration", "#Success", "#Mindset", 
            "#Goals", "#Positivity", "#GrowthMindset", "#DailyMotivation",
            "#Quotes", "#Wisdom", "#Achievement", "#Believe"
        ]
        
        # Select 2-3 random hashtags to avoid overwhelming the tweet
        selected_hashtags = random.sample(hashtags, random.randint(2, 3))
        
        # Check if quote already has hashtags
        if not any(tag in quote for tag in hashtags):
            quote += " " + " ".join(selected_hashtags)
        
        return quote
    
    def format_tweet(self, quote):
        """Format the quote for Twitter with proper length and hashtags"""
        # Add hashtags
        formatted_quote = self.add_hashtags(quote)
        
        # Ensure tweet is within Twitter's character limit (280 characters)
        if len(formatted_quote) > 280:
            # If too long, try without all hashtags and just add one
            base_quote = quote
            if len(base_quote) > 250:  # Leave room for hashtag
                base_quote = base_quote[:247] + "..."
            formatted_quote = base_quote + " #Motivation"
        
        return formatted_quote
    
    def post_tweet(self, message):
        """Post a tweet to Twitter"""
        try:
            response = self.client.create_tweet(text=message)
            logging.info(f"Tweet posted successfully: {message[:50]}...")
            return True
        except tweepy.Forbidden as e:
            logging.error(f"Forbidden error: {e}")
            return False
        except tweepy.TooManyRequests as e:
            logging.error(f"Rate limit exceeded: {e}")
            return False
        except tweepy.Unauthorized as e:
            logging.error(f"Unauthorized error: {e}")
            return False
        except Exception as e:
            logging.error(f"Error posting tweet: {e}")
            return False
    
    def post_daily_quote(self):
        """Main function to post a daily motivational quote"""
        logging.info("Starting daily quote posting process")
        
        # Get a random quote
        quote = self.get_random_quote()
        
        # Format the tweet
        formatted_tweet = self.format_tweet(quote)
        
        # Post the tweet
        success = self.post_tweet(formatted_tweet)
        
        if success:
            logging.info("Daily motivational quote posted successfully!")
            print(f"✅ Posted: {formatted_tweet}")
        else:
            logging.error("Failed to post daily quote")
            print("❌ Failed to post quote")
        
        return success

def main():
    """Main function to run the bot"""
    try:
        bot = MotivationalTwitterBot()
        bot.post_daily_quote()
    except ValueError as e:
        logging.error(f"Configuration error: {e}")
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()