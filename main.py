import praw
import groq
import schedule
import time
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='reddit_bot.log'
)

class RedditGroqBot:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT'),
            username=os.getenv('REDDIT_USERNAME'),
            password=os.getenv('REDDIT_PASSWORD')
        )
        
        self.groq_client = groq.Client(
            api_key=os.getenv('GROQ_API_KEY')
        )
        
        self.subreddit = self.reddit.subreddit(os.getenv('TARGET_SUBREDDIT'))
        
    def generate_content(self):
        """Generate content using Groq AI"""
        try:
            # Create a prompt for the content
            prompt = """Create an engaging Reddit post about a fascinating science fact. 
            Include a catchy title and detailed explanation. Format the response as:
            Title: [title here]
            Content: [content here]"""
            
            completion = self.groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",  # or your preferred Groq model
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse the response
            response_text = completion.choices[0].message.content
            title = response_text.split('Title:')[1].split('Content:')[0].strip()
            content = response_text.split('Content:')[1].strip()
            
            return title, content
            
        except Exception as e:
            logging.error(f"Error generating content: {str(e)}")
            return None, None

    def make_post(self):
        """Create a new Reddit post"""
        try:
            title, content = self.generate_content()
            if title and content:
                submission = self.subreddit.submit(title, selftext=content)
                logging.info(f"Successfully posted: {title}")
                return submission
            else:
                logging.error("Failed to generate content")
                
        except Exception as e:
            logging.error(f"Error posting to Reddit: {str(e)}")

    def generate_comment(self, post):
        """Generate and post a comment on another post"""
        try:
            # Create a prompt based on the post content
            prompt = f"""Generate a thoughtful and relevant comment for this Reddit post:
            Title: {post.title}
            Content: {post.selftext[:500]}  # Limit content length for API
            Make the comment engaging and contributive to the discussion."""
            
            completion = self.groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            comment = completion.choices[0].message.content
            post.reply(comment)
            logging.info(f"Successfully commented on post: {post.title}")
            
        except Exception as e:
            logging.error(f"Error generating/posting comment: {str(e)}")

def run_bot():
    """Main function to run the bot"""
    bot = RedditGroqBot()
    
    # Schedule daily post
    def scheduled_post():
        bot.make_post()
        
        # Optionally comment on some recent posts
        for post in bot.subreddit.new(limit=5):
            if post.author != bot.reddit.user.me():  # Don't comment on own posts
                bot.generate_comment(post)
    
    schedule.every().day.at("12:54").do(scheduled_post)
    #schedule.every().day.at("17:00").do(scheduled_post)
    
    # Keep the script running
    while True:
        try:
            schedule.run_pending()
            time.sleep(15)  # Check schedule every
        except Exception as e:
            logging.error(f"Schedule error: {str(e)}")
            time.sleep(15)  # Wait if there's an error

if __name__ == "__main__":
    run_bot()