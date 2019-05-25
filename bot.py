import discord
import asyncio
import json
import re
import os

#((?<=\=\=)\w+)

from framework.dbprocess import DBProcess
from core import Core

#Lmao

auth_json_path = 'auth.json'

if os.path.isfile(auth_json_path):
    auth_file = open(auth_json_path)
    auth_str = auth_file.read()
    auth_data = json.loads(auth_str)
    bot_name = auth_data['bot_name']
    token = auth_data['token']
else:
    bot_name = os.environ["BOT_NAME_DISCORD"]
    token = os.environ["TOKEN_DISCORD"]

client = discord.Client()
#dbprocessor = DBProcess()
core = Core()
commands_list = json.loads(open('commands.json').read())

command_regex = r"((?<=\=\=)\w+)|(((?<=-)\w+) (\w+))|((?<=-)\w+)"
    
on_watch_users = []

embed_col = {
    'debug' : 0xffff44,
    'generate_success' : 0x10ff10
}

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    global on_watch_users
    # Prevents recursive parsing
    if message.author == client.user:
        return

    # Checks if the message is a command. If it is, then parse the command.
    if message.content.startswith('=='): # Is a command
        tmp = re.findall(command_regex, message.content)
        if len(tmp) >= 1:
            command = tmp[0][0]
            commandargs = [(findings[4],'') if findings[1]=='' else (findings[2],findings[3]) for findings in tmp[1:]]
            if command!='':
                await message.channel.send(f"Jadi ente pengen nyuruh saya **`{command}`**?")
            else:
                print("IMPROPER command")
                return
            if len(commandargs)>0:
                await message.channel.send("Terus ini juga, gitu?:\n{}".format('\n'.join([str(x) for x in commandargs])))
        else:
            print("ERROR! No commands given")
            await message.channel.send("***Yang jelas napa, cok.***")

        ######

        # Commands that takes exactly only one keyword args
        if command in commands_list['kw_args_exactly_one']:
            if len(commandargs)==0: # Filters if there is no arguments passed
                print("NO ARGUMENTS PASSED FOR kw_args_exactly_one")
                await message.channel.send(f"{command} itu command yang nerima satu keyword argument dan ***anda dengan tidak becusnya lupa menulisnya juga***")

            if command=='debug': # debug command, 
                if commandargs[0][0] not in commands_list['kw_args_exactly_one'][command]: # Filters out debug commands
                    print("WRONG ARGUMENTS FOR debug")
                    await message.channel.send(f"command `debug` nggak kenal argumen {commandargs[0][0]}")
                if commandargs[0][0] == 'fetch_all_universities': # commands_list['kw_args_exactly_one'][command][0]
                    await message.channel.send(embed = discord.Embed(\
                        title="Ini list universitas, oniisan.",\
                        description='\n'.join(DBProcess().all_universities()),\
                        color=embed_col['debug'])\
                    )
                elif commandargs[0][0] == 'fetch_all_majors': # commands_list['kw_args_exactly_one'][command][1]
                    await message.channel.send(embed = discord.Embed(\
                        title="Prodi-prodi terdaftar di KRS",\
                        description='\n'.join(DBProcess().all_majors()),\
                        color=embed_col['debug'])\
                    )
                elif commandargs[0][0] == 'fetch_all_courses' : # commands_list['kw_args_exactly_one'][command][2]
                    await message.channel.send(embed = discord.Embed(\
                        title="Semua matkul yang ada di KRS",\
                        description='\n'.join(DBProcess().all_courses()),\
                        color=embed_col['debug'])\
                    )
                elif commandargs[0][0] == 'dump_embed' : # commands_list['kw_args_exactly_one'][command][3]
                    embed = discord.Embed(\
                        title="this is discord embed.",\
                        description="embed description",\
                        color=0xffff44)
                    embed.add_field(\
                        name="field1",\
                        value='owo whats this',\
                        inline=True)
                    embed.add_field(\
                        name="field2",\
                        value=f'im going to say the n-word to {message.author.mention}',\
                        inline=False)
                    await message.channel.send(f"{message.author.mention}", embed=embed)

        # Commands that takes one or more arguments
        elif command in commands_list['zero_or_more_args']:
            if len(commandargs)==0: # Filters if there is no arguments passed
                print("NO ARGUMENTS PASSED FOR zero_or_more_args")
                await message.channel.send(f"{command} itu command yang nerima **setidaknya** satu keyword argument dan ***anda dengan tidak becusnya lupa menulisnya juga***")

            if command=='krs':
                if commandargs[0][0] == 'generate':
                    if commandargs[0][1].isdigit(): card = core.get_random_study_plan(int(commandargs[0][1]))
                    else: card = core.get_random_study_plan()
                    await message.channel.send(embed = discord.Embed(\
                        title=f"Kartu Rencana Studi",\
                        description=str(card),\
                        color=embed_col['generate_success'])\
                    )

        # Commands that takes exactly treats the rest of the string as a string argument
        elif command in commands_list['literal_args']:
            literal_arg = message.content[2+len(command):]
            if len(literal_arg) > 1: # Filters if there is any argument
                literal_arg = literal_arg[1:]
                if command == commands_list['literal_args'][0]: # say command,
                    await message.channel.send(literal_arg)
                ##elif command == commands_list['literal_args'][1]: # sayd command,
                ##    message.channel.send(literal_arg)
                ##    await message()
            else:
                print("NO LITERAL STRING ARGUMENTS PASSED FOR literal_args!")
                await message.channel.send(f"***IYA KALAU PENGEN {command} ARGUMENNYA TULIS JUGA***")

        # It is not a command the bot understands
        else: 
            print("INVALID command")
            await message.channel.send("*Ga ngerti ah*")
        return

    #######

    # Free text responses  
    if message.content.startswith('OwO_Cebong'):
        await message.channel.send('Jancok')
    if message.content.startswith('OwO_Kampret'):
        await message.channel.send('Delusional')
    if 'anjing' in message.content:
        await message.channel.send("Santai, kontol.")
        on_watch_users.append(message.author)

@client.event
async def on_typing(channel, user, when):
    global on_watch_users
    if user in on_watch_users:
        await channel.send(f"WOE WOE MAO NGETIK APA LU TOD? <@{user.id}>")
        on_watch_users.remove(user)
        await channel.trigger_typing()

#@client.event
#async def on_message(message):
#    if message.content.startswith('!test'):
#        counter = 0
#        tmp = await client.send_message(message.channel, 'Calculating messages...')
#        async for log in client.logs_from(message.channel, limit=100):
#            if log.author == message.author:
#                counter += 1
#
#        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
#    elif message.content.startswith('!sleep'):
#        await asyncio.sleep(5)
#        await client.send_message(message.channel, 'Done sleeping')

client.run(token)



