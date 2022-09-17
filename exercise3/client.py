import time

import aiohttp
import asyncio


class Client(object):
    host = 'http://localhost:8000{}'
    async def fetch(self, url, payload):
        async with self.session.post(url, data=payload) as response:
            return await response.read()

    async def run(self, r):
        url = self.host.format("/members_only")
        payload = {"id_post": "", "is_client": 'True'}
        tasks = []

        for i in range(r):
            payload['id_post'] = i
            task = asyncio.create_task(self.fetch(url, payload))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        print(responses[:15])
        await self.session.close()

    async def login(self):
        self.session = aiohttp.ClientSession()
        payload = {"username": "lucas", "password": "12345"}
        response = await self.session.post(self.host.format("/login"), data=payload)

    async def create_user(self):
        self.session = aiohttp.ClientSession()
        payload = {"name": "lucas", "email": "lucas@gmail.com", "username": "lucas", "password": "12345"}
        response = await self.session.post(self.host.format("/register"), data=payload)
        await self.session.close()




def start_client(count_requests):
    start = time.time()
    client = Client()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.create_user())
    loop.run_until_complete(client.login())

    loop.run_until_complete(client.run(count_requests))
    end = time.time()
    print("Running has taken: {} seconds.".format(end - start))


if __name__ == "__main__":
    correct_input = False
    while not correct_input:
        try:
            count_requests = int(input("Input how many request want to do"))
            if count_requests > 0 and count_requests < 1000:
                correct_input = True
                start_client(count_requests)
                break

        except KeyboardInterrupt:
            break
        except:
            print("Input a correct input.\n")
