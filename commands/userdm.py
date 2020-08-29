class Command:
    name = '디엠'
    aliases = ['유저디엠']

    async def run(self, client, message, ext):
        if ext.first_member == message.author: return
        ext.args.remove('<@!' + str(ext.first_member.id) + '>')
        try: await ext.first_member.send(' '.join(ext.args) + f'\n보낸 사람: {message.author}')
        except: await message.channel.send('유저에게 디엠 전송을 실패했습니다')
        else: await message.add_reaction('⭕')