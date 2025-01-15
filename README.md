
# Daily AI Content Generation Reddit Bot

This project implements a Reddit bot that generates AI-powered content using Groq AI and posts it to a specified subreddit on a daily schedule. The bot uses the PRAW (Python Reddit API Wrapper) for Reddit interactions and Groq AI for content generation.








## Run Locally

Clone the project

```bash
  git clone https://github.com/thorbus/Synkrit_AI_assignment.git
```
install required libraries
```bash
  pip install groq praw requests schedule python-dotenv
```

Go to the project directory

Run App

```bash
      python .\main.py
```


## Environment Variables

# Groq API Credentials
GROQ_API_KEY=your_groq_api_key

# Reddit API Credentials
REDDIT_CLIENT_ID=your_reddit_client_id

REDDIT_CLIENT_SECRET=your_reddit_client_secret

REDDIT_USERNAME=your_reddit_username

REDDIT_PASSWORD=your_reddit_password

REDDIT_USER_AGENT=your_user_agent

# here we have used target subreddit as r/test 

TARGET_SUBREDDIT="test" 



## Features

Content Generation

The bot uses the Groq AI API to generate text-based content based on a specified prompt. The bot sends a prompt to the Groq AI API and receives an AI-generated response, which is then posted on Reddit.
Scheduled Posts

The bot uses the schedule library to post content daily at a user-specified time. The time can be customized in the script.
Posting to Reddit

The bot uses the PRAW library to authenticate with Reddit and post the generated content. It posts to a subreddit defined in the code (currently set to "test" for testing purposes).
Bonus Feature - Comment Generation

The bot can also generate comments and reply to existing Reddit posts. This feature is optional and can be activated by defining a post URL.
Logging

The bot logs important activities and errors to a file called reddit_bot.log. This includes:

    Starting the bot
    Posting content to Reddit
    Any errors encountered during content generation or posting

You can view the log file to monitor the bot's activities.
