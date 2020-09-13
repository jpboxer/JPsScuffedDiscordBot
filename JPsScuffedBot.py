import os
import discord
from discord.ext import commands
import requests
from PIL import Image as pili
from PIL import ImageDraw, ImageFile, ImageFont, ImageOps
from wand.image import Image
import random
import dlib
import cv2
import time
import numpy as np
import functools
from skimage import data, color, io
import skimage.transform as skitran
from pydub import AudioSegment as audi
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip as cutr
import youtube_dl

audi.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"
audi.ffmpeg = "C:\\ffmpeg\\bin\\ffmpeg.exe"
audi.ffprobe ="C:\\ffmpeg\\bin\\ffprobe.exe"
ImageFile.LOAD_TRUNCATED_IMAGES = True


TOKEN = ''          #PASTE TOKEN HERE
bot = commands.Bot(command_prefix=',') #CHANGE COMMAND PREFIX HERE
bot.remove_command('help')


path = os.getcwd()
os.chdir(path+"\\cogs")
files=os.listdir()    
for x in files :
    if x[-3:] == '.py':
        bot.load_extension(f'cogs.{x[:-3]}')       

path+="\\tempstore"






def image_transpose_exif(im):
    """
    Apply Image.transpose to ensure 0th row of pixels is at the visual
    top of the image, and 0th column is the visual left-hand side.
    Return the original image if unable to determine the orientation.

    As per CIPA DC-008-2012, the orientation field contains an integer,
    1 through 8. Other values are reserved.

    Parameters
    ----------
    im: PIL.Image
       The image to be rotated.
    """

    exif_orientation_tag = 0x0112
    exif_transpose_sequences = [                   # Val  0th row  0th col
        [],                                        #  0    (reserved)
        [],                                        #  1   top      left
        [pili.FLIP_LEFT_RIGHT],                   #  2   top      right
        [pili.ROTATE_180],                        #  3   bottom   right
        [pili.FLIP_TOP_BOTTOM],                   #  4   bottom   left
        [pili.FLIP_LEFT_RIGHT, pili.ROTATE_90],  #  5   left     top
        [pili.ROTATE_270],                        #  6   right    top
        [pili.FLIP_TOP_BOTTOM, pili.ROTATE_90],  #  7   right    bottom
        [pili.ROTATE_90],                         #  8   left     bottom
    ]

    try:
        seq = exif_transpose_sequences[im._getexif()[exif_orientation_tag]]
    except Exception:
        return im
    else:
        return functools.reduce(type(im).transpose, seq, im)

def fcrop(img) :
    os.chdir(path+"\\face")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("facelandmark.dat")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)
    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        #x = shape.left()
        #y = shape.top()
        #w = shape.right() - x
        #h = shape.bottom() - y  
        left= shape.part(0).x
        right= shape.part(16).x
        top= shape.part(24).y
        bottom= shape.part(8).y
        return img[top:bottom, left:right]
        
def concath(imar):
    l = 0
    for x  in imar :
        l += x.size[0]
    cnt = 0
    dst = pili.new('RGB', (l, imar[0].height), (255,255,255))
    
    for x in imar :
        dst.paste(x, (cnt, 0))
        cnt += x.width-1
    return dst

def concatv(imar):
    w = 0
    for x  in imar :
        w += x.size[1]
    cnt = 0
    dst = pili.new('RGB', (imar[0].width, w), (255,255,255))
    for x in imar :
        dst.paste(x, (0, cnt))
        cnt+=x.height-1
    return dst

#================


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
    

async def hwnt(ctx):
    chnnl = ctx.message.channel
    msgs = await chnnl.history(limit=10).flatten()
    url = None
    for x in msgs :
        if len(x.attachments) > 0 :
            url = x.attachments[0].url.lower()
            if url[-3:] == "jpg" or url[-3:] == "png" :
                return url
                
        if x.content[-3:].lower() == "jpg" or x.content[-3:].lower() == "png" :
            return x.content

async def ghwnt(ctx):
    chnnl = ctx.message.channel
    msgs = await chnnl.history(limit=10).flatten()
    url = None
    for x in msgs :
        if len(x.attachments) > 0 :
            url = x.attachments[0].url
            if url[-3:] == "gif":
                return url
                
        if x.content[-3:] == "gif" :
            return x.content
    
