import pyttsx3
from reddit import *
import json
class TTS:
    def __init__(self, rate, volume, voices):
        self.engine = pyttsx3.init()

        self.rate = rate
        self.volume = volume
        self.voices = voices

        
        self.engine.setProperty('rate', self.engine.getProperty('rate')) # default 200 wpm
        self.engine.setProperty('volume', self.engine.getProperty('volume')) # default 1.0
        self.engine.setProperty('voice', self.engine.getProperty('voice')) # default english

    def to_speech(self, post_list):
        print('Converting posts to audio...')
        for x in post_list: # loop through posts and save them as audio
            print(x['title'])
            self.engine.save_to_file(x['title']+x['content'], f'{file_name_cleaner(x["title"])}.mp3')
            self.engine.runAndWait()

class Reddit_bot:
    def __init__(self, subreddit_dict=None, settings_file=None, client_id=None, client_secret=None, user_agent=None, ):
        self.settings = settings_file # load settings json first to avoid defining variables twice

        if settings_file != None:
            self.load_settings()
        elif client_id != None and client_secret != None and user_agent != None:
            self.client_id = client_id
            self.client_secret = client_secret
            self.user_agent = user_agent
        del settings_file
        global TTS
        TTS = TTS(self.rate, self.volume, self.voice)

    def load_settings(self):  
        settings = json.load(open(self.settings))  

        # API settings
        self.client_id = settings['credentials']['client_id']
        self.client_secret = settings['credentials']['client_secret']
        self.user_agent = settings['credentials']['user_agent']

        # TTS settings
        self.rate = settings['tts_settings']['rate']
        self.volume = settings['tts_settings']['volume']
        self.voice = settings['tts_settings']['voice']

        self.subreddit_dict = {}
        for subreddit in settings['subreddit_list']:
            self.subreddit_dict[settings['subreddit_list'][subreddit]['subreddit']] = int(settings['subreddit_list'][subreddit]['post_number'])
    
    def get_posts(self):
        self.post_list = []
        for subreddit in self.subreddit_dict: # loop through subreddits found in settings.json
            print(f"Getting {self.subreddit_dict[subreddit]} posts from {subreddit}...") # status message
            get_posts = api.get_posts(subreddit, self.subreddit_dict[subreddit]) # get posts from subreddit
            if get_posts == 404: # if subreddit doesn't exist
                print(f"Subreddit {subreddit} not found or no posts avalible. Skipping...")
                continue
            for x in get_posts: #remove posts from list that are stickied
                self.post_list.append(x)
            print('Done.')



def file_name_cleaner(file_name):
    # remove invalid characters from file name
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        file_name = file_name.replace(char, '')
    # replace spaces with underscores
    file_name = file_name.replace(' ', '_')
    # shorten file name if too long
    file_name = file_name[:150]+"..."
    return file_name

reddit_bot = Reddit_bot(settings_file='settings.json')
api = Reddit(reddit_bot.client_id, reddit_bot.client_secret, reddit_bot.user_agent)
reddit_bot.get_posts()
TTS.to_speech(reddit_bot.post_list)