import discord
from discord.ext import commands
import random
import asyncio

players = {}

status = "Commands: -help"
cmd_prefix = "-"

bot = commands.Bot(command_prefix=cmd_prefix, description="Made by SendPacket")

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name=status))
    print('------------------')
    print('Bot loaded & ready')
    print(bot.user.id)
    print('------------------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    else:
        if message.content == cmd_prefix+"help":
            if message.author.server_permissions.administrator:
                embed = discord.Embed(title="▶ Administrator Commands b.3", description="", color=0x42a1f4)
                embed.add_field(name="Spam", value="Sends a message multiple times (syntax: <times> <txt>)", inline=False)
                embed.add_field(name="Clear", value="Clears the text channel (syntax: <lines>)", inline=False)
                embed.add_field(name="Music", value="Basic MusicBot (syntax: <play/stop/pause/resume> <url>)", inline=False)
                embed.add_field(name="Separate", value="Divides the characters of a text in spaces (syntax: <space> <txt>)", inline=False)
                embed.add_field(name="Shutdown", value="Closes the bot", inline=False)
                await bot.send_message(message.channel, embed=embed)   
            else:
                embed = discord.Embed(title="▶ Member Commands b.3", description="", color=0x42a1f4)
                embed.add_field(name="Music", value="Basic MusicBot (syntax: play <url>)", inline=False)
                embed.add_field(name="Separate", value="Divides the characters of a text in spaces (syntax: <space> <txt>)", inline=False)
                await bot.send_message(message.channel, embed=embed)   

        elif message.content.startswith(cmd_prefix+"spam"):
            if message.author.server_permissions.administrator:
                n = int(message.content.split()[1])
                for i in range(n): 
                    spam_message = ' '.join(message.content.split()[2:])
                    await bot.send_message(message.channel, spam_message)  
            else:
                await bot.send_message(message.channel, "You have to be an administrator to use that command")

        elif message.content.startswith(cmd_prefix+"clear"):
            try:
                if message.author.server_permissions.administrator:
                    if message.channel.type == discord.ChannelType.text:
                        mgs = []
                        async for x in bot.logs_from(message.channel, limit= int(message.content.split()[1])):
                            mgs.append(x)
                        await bot.delete_messages(mgs)
                        await bot.send_message(message.channel, "Chat cleaned!")
                    else:
                        await bot.send_message(message.channel, "That channel is not a text channel!")
                else:
                    await bot.send_message(message.channel, "You have to be an administrator to use that command")
            except Exception:
                await bot.send_message(message.channel, "Wrong usage of that command. Please use the correct syntax (clear <lines>)")   

        elif message.content.startswith(cmd_prefix+"separate"):
            n = int(message.content.split()[1])
            start_message = ''.join(message.content.split()[2:])
            final_message = ""
            for o in range(len(start_message)):
                final_message += start_message[o]
                for i in range(n): 
                    final_message += " "
            await bot.send_message(message.channel, final_message)   

        elif message.content == cmd_prefix+"shutdown":
            if message.author.server_permissions.administrator:
                await bot.send_message(message.channel, "Bye!")  
                await bot.logout()
            else:
                await bot.send_message(message.channel, "You have to be an administrator to use that command")

        elif message.content.startswith(cmd_prefix+"music"):
            try:
                args1 = message.content.split()[1]
                if args1 == "play":
                        p_url = ' '.join(message.content.split()[2:])
                        if p_url.startswith("https://www.youtube.com"):
                            try:
                                already_playing = False

                                if message.server.id in players:
                                    if not(players[message.server.id].is_done()):
                                        already_playing = True
                                        await bot.send_message(message.channel, "A song is already being played!")
                                
                                if not(already_playing):
                                    try:
                                        players[message.server.id].stop()
                                        players[message.server.id] = None
                                    except Exception:
                                        pass

                                    voice = None

                                    if bot.is_voice_connected(message.server):
                                        voice = bot.voice_client_in(message.server)
                                    else:
                                        voice = await bot.join_voice_channel(channel)

                                    player = await voice.create_ytdl_player(p_url)    
                                    players[message.server.id] = player
                                    players[message.server.id].start()
                                    await bot.send_message(message.channel, "Song added!")

                            except discord.ClientException:
                                await bot.send_message(message.channel, "You're not in a voice channel or a download error occured!") 
                        else:
                            await bot.send_message(message.channel, "Please write the youtube link of a valid video!")
                else:
                    try: 
                        if args1 == "pause":
                            if message.author.server_permissions.administrator:
                                players[message.server.id].pause()
                                await bot.send_message(message.channel, "Song paused!")  
                            else:
                                await bot.send_message(message.channel, "You have to be an administrator to use that command")
                        elif args1 == "resume":
                            if message.author.server_permissions.administrator:
                                players[message.server.id].resume()
                                await bot.send_message(message.channel, "Song resumed!")  
                            else:
                                await bot.send_message(message.channel, "You have to be an administrator to use that command")
                        elif args1 == "stop":
                            if message.author.server_permissions.administrator:
                                players[message.server.id].stop()
                                players[message.server.id] = None
                                await bot.send_message(message.channel, "Song removed!")
                            else:
                                await bot.send_message(message.channel, "You have to be an administrator to use that command")
                        else:
                            await bot.send_message(message.channel, "Wrong usage of that command. Please use the correct syntax (music <play/stop/pause/resume> <url>) ")                         
                    except Exception:
                        await bot.send_message(message.channel, "Nothing is being played!")             
            except discord.DiscordException:
                await bot.send_message(message.channel, "Internal Error") 
            except IndexError:
                await bot.send_message(message.channel, "Wrong usage of that command. Please use the correct syntax (music <play/stop/pause/resume> <url>) ")                         
        
            
        
@bot.event
async def on_command_error(ctx, error): 
    if isinstance(error, commands.CommandNotFound):
        return

bot.remove_command("help")
bot.run('token')
