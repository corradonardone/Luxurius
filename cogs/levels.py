import discord
import json
from discord import File
from discord.ext import commands
from typing import Optional
from easy_pil import Editor, load_image_async, Font

def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

level = ["Level-5+", "Level-10+", "Level-15+"]

level_num = [5, 10, 15]

class Levelsys(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print("Leveling Cog Ready!")

  @commands.Cog.listener()
  async def on_message(self, message):
    if not message.content.startswith("/" or get_prefix):
      if not message.author.bot:
        with open("json\levels.json", "r") as f:
          data = json.load(f)
        if str(message.guild.id) in data:
          if str(message.author.id) in data[str(message.guild.id)]:
            xp = data[str(message.guild.id)][str(message.author.id)]['xp']
            lvl = data[str(message.guild.id)][str(message.author.id)]['level']
            increased_xp = xp+15
            new_level = int(increased_xp/100)
            data[str(message.guild.id)][str(message.author.id)]['xp']=increased_xp
            with open("json\levels.json", "w") as f:
              json.dump(data, f)
            if new_level > lvl:
              embed=discord.Embed(title="Level Up!", description=f"{message.author.mention} just leveled up to level **{new_level}**!!!", color=0x31e30d)
              await message.channel.send(embed=embed)
              data[str(message.guild.id)][str(message.author.id)]['level']=new_level
              data[str(message.guild.id)][str(message.author.id)]['xp']=0
              with open("json\levels.json", "w") as f:
                json.dump(data, f)
              for i in range(len(level)):
                if new_level == level_num[i]:
                  await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))
                  mbed = discord.Embed(title=f"{message.author} You Have Gotten role **{level[i]}**!", color = message.author.colour)
                  mbed.set_thumbnail(url=message.author.avatar_url)
                  await message.channel.send(embed=mbed)
            return
        if str(message.guild.id) in data:
          data[str(message.guild.id)][str(message.author.id)] = {}
          data[str(message.guild.id)][str(message.author.id)]['xp'] = 0
          data[str(message.guild.id)][str(message.author.id)]['level'] = 1
        else:
          data[str(message.guild.id)] = {}
          data[str(message.guild.id)][str(message.author.id)] = {}
          data[str(message.guild.id)][str(message.author.id)]['xp'] = 0
          data[str(message.guild.id)][str(message.author.id)]['level'] = 1
        with open("json\levels.json", "w") as f:
          json.dump(data, f)
        with open("json\userdata.json", "r") as f:
          user_data = json.load(f)
        if str(message.author.id) in user_data:
          pass
        else:
          user_data[str(message.author.id)] = {}
          user_data[str(message.author.id)]['card'] = 5
          user_data[str(message.author.id)]['text_color'] = "#ff9933"
          user_data[str(message.author.id)]['bar_color'] = "#ff9933"
          user_data[str(message.author.id)]['blend'] = 0
        with open("json\userdata.json", "w") as f:
          json.dump(user_data, f)

  @discord.slash_command(name="rank", description="View your rank card")
  async def rank(self, ctx: commands.Context, user: Optional[discord.Member]):
    userr = user or ctx.author
    with open("json\levels.json", "r") as f:
      data = json.load(f)
    with open("json\userdata.json", "r") as f:
      user_data = json.load(f)
    xp = data[str(ctx.guild.id)][str(userr.id)]["xp"]
    lvl = data[str(ctx.guild.id)][str(userr.id)]["level"]
    next_level_xp = (lvl+1) * 100
    xp_need = next_level_xp
    xp_have = data[str(ctx.guild.id)][str(userr.id)]["xp"]
    card_num = str(user_data[str(userr.id)]['card'])
    text_color = str(user_data[str(userr.id)]['text_color'])
    bar_color = str(user_data[str(userr.id)]['bar_color'])
    blend = int(user_data[str(userr.id)]['blend'])
    percentage = int(((xp_have * 100)/ xp_need))
    if percentage < 1:
      percentage = 0
    background = Editor(f"images\{card_num}.png")
    profile = await load_image_async(str(userr.display_avatar))
    profile = Editor(profile).resize((150, 150)).circle_image()
    poppins = Font.poppins(size=40)
    poppins_small = Font.poppins(size=30)
    if blend == 1:
      ima = Editor("images\zBLACK.png")
      background.blend(image=ima, alpha=.5, on_top=False)
    background.paste(profile.image, (30, 30))
    background.rectangle((30, 220), width=650, height=40, fill="#fff", radius=20)
    background.bar(
        (30, 220),
        max_width=650,
        height=40,
        percentage=percentage,
        fill=bar_color,
        radius=20,
    )
    background.text((200, 40), str(userr.name), font=poppins, color=text_color)
    background.rectangle((200, 100), width=350, height=2, fill=bar_color)
    background.text(
        (200, 130),
        f"Level : {lvl}   "
        + f" XP : {xp} / {(lvl+1) * 100}",
        font=poppins_small,
        color=text_color,
    )
    card = File(fp=background.image_bytes, filename="zCARD.png")
    await ctx.respond(file=card)

  @discord.slash_command(name="leaderboard", description="View your server leaderboard")
  async def leaderboard(self, ctx, range_num=5):
    with open("json\levels.json", "r") as f:
      data = json.load(f)
    l = {}
    total_xp = []
    for userid in data[str(ctx.guild.id)]:
      xp = int(data[str(ctx.guild.id)][str(userid)]['xp']+(int(data[str(ctx.guild.id)][str(userid)]['level'])*100))
      l[xp] = f"{userid};{data[str(ctx.guild.id)][str(userid)]['level']};{data[str(ctx.guild.id)][str(userid)]['xp']}"
      total_xp.append(xp)
    total_xp = sorted(total_xp, reverse=True)
    index=1
    mbed = discord.Embed(
      title="Leaderboard Command Results"
    )
    for amt in total_xp:
      id_ = int(str(l[amt]).split(";")[0])
      level = int(str(l[amt]).split(";")[1])
      xp = int(str(l[amt]).split(";")[2])
      member = await self.bot.fetch_user(id_)
      if member is not None:
        name = member.name
        mbed.add_field(name=f"{index}. {name}",
        value=f"**Level: {level} | XP: {xp}**", 
        inline=False)
        if index == range_num:
          break
        else:
          index += 1
    await ctx.respond(embed = mbed)

  @commands.command("rank_reset")
  async def rank_reset(self, ctx, user: Optional[discord.Member]):
    member = user or ctx.author
    if not member == ctx.author:
      role = discord.utils.get(ctx.author.guild.roles, name="Bot-Mod")
      if not role in member.roles:
        await ctx.respond(f"You can only reset your data, to reset other data you must have {role.mention} role")
        return 
    with open("json\levels.json", "r") as f:
      data = json.load(f)
    del data[str(ctx.guild.id)][str(member.id)]
    with open("json\levels.json", "w") as f:
      json.dump(data, f)
    await ctx.respond(f"{member.mention}'s Data Got reset")
    
  @discord.slash_command(name="blend", description="Blend your rank card")
  async def blend(self, ctx, member: discord.Member=None):
    if member is None:
      member = ctx.author
    with open("json\userdata.json", "r") as f:
      user_data = json.load(f)
    if user_data[str(member.id)]['blend'] == 0:
      user_data[str(member.id)]['blend']=1
    else:
      user_data[str(member.id)]['blend']=0
    with open("json\userdata.json", "w") as f:
      json.dump(user_data, f)
    
  @discord.slash_command(name="card", description="Change your image card")
  async def card(self, ctx, card = None):
    member = ctx.author
    if card is None:
      embed = discord.Embed(title="Card Error", description="The card that you select doesn't exist!", color=0xe20808)
      await ctx.respond(embed=embed)
      return
    if int(card) > 6:
      embed = discord.Embed(title="Card Error", description="The card that you select doesn't exist!", color=0xe20808)
      await ctx.respond(embed=embed)
      return
    with open("json\userdata.json", "r") as f:
      user_data = json.load(f)
      user_data[str(member.id)]['card']=card
      embed2=discord.Embed(title="Card", description=f"Your new card is: {card}", color=0x12e203)
      await ctx.respond(embed=embed2)
    with open("json\userdata.json", "w") as f:
      json.dump(user_data, f)

def setup(client):
  client.add_cog(Levelsys(client))