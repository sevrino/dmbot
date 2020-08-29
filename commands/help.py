from discord import Embed

class Command:
    name = '도움'
    use = '도움 <명령어>'
    anything = True

    async def run(self, client, message, ext):
        cmd = ''.join(ext.args)
        if not cmd: await self.allhelp(client, message)
        else: await self.cmdhelp(client, message, cmd)

    async def allhelp(self, client, message): 
        await message.channel.send(embed = Embed(title = '도움', description = '**,** '.join([f'`{a}`' for a in [b.name for b in client.cmds]])))

    async def cmdhelp(self, client, message, cmd):
        cs = list(filter(lambda x: cmd == x.name, client.cmds))
        if not cs: return await message.channel.send('명령어가 없습니다')
        c = cs[0]
        d = dir(c)
        if 'aliases' in d: al = '**,** '.join([f'`{a}`' for a in c.aliases])
        else: al = '없습니다'
        if 'use' in d: use = client.prefix + c.use
        else: use = client.prefix + c.name
        if 'help' in d: help = c.help
        else: help = '없습니다'
        if 'cooltime' in d: cool = f'{c.cooltime}초'
        else: cool = '0초'
        await message.channel.send(embed = Embed(title = f'명령어 {c.name} 정보', description = f'**Aliases:** {al}\n**사용방법:** `{use}`\n**설명:** `{help}`\n**쿨타임:** `{cool}`'))
