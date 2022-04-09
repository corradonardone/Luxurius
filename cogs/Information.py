from re import sub
import discord
import json
from io import BytesIO
from discord.ext import commands
from PIL import Image, ImageChops, ImageDraw, ImageFont

def circle(pfp,size = (215,215)):
    
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

class Information(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @discord.slash_command(name="profile", description="View you profile card")
    async def profileinfo(self,ctx,member:discord.Member=None):
        if not member:
            member = ctx.author
        name, nick, Id, status = str(member), member.display_name, str(member.id), str(member.status).upper()
        created_at = member.created_at.strftime("%a %b\n%B %Y")
        joined_at = member.joined_at.strftime("%a %b\n%B %Y")
        with open("json\levels.json", "r") as f:
            data = json.load(f)
        lvl = data[str(ctx.guild.id)][str(member.id)]["level"]
        money, level = "Error", str(lvl)
        base = Image.open("images\profile.png").convert("RGBA")
        background = Image.open("images\sfondo.png").convert("RGBA")
        pfp = member.display_avatar.with_size(256)
        data = BytesIO(await pfp.read())
        pfp = Image.open(data).convert("RGBA")
        name = f"{name[:16]}.." if len(name)>16 else name
        nick = f"AKA - {nick[:17]}.." if len(nick)>17 else f"AKA - {nick}"
        draw = ImageDraw.Draw(base)
        pfp = circle(pfp,(215,215))
        font = ImageFont.truetype("font\server-profile.ttf",38)
        akafont = ImageFont.truetype("font\server-profile.ttf",30)
        subfont = ImageFont.truetype("font\server-profile.ttf",25)
        draw.text((280,240),name,font = font)
        draw.text((270,315), nick,font = akafont)
        draw.text((65,490),Id,font = subfont)
        draw.text((405,490),status, font = subfont)
        draw.text((65,635), money,font = subfont)
        draw.text((405,635),level,font = subfont)
        draw.text((65,770),created_at, font = subfont)
        draw.text((405,770),joined_at,font = subfont)
        base.paste(pfp,(56,158), pfp)
        background.paste(base,(0,0), base)
        with BytesIO() as a:
            background.save(a, "PNG")
            a.seek(0)
            await ctx.respond(file= discord.File(a, "profile.png"))

    @discord.slash_command(name="server", description="View server card information")
    async def serverinfo(self,ctx):
        name, Id, nick, membercount = ctx.guild.name, str(ctx.guild.id), "Server", str(ctx.guild.member_count)
        toprole = "Owner"
        owner = str(ctx.guild.owner)
        created_at = ctx.guild.created_at.strftime("%a %b\n%B %Y")
        level = "Error 404"
        base = Image.open("images\server.png").convert("RGBA")
        background = Image.open("images\sfondo.png").convert("RGBA")
        pfp = ctx.guild.icon.with_size(256)
        data = BytesIO(await pfp.read())
        pfp = Image.open(data).convert("RGBA")
        name = f"{name[:16]}.." if len(name)>16 else name
        draw = ImageDraw.Draw(base)
        pfp = circle(pfp,(215,215))
        font = ImageFont.truetype("font\server-profile.ttf",38)
        akafont = ImageFont.truetype("font\server-profile.ttf",30)
        subfont = ImageFont.truetype("font\server-profile.ttf",25)
        draw.text((280,240),name,font = font)
        draw.text((270,315), nick,font = akafont)
        draw.text((65,490),Id,font = subfont)
        draw.text((405,490),toprole, font = subfont)
        draw.text((65,635), owner,font = subfont)
        draw.text((405,635),level,font = subfont)
        draw.text((65,770),created_at, font = subfont)
        draw.text((405,770),membercount,font = subfont)
        base.paste(pfp,(56,158), pfp)
        background.paste(base,(0,0), base)
        with BytesIO() as a:
            background.save(a, "PNG")
            a.seek(0)
            await ctx.respond(file= discord.File(a, "profile.png"))
    
    @commands.command()
    async def avatar(self, ctx, *,  member : discord.Member=None):
        if not member:
            member = ctx.author
        embed = discord.Embed(title="Avatar")
        embed.set_image(url=f"{member.display_avatar}")

def setup(bot):
    bot.add_cog(Information(bot))