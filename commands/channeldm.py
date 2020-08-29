class Command:
    name = '채널디엠'
    user_per = ['admin']

    async def run(self, client, message, ext):
        if '<#' + str(ext.first_channel.id) + '>' not in message.content: return
        ext.args.remove('<#' + str(ext.first_channel.id) + '>')
        c = ' '.join(ext.args)
        res = list(map(len, await client.send_dm_many(ext.first_channel.members, c, message.author)))
        await message.channel.send(f'성공 유저: {res[0]}\n실패 유저: {res[1]}')