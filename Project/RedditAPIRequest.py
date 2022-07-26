import os

import requests


class RedditAPIRequest:
    topics = []
    topic = ''
    url = 'r/denverbroncos/top/'
    client_id = ''
    secret_key = ''
    username = ''
    password = ''

    def APIRequest(self):
        f = open('secret_key', "r")

        self.client_id = f.readline()
        self.secret_key = f.readline()
        self.username = f.readline()
        self.password = f.readline()
        print(self.client_id)
        print(self.secret_key)
        print(self.username)
        print(self.password)

        auth = requests.auth.HTTPBasicAuth(self.client_id, self.secret_key)
        print(auth)
        # here we pass our login method (password), username, and password
        data = {'grant_type': 'password',
                'username': self.username,
                'password': self.password}

        # setup our header info, which gives reddit a brief description of our app
        headers = {'User-Agent': 'school project/0.0.1'}

        # send our request for an OAuth token
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=headers)
        print(res)

        # convert response to JSON and pull access_token value
        TOKEN = res.json()['access_token']

        # add authorization to our headers dictionary
        headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

        # while the token is valid (~2 hours) we just add headers=headers to our requests
        requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)


if __name__ == "__main__":
    c = RedditAPIRequest
    c.APIRequest(c)
