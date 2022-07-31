import os

import requests
import pandas as pd
import re
from selenium import webdriver
from PIL import Image
import Screenshot
import inflect


class RedditAPIRequest:
    topics = []
    topic = ''
    client_id = ''
    secret_key = ''
    username = ''
    password = ''
    data_frame = ''
    op = [' OP.', 'OOP.', ' OOP.', ' OP', 'OOP', ' OOP']
    the_op = [' the OP.', ' the OOP.']

    def process_response(self, response):
        response.replace('/n', '')

        return response

    def get_urls(self, text):
        url = re.search("(?P<url>https?://[^\s]+)", text).group("url")
        return url

    def api_request(self):
        f = open('secret_key', "r")

        # Gotta remove that pesky /n
        self.client_id = f.readline()[0:-1]
        self.secret_key = f.readline()[0:-1]
        self.username = f.readline()[0:-1]
        self.password = f.readline()

        auth = requests.auth.HTTPBasicAuth(self.client_id, self.secret_key)

        # here we pass our login method (password), username, and password
        data = {'grant_type': 'password',
                'username': self.username,
                'password': self.password}

        # setup our header info, which gives reddit a brief description of our app
        headers = {'User-Agent': 'school project/0.0.1'}

        # send our request for an OAuth token
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=headers)

        # convert response to JSON and pull access_token value
        TOKEN = res.json()['access_token']

        # add authorization to our headers dictionary
        headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

        # while the token is valid (~2 hours) we just add headers=headers to our requests
        requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

        res = requests.get("https://oauth.reddit.com/r/BestofRedditorUpdates/top",
                           headers=headers, params={'limit': '20'})

        self.data_frame = pd.DataFrame(columns=['subreddit', 'title', 'selftext', 'upvote_ratio',
                                                'ups', 'downs', 'score', 'url'])
        data = res.json()['data']['children']
        print(data)
        #print(data)
        for i in range(len(data)):
            url = self.get_urls(self, data[i]['data']['selftext'])
            self.get_screenshot(self, url, i)
            self.data_frame.loc[i] = pd.Series({
                'subreddit': data[i]['data']['subreddit'],
                'title': data[i]['data']['title'],
                'selftext': self.process_response(self, data[i]['data']['selftext']),
                'upvote_ratio': data[i]['data']['upvote_ratio'],
                'ups': data[i]['data']['ups'],
                'downs': data[i]['data']['downs'],
                'score': data[i]['data']['score'],
                'url': url

            })

        #self.data_frame.to_excel('out.xlsx')

    def clean_response(self, file):
        df = pd.read_excel(file)
        p = inflect.engine()
        for line in range(len(df)):
            numbers = []

            if '*' in df['selftext'][line]:
                df['selftext'][line] = df['selftext'][line].replace('*', '')

            if '#' in df['selftext'][line]:
                df['selftext'][line] = df['selftext'][line].replace('#', '')

            if '$' in df['selftext'][line]:
                df['selftext'][line] = df['selftext'][line].replace('$', '')

            if '+' in df['selftext'][line]:
                df['selftext'][line] = df['selftext'][line].replace('+', '')

            numbers = [int(s) for s in df['selftext'][line].split() if s.isdigit()]
            if numbers is not None:
                for n in numbers:
                    if str(n) in df['selftext'][line]:
                        print('gotcha, replaced')
                        df['selftext'][line] = df['selftext'][line].replace(str(n), str(p.number_to_words(int(n))))

            for o in self.the_op:
                if o in df['selftext'][line]:
                    df['selftext'][line] = df['selftext'][line].replace(o, ' the person this happened to')

            for o in self.op:
                if o in df['selftext'][line]:
                    df['selftext'][line] = df['selftext'][line].replace(o, ' the person this happened to')


        print(df['selftext'])
        df.to_excel('another_cleaned_out.xlsx')

    def get_screenshot(self, url, incrementor):
        driver = webdriver.Chrome(executable_path='chromedriver.exe')
        driver.get(url)
        driver.save_screenshot('F:/Video_Resources/images/' + str(incrementor) + '.png')


if __name__ == "__main__":
    c = RedditAPIRequest
    c.clean_response(c, 'out.xlsx')