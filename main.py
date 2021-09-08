from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import telegram
from time import sleep
import praw
# from config import TOKEN, CHAT, RCLIENT_ID, RCLIENT_SECRET
import datetime
import re
import os

TOKEN = os.environ.get('TOKEN')
CHAT = os.environ.get('CHAT')
RCLIENT_ID = os.environ.get('RCLIENT_ID')
RCLIENT_SECRET = os.environ.get('RCLIENT_SECRET')

swap_bot = telegram.Bot(TOKEN)

reddit = praw.Reddit(client_id=RCLIENT_ID, client_secret=RCLIENT_SECRET, user_agent="Agent Smith")
subreddit = reddit.subreddit("hardwareswap")

have = re.compile(r".*\[H\].*(3080\s*[Tt][Ii]|3090).*[W]")
want = re.compile(r".*\[W\].*3070")
want = re.compile(r".*")

time_script_started = datetime.datetime.now()

for submission in subreddit.stream.submissions():
    title = submission.title
    time = submission.created_utc
    timestamp = datetime.datetime.fromtimestamp(time)
    if (time_script_started > timestamp) and (time_script_started - timestamp).seconds > 180:
        continue
    normal_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    if have.match(title) or want.match(title):
        time = submission.created_utc
        timestamp = datetime.datetime.fromtimestamp(time)
        normal_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        swap_bot.send_message(CHAT, 
f"""{normal_time}
{title}
{submission.url}
""", disable_web_page_preview=True)