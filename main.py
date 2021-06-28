import discord
import os
from channelInfo import channelInfoClass
import emojis
import json

client = discord.Client()
enabledChannelDict = {}
guildEmojis = {}
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    #keeps track of guilds so that appropriate emotes can be used
    print("------")
    print(type(message.channel))
    if (type(message.channel) == discord.channel.DMChannel):
      return
    guildEmojis.update({message.guild : message.guild.emojis})
    if message.author == client.user:
        return

    #strEmoji method one
    if message.content.startswith('$hello'):
        print("<><><><><><>><><><><><><><><><><><><><><><>")
        await message.channel.send('Hello!')

    #strEmoji method 2
    #reacts with a smile if no emote, if there is an emote reacts with that
    if message.content.startswith('$testReact'):
      string = message.content.split(" ")
      emoji = None
      #checks for default emojis first
      if len(string) > 1 and emojis.count(string[1]) > 0:
        emlist = list(emojis.get(string[1]))
        emoji = emlist[0]
      #now checks for guild emojis
      elif len(string) > 1:
        for i in range(len(guildEmojis)):
          strEmoji = (str(guildEmojis[message.guild][i]))
          if strEmoji == string[1]:
            emoji = guildEmojis[message.guild][i]
        if emoji == None:
          emoji = emojis.encode(":smile:")
      #if emoji not in guild, default to smile
      else:
        emoji = emojis.encode(":smile:")
      
      await message.add_reaction(emoji)

    #enables liking in a given channel
    if message.content.startswith('$enableLikes'):
      enabledChannel = channelInfoClass(message.channel)
      enabledChannelDict.update({message.channel : enabledChannel})
      channelFile = open("enabledChannels.txt", "w+")
      channelFile.truncate(0)
      txtToWrite = json.dump(enabledChannelDict)
      channelFile.write(txtToWrite)
      await message.channel.send('Liking enabled in ' + message.channel.name)
    if message.content.startswith('$whitelist'):
      if ',' in message.content:
        await message.channel.send("Please space apart emotes with spaces, not commas.")
        return
      if message.channel not in enabledChannelDict:
        await message.channel.send("Please enable likes in this channel to whitelist reactions")
        return
      channelObj = enabledChannelDict[message.channel]
      stri = message.content.split(" ")
      if (len(stri) == 1):
        channelObj.whitelisted = not channelObj.whitelisted
        if channelObj.whitelisted:
          await message.channel.send("This channel is now operating on its whitelist")
          return
        else:
          await message.channel.send("This channel is now operating on its blacklist")
          return
      for i in range(1, len(stri)):
        if channelObj.checkList(stri[i]):
          print("Already Whitelisted " + stri[i])
        else:
          channelObj.whitelist(stri[i])

        
      
      
@client.event
async def on_reaction_add(reaction, user):
  if reaction.message.author.name == "LikeBot":
    return
  print("reaction added somewhere")
  author = reaction.message.author
  print(enabledChannelDict)
  if reaction.message.channel in enabledChannelDict:
    thisChannel = enabledChannelDict[reaction.message.channel]
    print ("channel has liking enabled")
    if thisChannel.checkList(reaction):
      print('tried to call dm')
      if user.nick != None:
        name = user.nick
      else:
        name = user.name
      emoji = reaction.emoji
      if type(emoji) == discord.emoji.Emoji:
        emoji = "the :" + reaction.emoji.name + ": emote!"
      print(name)
      print(emoji)
      print(type(emoji))
      msg = name + " reacted to your message with " + emoji
      await dm(author, msg)

    
    

async def dm(author, message):
  print("dm called")
  dmchannel = author.dm_channel
  if dmchannel == None:
      await author.create_dm()
      dmchannel = author.dm_channel
      await dmchannel.send("Hi, I'm Likebot! I provide you with a notification when someone reacts to your message. Don't worry, you can opt out by sending $optout in the channel where I'm enabled. You can also opt back in using $optin")

  await dmchannel.send(message)


client.run(os.getenv('TOKEN'))