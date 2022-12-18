import pyttsx3
from reddit import *
import json

# init tts engine
engine = pyttsx3.init()

def get_settings():
    print('No settings.json file found or disabled. Please enter your settings below:')

    # credentials
    client_id = input('Enter client_id: ')
    client_secret = input('Enter client_secret: ')
    user_agent = input('Enter user_agent: ')
    username = input('Enter username: ')
    password = input('Enter password: ')

    # reddit post settings
    while True:
        try:
            loop = int(input('Enter number of subreddits: '))
            if loop < 1:
                raise ValueError
        except ValueError:
            print('Invalid number. Please enter a number greater than 0.')
            continue
        break

    for i in range(loop):
        subreddit = input('Enter subreddit: ') 
        while True:
            try:
                number = int(input('Enter number of posts: '))
                if number < 1:
                    raise ValueError
            except ValueError:
                print('Invalid number. Please enter a number greater than 0.')
                continue
            break

        subreddit_dict[subreddit] = number

    # tts settings
    rate = engine.getProperty('rate') # default 200 wpm
    volume = engine.getProperty('volume') # default 1.0
    voices = engine.getProperty('voices') # default 1

    # attempt to set settings
    print('Current Rate: ', rate)
    try:
        engine.setProperty('rate', int(input('Enter rate: '))) 
    except ValueError:
        print('Invalid rate. Continueing using default rate.')

    print('Current Volume: ', volume)
    try:
        engine.setProperty('volume', float(input('Enter volume: ')))
    except ValueError:
        print('Invalid volume. Continueing using default volume.')

    try:
        engine.setProperty('voice', voices[int(input('Enter voice: '))].id)
    except:
        print('Invalid voice. Continueing using default voice.')

    # delete variables
    del rate, volume, voices

    return client_id, client_secret, user_agent, username, password, subreddit, number

try:
    settings = json.load(open('settings.json'))

    if not settings['enabled']:
        client_id, client_secret, user_agent, username, password, subreddit, number = get_settings()
    else:
        # collect credentials
        client_id = settings['credentials']['client_id']
        client_secret = settings['credentials']['client_secret']
        user_agent = settings['credentials']['user_agent']
        username = settings['credentials']['username']
        password = settings['credentials']['password']

        # collect subreddits
        subreddit_dict = {}
        for subreddit in settings['subreddit_list']:
            subreddit_dict[settings['subreddit_list'][subreddit]['subreddit']] = int(settings['subreddit_list'][subreddit]['post_number'])

        # collect tts settings
        rate = settings['tts_settings']['rate']
        volume = settings['tts_settings']['volume']
        voice = settings['tts_settings']['voice']

        # set tts settings
        rate_active = engine.getProperty('rate') # default 200 wpm
        volume_active = engine.getProperty('volume') # default 1.0
        voices = engine.getProperty('voices') # default 1

        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
        engine.setProperty('voice', voices[voice].id)

        # delete variables
        del settings, rate, volume, voice, rate_active, volume_active, voices, subreddit

except FileNotFoundError: # if json doesn't exist request settings
    client_id, client_secret, user_agent, username, password, subreddit, number = get_settings()

# create reddit object with credentials (see reddit.py)
reddit = Reddit(client_id, client_secret, password, user_agent, username)
# delete now redundant credential variables
del client_id, client_secret, password, user_agent, username

post_list = list()

for subreddit in subreddit_dict: # loop through subreddits found in settings.json
        print(f"Getting {subreddit_dict[subreddit]} posts from {subreddit}...") # status message
        for x in reddit.get_posts(subreddit, subreddit_dict[subreddit]): # get posts from subreddit and remove the items from recived list  
            post_list.append(x)
        print('Done.')

print('Converting posts to audio...')
for post in post_list: # loop through posts and save them as audio
    engine.save_to_file(post['title']+post['content'], f"{post['title']}.mp3")
    engine.runAndWait()