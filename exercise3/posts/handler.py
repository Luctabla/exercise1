import aiohttp

POST_URL = "https://jsonplaceholder.typicode.com/posts/"


class PostHandler(object):
    async def get_post(self, id_post):
        uri = "{}{}".format(POST_URL, id_post)
        async with aiohttp.ClientSession() as session:
            resp = await session.get(uri)
            return await resp.json()
