import requests

POST_URL = 'https://jsonplaceholder.typicode.com/posts/'

class PostSDK:
    def get_post(self, id_post):
        response = requests.get("{}{}".format(POST_URL, id_post))
        return response.json()