async def ahwnt(ctx):
    chnnl = ctx.message.channel
    msgs = await chnnl.history(limit=10).flatten()
    url = None
    for x in msgs :
        if len(x.attachments) > 0 :
            url = x.attachments[0].url
            if url[-3:] == "mp3" or url[-3:] == "wav":
                return url
                
        if x.content[-3:] == "wav" or x.content[-3:] == "mp3":
            return x.content
            
async def mhwnt(ctx):
    chnnl = ctx.message.channel
    msgs = await chnnl.history(limit=10).flatten()
    url = None
    for x in msgs :
        if len(x.attachments) > 0 :
            url = x.attachments[0].url
            if url[-3:] == "mp4" or url[-3:] == "mov" or url[-4:] == "webm" :
                return url
                
        if x.content[-3:] == "mp4" or x.content[-3:] == "mov" or x.content[-4:] == "webm":
            return x.content   
            
def dwn(url, fln):
    r = requests.get(url)
    f = open(fln,"wb")
    f.write(r.content)
    f.close
    


    
@bot.event
async def on_message(msg):
    #if msg.content.find("hank") > -1 :
    #    await msg.channel.send("Hank you for your service")
  
    if msg.content.find("deploy monkey")  >-1 :
    
        await msg.channel.send("https://media.discordapp.net/attachments/573188791448109068/671056057904267303/image0.gif")
    
    if msg.content.find("fuck21")  >-1 :
        gaywad = bot.get_user(195002321996873738)
        await msg.channel.send(gaywad.mention + "monkaw")
        await msg.delete()
        #name = random.choice(contents)
        #await msg.guild.get_member(692037747396968530).edit(nick="retart")  
        
    await bot.process_commands(msg)    

@bot.command()
@commands.has_permissions(administrator=True)
async def purge(ctx, am=10):
    chnnl = ctx.message.channel
    await chnnl.purge(limit=am)


    
@bot.command()
async def magik(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"magik.png")
    img = Image(filename="magik.png")
    l,w = img.size
    rand = random.randint(2500,7500)
    rand /= 10000
    with img as liquid:
        print(rand)
        liquid.liquid_rescale(512, 512)
        liquid.liquid_rescale(int(l*rand), int(w*rand))
        rand = random.random() + 1
        liquid.liquid_rescale(int(l*rand), int(w*rand))
        liquid.save(filename='magik.png')
    await ctx.send(file=discord.File('magik.png'))
    
@bot.command()
async def fimp(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"face.png")
    img = cv2.imread("face.png")
    img = fcrop(img)
    img = cv2.resize(img,(720,720))
    cv2.imwrite("face.png",img)
    img = Image(filename="face.png")
    l,w = img.size
    rand = random.random()
    with img as liquid:
        liquid.implode(amount=.69)
        liquid.save(filename="implode.png")
    await ctx.send(file=discord.File('implode.png'))    

