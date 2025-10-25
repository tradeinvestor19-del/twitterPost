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
    
    def load_used_quotes(self):
        """Load the list of recently used quotes"""
        try:
            with open('data/used_quotes.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get('used_quotes', [])
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            logging.warning("Error parsing used quotes file, starting fresh")
            return []
    
    def save_used_quotes(self, used_quotes):
        """Save the list of recently used quotes"""
        try:
            # Ensure data directory exists
            os.makedirs('data', exist_ok=True)
            
            data = {'used_quotes': used_quotes}
            with open('data/used_quotes.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error saving used quotes: {e}")
    
    def get_random_quote(self):
        """Get a random motivational quote without recent repeats"""
        quotes = self.load_quotes()
        if not quotes:
            return "Stay motivated and keep pushing forward! 💪 #Motivation #Success"
        
        used_quotes = self.load_used_quotes()
        
        # Find quotes that haven't been used recently
        available_quotes = [quote for quote in quotes if quote not in used_quotes]
        
        # If we've used all quotes, reset the used list but keep last 10 to avoid immediate repeats
        if not available_quotes:
            logging.info("All quotes used, resetting with buffer to prevent immediate repeats")
            used_quotes = used_quotes[-10:] if len(used_quotes) >= 10 else []
            available_quotes = [quote for quote in quotes if quote not in used_quotes]
        
        # Select a random quote from available ones
        selected_quote = random.choice(available_quotes)
        
        # Add to used quotes and keep only last 50 to manage memory
        used_quotes.append(selected_quote)
        used_quotes = used_quotes[-50:]  # Keep only last 50 used quotes
        
        # Save updated used quotes
        self.save_used_quotes(used_quotes)
        
        logging.info(f"Selected quote (not used in last {len(used_quotes)} posts)")
        return selected_quote
    
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
        
        # Get a random quote (with duplicate prevention)
        quote = self.get_random_quote()
        
        # Format the tweet
        formatted_tweet = self.format_tweet(quote)
        
        # Post the tweet
        success = self.post_tweet(formatted_tweet)
        
        if success:
            # Log the posted quote with timestamp for tracking
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"Quote posted at {timestamp}: {quote[:100]}...")
            print(f"✅ Posted at {timestamp}: {formatted_tweet}")
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