class Command:
    name = '전체디엠'
    aliases = ['매스디엠', '모두디엠']
    user_per = ['owner']

    async def run(self, client, message, ext):
        res = list(map(len, await client.send_dm_many(message.guild.members, ' '.join(ext.args), message.author)))
        await message.channel.send(f'성공 유저: {res[0]}\n실패 유저: {res[1]}')