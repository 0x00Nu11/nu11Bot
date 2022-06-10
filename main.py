import discord, datetime, os
from functions import *

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} connected')
@client.event
async def on_message(message):
    if message.author==client.user or message.author.bot:
        return
    dot_command=str(message.content).split(' ')
    match dot_command[0]:
        case '.echo':
            await message.channel.send(str(message.content).replace('.echo', ''))
            await message.delete()
        case '.daily_quote':
            response=daily_quote()
            await message.channel.send(response, reference=message)
        case '.daily_poem':
            response=daily_poem()
            await message.channel.send(response, reference=message)
        case '.members':
            member_info=list([member.id, member.name] for member in message.guild.members)
            show_members=("**id**                                              **name**\n"
            +"------------------------------------------\n")
            for mid, mname in member_info:
                show_members+=f"{str(mid)}\t\t{mname}\n"
            await message.channel.send(show_members, reference=message)
        case '.info':
            msg=str(message.content).split(' ')
            info_list=[]
            for i in range(1, len(msg)):
                if '<@' in str(msg[i]):
                    tag=msg[i]
                    uid=make_ID(tag)
                    uname=list(member.name for member in message.guild.members if member.id==uid)[0]
                    ava=list(member.avatar_url for member in message.guild.members if member.id==uid)[0]
                    tcreated=list(member.created_at for member in message.guild.members if member.id==uid)[0]
                    date_created=make_time(tcreated)
                    age=get_age(tcreated, datetime.datetime.now())
                    info=(f'**Tag: **{tag}\n**Username: ** {uname}\n**ID: **{uid}\n**Date Created: **{date_created}\n'+
                    f'**Age: **{age}\n**Avatar Link: **{ava}\n{"-"*50}')
                    info_list.append(info)
            for k in range(len(info_list)):
                await message.channel.send(info_list[k], reference=message)
        case '.cwem':
            await message.channel.send(str(cwemmentize(message.content)).replace('.cwem', ''))
            await message.delete()
    
client.run(os.getenv('TOKEN'))