from chdp import CHDPClient
from chdp.chdp_funcs import use_func, dir_object, get_time
from asyncio import gather

from discord import (
    Message
)

class Extension: pass

class DMBot(CHDPClient): 
    async def use_cmd(self, message: Message) -> bool:
        if not message.content.startswith(self.prefix): return
        if message.author.bot: return
        if message.author.id in self.blacklist: return

        index = message.content.split(self.prefix)[1].split(' ')[0]
        try: args = message.content.split(index)[1][self.ix:].split(' ')[1:]
        except: args = []

        async def run(c):
            ext = Extension()
            setattr(ext, 'index', str(index))
            setattr(ext, 'args', list(args))
            setattr(ext, 'first_member', self.get_user_msg(message, ext))
            setattr(ext, 'first_channel', self.get_channel_msg(message, ext))
            setattr(ext, 'first_role', self.get_role_msg(message, ext))

            dirs = dir_object(c)
            if 'check' in dirs: 
                res = await use_func(c.check, self, message, ext)
                if not res: return 

            if 'user_per' in dirs:
                r = self.check_permissions(message.author, c.user_per)
                if not r and 'user_no_permission' in dirs: return await use_func(c.user_no_permission, self, message, ext) 
            if 'bot_per' in dirs:
                r = self.check_permissions(message.guild.me, c.bot_per)
                if not r and 'bot_no_permission' in dirs: return await use_func(c.bot_no_permission, self, message, ext)
            if 'cooltime' not in dirs: await use_func(c.run, self, message, ext)
            else:
                if not c.name in self.cooltimelist.keys(): self.cooltimelist[str(c.name)] = {}
                if not str(message.author.id) in self.cooltimelist[str(c.name)].keys(): 
                    self.cooltimelist[str(c.name)][str(message.author.id)] = get_time()
                    await use_func(c.run, self, message, ext)
                elif get_time() - self.cooltimelist[str(c.name)][str(message.author.id)] >= int(c.cooltime):
                    self.cooltimelist[str(c.name)][str(message.author.id)] = get_time()
                    await use_func(c.run, self, message, ext)
                else: 
                    if 'cooltime_nopass' in dirs: return await use_func(c.cooltime_nopass, self, message, ext)
            if 'after_run' in dirs: await use_func(c.after_run, self, message, ext)
        
        for m in self.cmds:
            dirs = dir_object(m)
            if 'aliases' not in dirs:
                if index == m.name: 
                    await run(m)
                    return True
            else: 
                if index in m.aliases or index == m.name: 
                    await run(m)
                    return True
        
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