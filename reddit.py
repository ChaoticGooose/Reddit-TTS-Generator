import praw

class Reddit:
    def __init__(self, client_id, client_secret, password, user_agent, username): # initialize the class with the credentials
        self.reddit = praw.Reddit(
            client_id= client_id,
            client_secret=client_secret,
            password=password,
            user_agent=user_agent,
            username=username,
        )

    def get_posts(self, subreddit, number): # get the posts from the subreddit and return them as a list
        posts = []
        try: # try to get the posts
            for submission in self.reddit.subreddit(subreddit).top(time_filter="day", limit=number):
                posts.append({
                    'title': submission.title,
                    'content': submission.selftext,
                    'url': 'https://reddit.com' + submission.permalink
                })
        except Exception as e:
            print(f'ERROR: "{e}"') # print the error if there is one, Most likly a redirect error/404 error if the subreddit doesn't exist or is banned
        for post in posts: # return the posts
            yield post