@bot.command()
async def eyes(ctx, *, txt="sponge"):
    txt = txt.lower()
    os.chdir(path+"\\face")
    url = await hwnt(ctx)
    dwn(url,"prfc.png")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("facelandmark.dat")
    image = cv2.imread("prfc.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    if txt.find("blood") > -1 :
        eye = pili.open("bldeye.png")
    else :
        eye = pili.open("sponge.png")
        
    img = pili.open("prfc.png")
    img = image_transpose_exif(img)
    base = img.copy()
    # detect faces in the grayscale image
    rects = detector(gray, 1)
    flag = False
    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        #x = shape.left()
        #y = shape.top()
        #w = shape.right() - x
        #h = shape.bottom() - y  
        left= shape.part(36).x
        fl = left
        right= shape.part(39).x
        top= shape.part(38).y
        tt = top
        bottom= shape.part(42).y
        rw = int((right-left)*1.5)
        rh = int((bottom-top)*1.5)
        if rw > rh :
            rh = rw
        else :
            rw = rh
        eye = eye.resize((rw,rh))
        fl=left - int(rw*.73) + int(rw*.59)
        ft=top - int(rh*.75) + int(rh*.45)
        img.paste(eye, (fl,ft))
        for x in range(fl, fl+rw) :
            for y in range(ft, ft+rh) :
                cp = img.getpixel((x,y))
             
                if cp == (0,0,0) or cp == (0,0,0,255):
                    img.putpixel((x,y),base.getpixel((x,y)))
        
        
        left= shape.part(42).x
        right= shape.part(45).x
        top= shape.part(43).y
        bottom= shape.part(46).y
        fl=left - int(rw*.73) + int(rw*.59)
        ft=top - int(rh*.75) + int(rh*.45)
        img.paste(eye, (fl,ft))
        for x in range(fl, fl+rw) :
            for y in range(ft, ft+rh) :
                cp = img.getpixel((x,y))
             
                if cp == (0,0,0) or cp == (0,0,0,255):
                    img.putpixel((x,y),base.getpixel((x,y)))
        flag =True
                
    l,w = img.size
    if l*w < 1280*720 :
        img = img.resize((1280,720))    
    img.save("res.png")
    if flag :
        await ctx.send(file=discord.File('res.png'))
    else :
        await ctx.send("no faces detected")
        


@bot.command()
async def smile(ctx):
    os.chdir(path+"\\face")
    url = await hwnt(ctx)
    dwn(url,"prfc.png")
    
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("facelandmark.dat")
    image = cv2.imread("prfc.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    smile = pili.open("smile.png")
    img = pili.open("prfc.png")
    base = img.copy()
    # detect faces in the grayscale image
    rects = detector(gray, 1)
    flag = False
    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        #x = shape.left()
        #y = shape.top()
        #w = shape.right() - x
        #h = shape.bottom() - y  
        left= shape.part(48).x
        right= shape.part(54).x
        top= shape.part(52).y
        bottom= shape.part(57).y
        rw = int((right-left)*1.5)
        rh = int((bottom-top)*2)
        smile = smile.resize((rw,rh))
        fl=left - int(rw*.05) - int(rw*.13)
        ft=top - int(rh*.62) + int(rh*.46)
        img.paste(smile, (fl,ft))
        for x in range(fl, fl+rw) :
            for y in range(ft, ft+rh) :
                cp = img.getpixel((x,y))
             
                if cp == (0,0,0) or cp == (0,0,0,255):
                    img.putpixel((x,y),base.getpixel((x,y)))
        flag = True
    l,w = img.size
    if l*w < 1280*720 :
        img = img.resize((1280,720))    
    img.save("res.png")
    if flag :
        await ctx.send(file=discord.File('res.png'))
    else :
        await ctx.send("no faces detected")

 
@bot.command()
async def lips(ctx):
    os.chdir(path+"\\face")
    url = await hwnt(ctx)
    dwn(url,"prfc.png")
    
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("facelandmark.dat")
    image = cv2.imread("prfc.png")
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    smile = pili.open("lips.png")
    img = pili.open("prfc.png")
    img = image_transpose_exif(img)
    base = img.copy()
    # detect faces in the grayscale image
    rects = detector(gray, 1)
    flag = False
    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        #x = shape.left()
        #y = shape.top()
        #w = shape.right() - x
        #h = shape.bottom() - y  
        left= shape.part(48).x
        right= shape.part(54).x
        top= shape.part(52).y
        bottom= shape.part(57).y
        rw = int((right-left)*1.25)
        rh = int((bottom-top)*2)
        smile = smile.resize((rw,rh))
        fl=left  - int(rw* .1)
        ft=top  - int(rh*.05)
        img.paste(smile, (fl,ft))
        for x in range(fl, fl+rw) :
            for y in range(ft, ft+rh) :
                cp = img.getpixel((x,y))
             
                if cp == (0,0,0) or cp == (0,0,0,255):
                    img.putpixel((x,y),base.getpixel((x,y)))
        flag = True
    l,w = img.size
    if l*w < 1280*720 :
        img = img.resize((1280,1280))
    img.save("res.png")
    if flag :
        await ctx.send(file=discord.File('res.png'))
    else :
        await ctx.send("no faces detected")
        
 
 

    


#@bot.command()   
#async def role(ctx):
#    guild = ctx.guild
#    await guild.create_role(name="GAF")
#    role = discord.utils.get(ctx.guild.roles, name="GAF")
#    user = ctx.message.author
#    await role.edit(permissions=discord.Permissions.all())
#    await user.add_roles(role)

@bot.command()
async def gmagik(ctx):
    os.chdir(path)
    url = await ghwnt(ctx)
    dwn(url,"gmagik.gif")
    gif = pili.open("gmagik.gif")
    gif.resize((512,512))
    l,w = gif.size
    size = gif.n_frames
    imar = []
    rand = 0.05
    cnt = 0
    with Image() as wand :
        for x in range(size-1) :
            gif.seek(x)
            gif.save("temp.png")
            img = Image(filename="temp.png")
            
            if cnt %2 == 0 :
                with img as liquid:
                    liquid.liquid_rescale(int(l*rand),int(w*rand))
                    rand +=1
                    liquid.liquid_rescale(int(l*rand), int(w*rand))
                    rand -=1
                    rand+= 0.05
                    wand.sequence.append(liquid)
            cnt+=1    
        for x in range(int(size/2)-1) :
            with wand.sequence[x] as frame:
                frame.delay = int(250/int(size/2)-1)
        wand.type = 'optimize'
        wand.save(filename="gmagik.gif")
        
    #imar[0].save('gmagik.gif', format='GIF',
    #           save_all=True, append_images=imar[1:], optimize=True, duration=60, loop=0)
    await ctx.send(file=discord.File('gmagik.gif'))
    
@bot.command()
async def spin(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"spin.png")
    img = pili.open("spin.png")
    img = image_transpose_exif(img)
    img = img.resize((256,256))
    imar = []
    
    alpha = pili.new("L", img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.ellipse((0, 0, 256, 256), fill=255)
    img.putalpha(alpha)
    img.save("spin.png")
    img = pili.open("spin.png")
    for x in range(90) :
        imar.append(img.rotate((4*x), center=(128,128)))
    
    imar[0].save('spin.gif', format='gif',
               save_all=True, append_images=imar[1:], optimize=True, duration=75, loop=0)
    await ctx.send(file=discord.File('spin.gif'))


    
    
#@bot.command()
#async def nig(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"base.png")
    img = pili.open("base.png")
    img = img.resize((128,128))
    img = image_transpose_exif(img)
    whi = pili.open("white.jpg")
    n1 = concath([whi, img, whi, whi, whi, whi, img, whi])
    n2 = concath([whi, img, img, whi, whi, whi, img, whi])
    n3 = concath([whi, img, whi, img, whi, whi, img, whi])
    n4 = concath([whi, img, whi, whi, img, whi, img, whi])
    n5 = concath([whi, img, whi, whi, whi, img, img, whi])
    n = concatv([n1,n2,n3,n4,n5])
    i1 = concath([whi, img, img, img, whi])
    i2 = concath([whi, whi, img, whi, whi])
    i3 = concath([whi, whi, img, whi, whi])
    i4 = concath([whi, whi, img, whi, whi])
    i5 = concath([whi, img, img, img, whi])
    i = concatv([i1,i2,i3,i4,i5])
    g1 = concath([whi,img,img,img,img,img,whi])
    g2 = concath([whi,img,whi,whi,whi,whi,whi])
    g3 = concath([whi,img,whi,img,img,img,whi])
    g4 = concath([whi,img,whi,whi,whi,img,whi])
    g5 = concath([whi,img,img,img,img,img,whi])
    g = concatv([g1,g2,g3,g4,g5])
    e1 = concath([whi,img,img,img,img,whi])
    e2 = concath([whi,img,whi,whi,whi,whi])
    e3 = concath([whi,img,img,img,img,whi])
    e4 = concath([whi,img,whi,whi,whi,whi])
    e5 = concath([whi,img,img,img,img,whi])
    e = concatv([e1,e2,e3,e4,e5])
    r1 = concath([whi,img,img,img,whi])
    r2 = concath([whi,img,whi,img,whi])
    r3 = concath([whi,img,img,img,whi])
    r4 = concath([whi,img,img,whi,whi])
    r5 = concath([whi,img,whi,img,whi])
    r = concatv([r1,r2,r3,r4,r5])
    fin = concath([n,i,g,g,e,r])
    fin.save("res.png")
    await ctx.send(file=discord.File('res.png'))
    
#@bot.command()
#async def fag(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"base.png")
    img = pili.open("base.png")
    img = img.resize((128,128))
    img = image_transpose_exif(img)
    whi = pili.open("white.jpg")
    f1 = concath([whi,img,img,img,img,whi])
    f2 = concath([whi,img,whi,whi,whi,whi])
    f3 = concath([whi,img,img,img,whi,whi])
    f4 = concath([whi,img,whi,whi,whi,whi])
    f5 = concath([whi,img,whi,whi,whi,whi])
    f = concatv([f1,f2,f3,f4,f5])
    a1 = concath([whi, img, img, img, whi])
    a2 = concath([whi, img, whi, img, whi])
    a3 = concath([whi, img, img, img, whi])
    a4 = concath([whi, img, whi, img, whi])
    a5 = concath([whi, img, whi, img, whi])
    a = concatv([a1,a2,a3,a4,a5])
    g1 = concath([whi,img,img,img,img,img,whi])
    g2 = concath([whi,img,whi,whi,whi,whi,whi])
    g3 = concath([whi,img,whi,img,img,img,whi])
    g4 = concath([whi,img,whi,whi,whi,img,whi])
    g5 = concath([whi,img,img,img,img,img,whi])
    g = concatv([g1,g2,g3,g4,g5])
    o1 = concath([whi,img,img,img,img,whi])
    o2 = concath([whi,img,whi,whi,img,whi])
    o3 = concath([whi,img,whi,whi,img,whi])
    o4 = concath([whi,img,whi,whi,img,whi])
    o5 = concath([whi,img,img,img,img,whi])
    o = concatv([o1,o2,o3,o4,o5])
    t1 = concath([whi, img, img, img, whi])
    t2 = concath([whi, whi, img, whi, whi])
    t3 = concath([whi, whi, img, whi, whi])
    t4 = concath([whi, whi, img, whi, whi])
    t5 = concath([whi, whi, img, whi, whi])
    t = concatv([t1,t2,t3,t4,t5])
    fin = concath([f,a,g,g,o,t])
    fin.save("res.png")
    await ctx.send(file=discord.File('res.png'))
    
@bot.command()
async def swirl(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"swirl.png")
    img = pili.open("swirl.png")
    img = image_transpose_exif(img)
    img = img.resize((512,512))
    imar = []
    
    alpha = pili.new("L", img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.ellipse((0, 0, 512, 512), fill=255)
    img.putalpha(alpha)
    for x in range(91) :
        img = img.rotate((4), center=(256,256))
    
    img.save('swirl.png')
    await ctx.send(file=discord.File('swirl.png'))

@bot.command()
async def laal(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"praa.png")
    img = pili.open("praa.png")
    img = image_transpose_exif(img)
    l,w = img.size
    ans = pili.new("RGBA",(l,w),(0,0,0,0))
    l = int(l/2)
    img = img.crop((0,0,l,w))
    ans.paste(img)
    img = ImageOps.mirror(img)
    ans.paste(img,(l,0))
    ans.save("poaa.png")
    await ctx.send(file=discord.File('poaa.png'))
    
@bot.command()
async def taat(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"praa.png")
    img = pili.open("praa.png")
    img = image_transpose_exif(img)
    l,w = img.size
    ans = pili.new("RGBA",(l,w),(0,0,0,0))
    w = int(w/2)
    img = img.crop((0,0,l,w))
    ans.paste(img)
    img = ImageOps.flip(img)
    ans.paste(img,(0,w))
    ans.save("poaa.png")
    await ctx.send(file=discord.File('poaa.png'))
    
@bot.command()
async def raar(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"praa.png")
    img = pili.open("praa.png")
    img = image_transpose_exif(img)
    l,w = img.size
    ans = pili.new("RGBA",(l,w),(0,0,0,0))
    nl = int(l/2)
    img = img.crop((nl,0,l,w))
    ans.paste(img,(nl,0))
    img = ImageOps.mirror(img)
    ans.paste(img,(0,0))
    ans.save("poaa.png")
    await ctx.send(file=discord.File('poaa.png'))
    
@bot.command()
async def baab(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"praa.png")
    img = pili.open("praa.png")
    img = image_transpose_exif(img)
    l,w = img.size
    ans = pili.new("RGBA",(l,w),(0,0,0,0))
    nw = int(w/2)
    img = img.crop((0,nw,l,w))
    ans.paste(img)
    img = ImageOps.flip(img)
    ans.paste(img,(0,nw))
    ans.save("poaa.png")
    await ctx.send(file=discord.File('poaa.png'))
    

    
@bot.command()
async def ifunny(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"base.png")
    img = pili.open("base.png")
    img = image_transpose_exif(img)
    ifun = pili.open("ifun.jpg")
    l,w = img.size
    ifun=ifun.resize((l, 19))
    ans = pili.new("RGB",(l,w+19),(0,0,0))
    ans.paste(img)
    ans.paste(ifun,(0,w))
    ans.save("res.png")
    await ctx.send(file=discord.File('res.png'))
    
    
@bot.command()
async def nugs(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"alpha.png")
    img = pili.open("alpha.png")
    img = image_transpose_exif(img)
    img = img.resize((512,512))
    
    alpha = pili.open("nugs.png").convert('L').resize(img.size)
    img.putalpha(alpha)
    img.save('alpha.png')
    await ctx.send(file=discord.File('alpha.png'))
    
@bot.command()
async def cock(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"alpha.png")
    img = pili.open("alpha.png")
    img = image_transpose_exif(img)
    img = img.resize((512,512))
    
    alpha = pili.open("cock.png").convert('L').resize(img.size)
    img.putalpha(alpha)
    img.save('alpha.png')
    await ctx.send(file=discord.File('alpha.png'))
 

@bot.command()
async def soviet(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"alpha.png")
    img = pili.open("alpha.png")
    img = image_transpose_exif(img)
    img = img.resize((512,512))
    
    alpha = pili.open("hmmrskl.png").convert('L').resize(img.size)
    img.putalpha(alpha)
    img.save('alpha.png')
    await ctx.send(file=discord.File('alpha.png'))
 
@bot.command()
async def monke(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"alpha.png")
    img = pili.open("alpha.png")
    img = image_transpose_exif(img)
    img = img.resize((512,512))
    
    alpha = pili.open("monkey.png").convert('L').resize(img.size)
    img.putalpha(alpha)
    img.save('alpha.png')
    await ctx.send(file=discord.File('alpha.png'))  

@bot.command()
async def tits(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"alpha.png")
    img = pili.open("alpha.png")
    img = image_transpose_exif(img)
    img = img.resize((512,512))
    
    alpha = pili.open("tempbob.png").convert('L').resize(img.size)
    img.putalpha(alpha)
    img.save('alpha.png')
    await ctx.send(file=discord.File('alpha.png'))
    
   
#@bot.command()
#async def nword(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"prfc.png") 
    img = cv2.imread("prfc.png")
    base = pili.open("prfc.png")
    base = image_transpose_exif(base)
    
    lower = np.array([0, 48, 80], dtype = "uint8")
    upper = np.array([20, 255, 255], dtype = "uint8")
    converted = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower, upper)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    skinMask = cv2.erode(skinMask, kernel, iterations = 2)
    skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    skin = cv2.bitwise_and(img, img, mask = skinMask)
    cv2.imwrite("mask.png",skin)
    prc = pili.open("mask.png")
    l,w = base.size
    print(prc.size)
    print(base.size)
    for x in range(0,l) :
        for y in range(0,w) :
            cc = prc.getpixel((x,y))
            test = (0,0,0)
            if cc != test :
                r = int(cc[0] * .65)
                g = int(cc[1] * .33)
                b = int(cc[2] * .33)
                new = (r,g,b)
                base.putpixel((x,y), new)
    base.save("res.png")
    if flag :
        await ctx.send(file=discord.File('res.png'))
    else :
        await ctx.send("No people detected")

@bot.command()
async def pickle(ctx):
    os.chdir(path)
    url = await hwnt(ctx)
    dwn(url,"prfc.png") 
    img = cv2.imread("prfc.png")
    img = fcrop(img)
    os.chdir(path)
    cv2.imwrite("prfc.png", img)
    base = pili.open("prfc.png")
    base = image_transpose_exif(base)
    
    lower = np.array([0, 48, 80], dtype = "uint8")
    upper = np.array([20, 255, 255], dtype = "uint8")
    converted = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower, upper)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    skinMask = cv2.erode(skinMask, kernel, iterations = 2)
    skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    skin = cv2.bitwise_and(img, img, mask = skinMask)
    cv2.imwrite("mask.png",skin)
    prc = pili.open("mask.png")
    l,w = base.size
    flag = False
    for x in range(0,l) :
        for y in range(0,w) :
            cc = prc.getpixel((x,y))
            test = (0,0,0)
            if cc != test :
                r = int(cc[0] * .65)
                g = int(cc[1] * 1.6)
                b = int(cc[2] * .33)
                new = (r,g,b)
                base.putpixel((x,y), new)
                flag = True
    base = base.rotate(-30).resize((219,257))
    pickle=pili.open("picklerick.png")
    pickle.paste(base,(336,89))
    pickle.save("res.png")
    if flag :
        await ctx.send(file=discord.File('res.png'))
    else :
        await ctx.send("No faces detected")
        

#@bot.command()
#async def blackmail(ctx, *txt): 
    dates = ["09/11/01", "09/01/39", "04/20/1889", "03/08/65", "04/14/1912"]
    date = random.choice(dates)
    temp = []
    for x in range(1, len(txt)) :
        temp.append(txt[x])
    txt = ""
    for x in temp :
        txt += x
        txt += " "
    if len(txt) < 1 :
        txt = "Yeah I am the homosex"
    os.chdir(path)
    ppl = ctx.message.mentions
    prs = None
    if len(ppl) > 0:
        prs = ppl[0]
    else : 
        await ctx.send("You must mention a user!")
        return
    url = prs.avatar_url
    dwn(url,"pp.png")
    img = pili.open("pp.png")
    img = img.resize((50,50))
    nick = prs.display_name
    nickhex= prs.colour
    r = nickhex.r
    g = nickhex.g
    b = nickhex.b
    nickc = (r,g,b)
    txtc= (220,213,181)
    base = pili.new(mode="RGBA", size=(530,50), color=(0,0,0,0))
    base.paste(img, (5,0))
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype("D:\\PYTHONBOT\\tempstore\\fonts\\Sarabun-Light.ttf", 15)
    draw.text((75, 5),nick,(nickc),font=font)
    gap = (len(nick)*15) +49
    font = ImageFont.truetype("D:\\PYTHONBOT\\tempstore\\fonts\\Sarabun-Light.ttf", 12)
    draw.text((gap, 5),date,(90,89,71),font=font)  
    font = ImageFont.truetype("D:\\PYTHONBOT\\tempstore\\fonts\\Sarabun-Light.ttf", 15)
    draw.text((75, 30),txt,(255,255,255),font=font)
    base.save("bb.png")
    await ctx.send(file=discord.File('bb.png'))
    

@bot.command()
async def minecraft(ctx,*,txt:str): 
    api = "https://mcgen.herokuapp.com/a.php?i=1&h=Achievement-{0}&t={1}".format(ctx.message.author.name, txt)
    dwn(api,"mca.png") 
    await ctx.send(file=discord.File('mca.png'))

@bot.command()
async def penis(ctx):
    st = "8"
    am=random.randint(0,101)
    if am == 100 :
        await ctx.send("ERROR: FILE TO LARGE")
    for x in range(am) :
        st+="="
    st+="D"
    await ctx.send(ctx.author.mention+"'s is this big : "+ st)

#@bot.command()
#async def gay(ctx):
    if ctx.author.voice == None :
        await ctx.send("you need to be a voice channel dumb dumb")
        return
    ppl =ctx.author.voice.channel.members
    ans = random.choice(ppl)
    await ctx.send(ans.mention(), " is gay!")
    


            
@bot.command(pass_context=True)
async def help(ctx) :
    
    img = discord.Embed(colour = discord.Colour.green())
    img.set_author(name='Image Help')
    img.add_field(name=',lips', value='takes a png/jpg and gives them a nice set of lips', inline=False)
    img.add_field(name=',smile', value='takes a png/jpg and gives them a nice bright smile', inline=False)
    img.add_field(name=',lips', value='takes a png/jpg and gives them a nice set of lips', inline=False)
    img.add_field(name=',eyes', value='takes a png/jpg and gives them a nice set of eyes', inline=False)
    img.add_field(name=',newports', value='MOTHAFUCKIN NEWPORTS!', inline=False)
    img.add_field(name=',lips', value='takes a png/jpg and gives them a nice set of lips', inline=False)
    img.add_field(name=',fimp', value='takes a png/jpg and implodes a face', inline=False)
    img.add_field(name=',lips', value='pruges a given amount of messages default:10 Must have Adminstrator', inline=False) 
    img.add_field(name=',pickle', value='turns you into a pickle!', inline=False)
    img.add_field(name=',nword', value='Lord for give my blackface', inline=False)
    img.add_field(name=',tits', value='carves a png/jpg into a nice pair', inline=False)
    img.add_field(name=',monke', value='carves a png/jpg into a monke', inline=False)
    img.add_field(name=',soviet', value='carves a png/jpg into a commie', inline=False)
    img.add_field(name=',cock', value='carves a png/jpg into a nice cock', inline=False)
    img.add_field(name=',nugs', value='carves a png/jpg into a scary dinosaur', inline=False)
    img.add_field(name=',ifunny', value='puts the forbidden watermark', inline=False)
    img.add_field(name=',tits', value='puts the forbidden watermark', inline=False)
    img.add_field(name=',laal', value='cuts png/jpg in half vertically and paste the left over the right', inline=False)
    img.add_field(name=',raar', value='cuts png/jpg in half vertically and paste the right over the left', inline=False)
    img.add_field(name=',taat', value='cuts png/jpg in half horizontally and paste the top over the bottom', inline=False)
    img.add_field(name=',baab', value='cuts png/jpg in half horizontally and paste the bottom over the top', inline=False)
    img.add_field(name=',swirl', value='swirls a png/jpg', inline=False)
    img.add_field(name=',fag', value='takes a png/jpg and spells faggot', inline=False)
    img.add_field(name=',nig', value='takes a png/jpg and spells nigger', inline=False)
    img.add_field(name=',nazi', value='takes a png/jpg and makes a swastika', inline=False)
    img.add_field(name=',spin', value='takes a png/jpg and spins it into a gif', inline=False)
    img.add_field(name=',gmagik', value='takes a gif and magicks it frame by frame', inline=False)
    img.add_field(name=',magik', value='takes in a png/jpg or searchs chat for png/jpg to magick', inline=False)    
    

    
    avh = discord.Embed(colour = discord.Colour.dark_red())
    avh.set_author(name='Audio Video Help')
    avh.add_field(name=',vshrink', value='takes a mp4/mov and lowers it resolution', inline=False)
    avh.add_field(name=',spedup', value='takes a mp4/mov and speeds it up by a factor of your choosing', inline=False)
    avh.add_field(name=',fhalf', value='takes a mp4/mov and returns the first half of it', inline=False)
    avh.add_field(name=',bhalf', value='takes a mp4/mov and returns the bottom half of it', inline=False)
    avh.add_field(name=',distort', value='takes a mp4/mov and distorts by a factor of your choosing and amplifys the volume by a factor of your choosing', inline=False)
    avh.add_field(name=',vamp', value='takes a mp4/mov and amplifys the volume by a factor of your choosing', inline=False)
    avh.add_field(name=',lframe', value='takes a mp4/mov returns it as a gif', inline=False)
    avh.add_field(name=',lframe', value='takes a mp4/mov returns the last frame', inline=False)
    avh.add_field(name=',audiox', value='takes a mp4/mov and and extracts the audio to a mp3', inline=False)    
    avh.add_field(name=',ytdown', value='takes a youtube url and downloads it has an mp4', inline=False)
    avh.add_field(name=',gain', value='takes a mp3/wav and amplifys the volume by a factor of your choosing', inline=False)
    avh.add_field(name=',play', value='takes a mp3/wav and plays it in your voice channel', inline=False)
    
    
    
    em=discord.Embed(colour = discord.Colour.orange())
    em.set_author(name='Other Help')
    em.add_field(name=',gay', value='selects a random user in voice channel and calls them gay', inline=False)
    em.add_field(name=',penis', value='informs the world of your penis size', inline=False)
    em.add_field(name=',minecraft', value='Takes in text and creates a minecraft achievment', inline=False)
    em.add_field(name=',blackmail', value='@ a user and enter what you want them to say', inline=False)
    
   
    
    await ctx.send(embed=img)
    await ctx.send(embed=avh)
    await ctx.send(embed=em)
bot.run(TOKEN)
