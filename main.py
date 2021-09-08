from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import telegram
from time import sleep
import praw
# from config import TOKEN, CHAT, RCLIENT_ID, RCLIENT_SECRET
import datetime
from datetime import timezone
import re
import os

TOKEN = os.environ.get('TOKEN')
CHAT = os.environ.get('CHAT')
RCLIENT_ID = os.environ.get('RCLIENT_ID')
RCLIENT_SECRET = os.environ.get('RCLIENT_SECRET')

swap_bot = telegram.Bot(TOKEN)

reddit = praw.Reddit(client_id=RCLIENT_ID, client_secret=RCLIENT_SECRET, user_agent="Agent Smith")
subreddit = reddit.subreddit("hardwareswap")

have = re.compile(r".*\[H\].*(3080\s*[Tt][Ii]|3090).*\[W\]")
want = re.compile(r".*\[W\].*3070")

time_script_started = datetime.datetime.now()
EST = timezone(datetime.timedelta(hours=-4))

for submission in subreddit.stream.submissions():
    title = submission.title
    time = submission.created_utc
    timestamp = datetime.datetime.fromtimestamp(time)
    if (time_script_started > timestamp) and (time_script_started - timestamp).seconds > 1800:
        continue
    normal_time = timestamp.astimezone(EST).strftime('%Y-%m-%d %H:%M:%S')
    print(f"New post on the subreddit on {normal_time}\nChecking if it matches the search query. Title:" )
    print(f"\t {title}")
    if have.match(title) or want.match(title):
        print("=====\nPasses the query, sending Telegram message!\n=====")
        swap_bot.send_message(CHAT, 
f"""{normal_time}
{title}
{submission.url}
""", disable_web_page_preview=True)

    print("")