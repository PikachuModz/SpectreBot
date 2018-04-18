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
            embed = discord.Embed(title="▶ Commands b.1", description="", color=0x42a1f4)
            embed.add_field(name="Spam", value="Sends a message multiple times (syntax: <times> <txt>)", inline=False)
            embed.add_field(name="Music", value="Basic MusicBot (syntax: <play/stop/pause/resume> <url>)", inline=False)
            embed.add_field(name="Separate", value="Divides the characters of a text in spaces (syntax: <space> <txt>)", inline=False)
            embed.add_field(name="Shutdown", value="Closes the bot", inline=False)
            await bot.send_message(message.channel, embed=embed)   
           
        elif message.content.startswith(cmd_prefix+"spam"):
            n = int(message.content.split()[1])
            for i in range(n): 
                spam_message = ' '.join(message.content.split()[2:])
                await bot.send_message(message.channel, spam_message)  

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
            await bot.send_message(message.channel, "Bye!")  
            await bot.logout()

        elif message.content.startswith(cmd_prefix+"music"):
            try:
                args1 = message.content.split()[1]
                if args1 == "play":
                        p_url = ' '.join(message.content.split()[2:])
                        if p_url.startswith("https://www.youtube.com"):
                            try:
                                channel = message.author.voice.voice_channel
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
                                return
                        else:
                            await bot.send_message(message.channel, "Please write the youtube link of a valid video!")
                else:
                    try: 
                        if args1 == "pause":
                            players[message.server.id].pause()
                            await bot.send_message(message.channel, "Song paused!")  
                        elif args1 == "resume":
                            players[message.server.id].resume()
                            await bot.send_message(message.channel, "Song resumed!")  
                        elif args1 == "stop":
                            players[message.server.id].stop()
                            players[message.server.id] = None
                            await bot.send_message(message.channel, "Song removed!")
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
