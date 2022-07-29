import os

import requests
import pandas as pd


class RedditAPIRequest:
    topics = []
    topic = ''
    url = 'r/denverbroncos/top/'
    client_id = ''
    secret_key = ''
    username = ''
    password = ''
    data_frame = ''

    def process_response(self, response):
        response.replace('/n', '')

        return response


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
                           headers=headers, params={'limit': '100'})

        self.data_frame = pd.DataFrame(columns=['subreddit', 'title', 'selftext', 'upvote_ratio', 'ups', 'downs', 'score'])
        data = res.json()['data']['children']
        #print(data)
        for i in range(len(data)):
            #self.ProcessResponse(data[i]['data']['selftext'])
            #print(res.json()[i])
            self.data_frame.loc[i] = pd.Series({
                'subreddit': data[i]['data']['subreddit'],
                'title': data[i]['data']['title'],
                'selftext': self.process_response(self, data[i]['data']['selftext']),
                'upvote_ratio': data[i]['data']['upvote_ratio'],
                'ups': data[i]['data']['ups'],
                'downs': data[i]['data']['downs'],
                'score': data[i]['data']['score']
            })
        """
        for post in res.json()['data']['children']:
            # print(post['data']['title'], post['data']['selftext'])
            self.data_frame = pd.concat({
                'subreddit': post['data']['subreddit'],
                'title': post['data']['title'],
                'selftext': post['data']['selftext'],
                'upvote_ratio': post['data']['upvote_ratio'],
                'ups': post['data']['ups'],
                'downs': post['data']['downs'],
                'score': post['data']['score']
            }, ignore_index=True)"""

        """for line in range(len(self.data_frame)):
            if 'the OP*' in self.data_frame['selftext'][line] or 'the OP.*' in self.data_frame['selftext'][line] or 'NOT OP' in self.data_frame['selftext'][line]:
                print('gotcha')
                self.data_frame['selftext'][line] = self.data_frame['selftext'][line].replace(self.data_frame['selftext'][line],
                                                                    'I am not the person this happened to.*')

            if 'OP.*' in self.data_frame['selftext'][line]:
                print('got it')
                self.data_frame['selftext'][line] = self.data_frame['selftext'][line].replace(self.data_frame['selftext'][line],
                                                                    'I am not the person this happened to.')

            if '[Original]' in self.data_frame['selftext'][line]:
                print('done')
                self.data_frame['selftext'][line] = self.data_frame['selftext'][line].replace(self.data_frame['selftext'][line], '')"""

        self.data_frame.to_excel('out.xlsx')

    def clean_response(self):
        df = pd.read_excel('out.xlsx')

        for line in range(len(df)):
            """if 'the OP*' in df['selftext'][line]:
                print('gotcha')
                df['selftext'][line] = df['selftext'][line].replace('the OP*',
                                                                    'I am not the person this happened to.*')
            if 'the OP.*' in df['selftext'][line]:
                print('gotcha')
                df['selftext'][line] = df['selftext'][line].replace('the OP.*',
                                                                    'I am not the person this happened to.*')
            if 'NOT OP' in df['selftext'][line]:
                print('gotcha')
                df['selftext'][line] = df['selftext'][line].replace('NOT OP',
                                                                    'I am not the person this happened to.*')
            if 'OP.*' in df['selftext'][line]:
                print('got it')
                df['selftext'][line] = df['selftext'][line].replace('OP*',
                                                                    'I am not the person this happened to.')
                                                                    """
            if '*' in df['selftext'][line]:
                df['selftext'][line] = df['selftext'][line].replace('*', '')

            if '#' in df['selftext'][line]:
                df['selftext'][line] = df['selftext'][line].replace('#', '')
                
        df.to_excel('cleaned_out.xlsx')


if __name__ == "__main__":
    c = RedditAPIRequest
    c.clean_response(c)
