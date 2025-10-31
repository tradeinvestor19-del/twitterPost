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
        logging.FileHandler('bot.log', encoding='utf-8'),
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
    
    def create_motivational_poll(self):
        """Create engaging motivational polls"""
        polls = [
            # Original polls
            {
                "question": "What motivates you more? 🔥",
                "options": ["Fear of failure", "Excitement for success", "Proving doubters wrong", "Personal growth"]
            },
            {
                "question": "Your biggest productivity killer? ⚡",
                "options": ["Social media", "Perfectionism", "Procrastination", "Overthinking"]
            },
            {
                "question": "Best time for your most important work? 🕐",
                "options": ["Early morning", "Late night", "Afternoon", "Whenever inspired"]
            },
            {
                "question": "What's your success fuel? 💪",
                "options": ["Clear goals", "Daily habits", "Strong mindset", "Support system"]
            },
            {
                "question": "How do you handle setbacks? 🚀",
                "options": ["Learn and adapt", "Push harder", "Take a break", "Seek advice"]
            },
            {
                "question": "Your ideal morning routine includes? 🌅",
                "options": ["Exercise", "Meditation", "Reading", "Planning the day"]
            },
            {
                "question": "What drives your ambition most? 🎯",
                "options": ["Freedom", "Impact", "Recognition", "Challenge"]
            },
            {
                "question": "Your go-to stress buster? 🧘",
                "options": ["Music", "Exercise", "Nature walk", "Deep breathing"]
            },
            {
                "question": "Best investment for personal growth? 📈",
                "options": ["Books/courses", "Networking", "Experiences", "Mentorship"]
            },
            {
                "question": "Your productivity secret weapon? ⚔️",
                "options": ["Time blocking", "To-do lists", "Deadlines", "Rewards system"]
            },
            {
                "question": "What keeps you going when things get tough? 💎",
                "options": ["Family/friends", "Future vision", "Past struggles", "Inner strength"]
            },
            {
                "question": "Your definition of success? 🏆",
                "options": ["Financial freedom", "Happy relationships", "Personal fulfillment", "Making a difference"]
            },
            
            # NEW EXPANDED POLLS
            {
                "question": "Which mindset shift changed your life most? 🧠",
                "options": ["Growth over fixed", "Abundance over scarcity", "Progress over perfection", "Action over intention"]
            },
            {
                "question": "Your biggest fear when starting something new? 😰",
                "options": ["Fear of failure", "Fear of judgment", "Fear of success", "Fear of the unknown"]
            },
            {
                "question": "What stops most people from achieving their dreams? 🚧",
                "options": ["Lack of belief", "Fear of hard work", "Waiting for permission", "Comparing to others"]
            },
            {
                "question": "Your ideal work environment? 🏢",
                "options": ["Total silence", "Background music", "Bustling cafe", "Nature sounds"]
            },
            {
                "question": "How do you celebrate small wins? 🎉",
                "options": ["Share with others", "Treat yourself", "Set bigger goals", "Reflect quietly"]
            },
            {
                "question": "What's your biggest time waster? ⏰",
                "options": ["Endless scrolling", "Perfectionist editing", "Overthinking decisions", "Unproductive meetings"]
            },
            {
                "question": "Your learning style preference? 📚",
                "options": ["Reading books", "Watching videos", "Hands-on practice", "Discussion groups"]
            },
            {
                "question": "What makes you feel most accomplished? ✨",
                "options": ["Helping others", "Solving problems", "Creating something", "Overcoming challenges"]
            },
            {
                "question": "Your approach to goal setting? 🎯",
                "options": ["Big audacious goals", "Small daily steps", "Monthly milestones", "Go with the flow"]
            },
            {
                "question": "What's your superpower in tough times? 🦸",
                "options": ["Staying calm", "Finding solutions", "Motivating others", "Adapting quickly"]
            },
            {
                "question": "Your ideal Friday evening? 🌙",
                "options": ["Planning next week", "Complete relaxation", "Social activities", "Personal hobbies"]
            },
            {
                "question": "What skill do you wish you learned earlier? 🎨",
                "options": ["Communication", "Financial literacy", "Time management", "Emotional intelligence"]
            },
            {
                "question": "Your biggest confidence booster? 💫",
                "options": ["Past achievements", "Positive self-talk", "Others' encouragement", "New challenges conquered"]
            },
            {
                "question": "How do you recharge your energy? 🔋",
                "options": ["Alone time", "Social connection", "Physical activity", "Creative pursuits"]
            },
            {
                "question": "Your relationship with failure? 💪",
                "options": ["Learning opportunity", "Stepping stone", "Temporary setback", "Fuel for comeback"]
            },
            {
                "question": "What would you tell your 18-year-old self? 👶",
                "options": ["Take more risks", "Trust yourself more", "Focus on relationships", "Start investing early"]
            },
            {
                "question": "Your money mindset? 💰",
                "options": ["Save first, spend later", "Invest in experiences", "Build multiple incomes", "Money follows value"]
            },
            {
                "question": "What's your decision-making style? 🤔",
                "options": ["Quick and intuitive", "Research everything", "Ask trusted advisors", "Pro/con lists"]
            },
            {
                "question": "Your biggest life lesson so far? 📖",
                "options": ["Patience pays off", "Authenticity matters", "Health is wealth", "Relationships > achievements"]
            },
            {
                "question": "How do you handle criticism? 🛡️",
                "options": ["Learn from it", "Defend your position", "Ignore the haters", "Use it as motivation"]
            },
            {
                "question": "Your ideal team dynamic? 👥",
                "options": ["Collaborative brainstorming", "Clear role division", "Friendly competition", "Supportive mentorship"]
            },
            {
                "question": "What's your creative outlet? 🎨",
                "options": ["Writing", "Visual arts", "Music/dance", "Problem solving"]
            },
            {
                "question": "Your approach to networking? 🤝",
                "options": ["Help first, ask later", "Mutual value exchange", "Authentic connections only", "Strategic relationship building"]
            },
            {
                "question": "What drives your daily habits? 🔄",
                "options": ["Long-term vision", "Immediate results", "Peer accountability", "Personal discipline"]
            },
            {
                "question": "Your weekend priority? 🏖️",
                "options": ["Rest and recovery", "Personal projects", "Family/friends time", "Adventure/exploration"]
            },
            {
                "question": "How do you measure progress? 📏",
                "options": ["Quantifiable metrics", "Feeling of growth", "Others' feedback", "Milestone achievements"]
            },
            {
                "question": "Your biggest strength in leadership? 👑",
                "options": ["Vision setting", "Team motivation", "Problem solving", "Decision making"]
            },
            {
                "question": "What's your risk tolerance? 🎲",
                "options": ["Calculated risks only", "Go big or go home", "Small experiments first", "Play it safe"]
            },
            {
                "question": "Your ideal life balance? ⚖️",
                "options": ["Work-life separation", "Integrated lifestyle", "Seasonal focus shifts", "Present moment awareness"]
            },
            {
                "question": "How do you stay motivated long-term? 🏃",
                "options": ["Visualize end goals", "Celebrate small wins", "Find new challenges", "Remember your 'why'"]
            }
        ]
        
        return random.choice(polls)

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
    
    def add_engagement_hook(self, quote):
        """Add engaging questions and call-to-actions to boost interaction"""
        
        # Context-aware hooks based on quote content
        quote_lower = quote.lower()
        
        # Success-related hooks
        if any(word in quote_lower for word in ['success', 'achieve', 'accomplish', 'win', 'victory']):
            success_hooks = [
                "🏆 What does success mean to you?",
                "🎯 What's your biggest goal right now?",
                "� Share your success story below!",
                "� What's your next milestone?",
                "✨ Tag someone crushing their goals!"
            ]
            return quote + "\n\n" + random.choice(success_hooks)
        
        # Growth/learning related hooks
        elif any(word in quote_lower for word in ['grow', 'learn', 'improve', 'better', 'change']):
            growth_hooks = [
                "🌱 What are you learning today?",
                "� How are you growing this week?",
                "🔄 What positive change are you making?",
                "� Share your biggest lesson learned!",
                "🎓 What skill are you developing?"
            ]
            return quote + "\n\n" + random.choice(growth_hooks)
        
        # Motivation/inspiration related hooks
        elif any(word in quote_lower for word in ['motivation', 'inspire', 'dream', 'goal', 'push']):
            motivation_hooks = [
                "🔥 What keeps you motivated?",
                "⚡ What's driving you today?",
                "💭 Share what inspires you most!",
                "🎪 What dream are you chasing?",
                "💪 Who's your biggest inspiration?"
            ]
            return quote + "\n\n" + random.choice(motivation_hooks)
        
        # Failure/challenge related hooks
        elif any(word in quote_lower for word in ['fail', 'challenge', 'difficult', 'struggle', 'overcome']):
            challenge_hooks = [
                "💪 What challenge are you overcoming?",
                "� How do you bounce back from setbacks?",
                "🌟 Share how you turned failure into fuel!",
                "🛡️ What's your comeback story?",
                "⚡ How do you stay strong in tough times?"
            ]
            return quote + "\n\n" + random.choice(challenge_hooks)
        
        # General engagement hooks for all other quotes
        else:
            general_hooks = [
                "💭 What do you think?",
                "👇 Share your thoughts below!",
                "🔄 RT if you agree!",
                "💪 Who needs to see this today?",
                "✨ Tag someone who inspires you!",
                "🎯 What's your take on this?",
                "💡 How does this resonate with you?",
                "🌟 What's your perspective?",
                "👑 Share this with your squad!",
                "� Let's discuss in the comments!",
                "🚀 Ready to take action?",
                "🔋 How do you apply this to your life?",
                "🎨 What's your story?",
                "📢 Drop a 💪 if you're ready!",
                "🌈 What motivates you most?"
            ]
            
            # 70% chance to add engagement hook
            if random.random() < 0.7:
                return quote + "\n\n" + random.choice(general_hooks)
        
        return quote
    
    def format_tweet(self, quote):
        """Format the quote for Twitter with proper length"""
        # Add engagement hook first
        quote_with_engagement = self.add_engagement_hook(quote)
        
        # Ensure tweet is within Twitter's character limit (280 characters)
        if len(quote_with_engagement) > 280:
            # If too long, trim the quote
            base_quote = quote
            if len(base_quote) > 277:
                base_quote = base_quote[:277] + "..."
            
            # Try to fit engagement hook if possible
            engagement_quote = self.add_engagement_hook(base_quote)
            if len(engagement_quote) <= 280:
                formatted_quote = engagement_quote
            else:
                formatted_quote = base_quote
        else:
            formatted_quote = quote_with_engagement
        
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

    def post_poll(self, poll_data):
        """Post a poll to Twitter"""
        try:
            # Twitter API v2 poll creation
            response = self.client.create_tweet(
                text=poll_data["question"],
                poll_options=poll_data["options"],
                poll_duration_minutes=1440  # 24 hours
            )
            logging.info(f"Poll posted successfully: {poll_data['question'][:50]}...")
            return True
        except tweepy.Forbidden as e:
            logging.error(f"Forbidden error posting poll: {e}")
            return False
        except tweepy.TooManyRequests as e:
            logging.error(f"Rate limit exceeded for poll: {e}")
            return False
        except tweepy.Unauthorized as e:
            logging.error(f"Unauthorized error for poll: {e}")
            return False
        except Exception as e:
            logging.error(f"Error posting poll: {e}")
            return False

    def should_post_poll(self):
        """Decide whether to post a poll or regular quote (20% chance for poll)"""
        return random.random() < 0.2  # 20% chance to post a poll
    
    def force_poll(self):
        """Force post a poll for testing purposes"""
        logging.info("Force posting a motivational poll")
        
        poll_data = self.create_motivational_poll()
        
        success = self.post_poll(poll_data)
        
        if success:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"📊 POLL Posted at {timestamp}:")
            print(f"Question: {poll_data['question']}")
            print(f"Options: {' | '.join(poll_data['options'])}")
        else:
            print("❌ Failed to post poll")
            
        return success
    
    def post_daily_content(self):
        """Main function to post daily motivational content (quotes or polls)"""
        logging.info("Starting daily content posting process")
        
        # Decide between posting a quote or a poll
        if self.should_post_poll():
            # Post a motivational poll
            poll_data = self.create_motivational_poll()
            
            success = self.post_poll(poll_data)
            
            if success:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logging.info(f"Poll posted at {timestamp}: {poll_data['question'][:100]}...")
                print(f"📊 Poll Posted at {timestamp}: {poll_data['question']}")
                print(f"Options: {', '.join(poll_data['options'])}")
            else:
                logging.error("Failed to post poll")
                print("❌ Failed to post poll")
                
        else:
            # Post a regular motivational quote
            quote = self.get_random_quote()
            formatted_tweet = self.format_tweet(quote)
            success = self.post_tweet(formatted_tweet)
            
            if success:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                has_engagement = "\n\n" in formatted_tweet
                engagement_status = "with engagement hook" if has_engagement else "without engagement hook"
                logging.info(f"Quote posted at {timestamp} {engagement_status}: {quote[:100]}...")
                print(f"✅ Quote Posted at {timestamp}: {formatted_tweet}")
            else:
                logging.error("Failed to post daily quote")
                print("❌ Failed to post quote")
        
        return success

    def post_daily_quote(self):
        """Legacy method for backwards compatibility - now calls post_daily_content"""
        return self.post_daily_content()

def main():
    """Main function to run the bot"""
    try:
        bot = MotivationalTwitterBot()
        bot.post_daily_content()
    except ValueError as e:
        logging.error(f"Configuration error: {e}")
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()