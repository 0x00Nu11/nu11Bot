import discord, datetime, os, dotenv
from functions import *

dotenv.load_dotenv()
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
                    age=get_age(datetime.datetime.now(), tcreated)
                    info=(f'**Tag: **{tag}\n**Username: ** {uname}\n**ID: **{uid}\n**Date Created: **{date_created}\n'+
                    f'**Age: **{age}\n**Avatar Link: **{ava}\n{"-"*50}')
                    info_list.append(info)
            for k in range(len(info_list)):
                await message.channel.send(info_list[k], reference=message)
        case '.cwem':
            await message.channel.send(str(cwemmentize(message.content)).replace('.cwem', ''))
            await message.delete()
        case '.poll':
            emojis={
                1:'\U00000031\U0000fe0f\U000020e3',
                2:'\U00000032\U0000fe0f\U000020e3',
                3:'\U00000033\U0000fe0f\U000020e3',
                4:'\U00000034\U0000fe0f\U000020e3',
                5:'\U00000035\U0000fe0f\U000020e3',
                6:'\U00000036\U0000fe0f\U000020e3',
                7:'\U00000037\U0000fe0f\U000020e3',
                8:'\U00000038\U0000fe0f\U000020e3',
                9:'\U00000039\U0000fe0f\U000020e3',
                10:'\N{KEYCAP TEN}'
            }
            title, description, options, n_options=poll(message.content)
            if (title, description, options, n_options)==None:
                return
            poll_content=f'**{title}**\n*{description}*\n{"-"*40}\n'
            for i in range(len(options)):
                poll_content+=f'{emojis.get(i+1)} {options[i]}\n'
            bot_msg = await message.channel.send(poll_content)
            for i in range(n_options):
                print(emojis.get(i+1))
                await bot_msg.add_reaction(emojis.get(i+1))
        case '.reverse_img':
            attatch=message.attachments[0]
            url=attatch.url
            n_matches=reverse_img(url)
            if n_matches==None:
                await message.channel.send('**no matches found**', reference=message)
            for i in n_matches:
                await message.channel.send(i, reference=message)
client.run(os.getenv('TOKEN'))