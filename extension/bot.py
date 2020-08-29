from chdp import CHDPClient
from asyncio import gather

class Extension: pass

class DMBot(CHDPClient): 
    async def send_dm_many(self, users, content, author):
        content += f'\n보낸 사람: {author}'
        fail = []
        success = []

        async def send(m):
            try: await m.send(content)
            except: fail.append(m)
            else: success.append(m)
        
        i = 0
        corlist = []
        for m in users:
            i += 1
            if not (i % 10):
                await gather(*corlist)
                corlist = []
                i = 0
            corlist.append(send(m))
        if corlist: await gather(*corlist)

        return success, fail
