class Command:
    name = '역할디엠'
    user_per = ['admin']

    async def run(self, client, message, ext):
        if not ext.first_role: return
        ext.args.remove('<@&' + str(ext.first_role.id) + '>')
        c = ' '.join(ext.args)
        res = list(map(len, await client.send_dm_many(ext.first_role.members, c, message.author)))
        await message.channel.send(f'성공 유저: {res[0]}\n실패 유저: {res[1]}')