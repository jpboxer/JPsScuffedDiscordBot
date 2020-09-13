import os
import discord
from discord.ext import commands
import requests
import random
import numpy as np
from pydub import AudioSegment as audi
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip as cutr
import youtube_dl

audi.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"
audi.ffmpeg = "C:\\ffmpeg\\bin\\ffmpeg.exe"
audi.ffprobe ="C:\\ffmpeg\\bin\\ffprobe.exe"

if os.getcwd().find("cogs") > -1 :
    os.chdir("..")
path = os.getcwd()
path+="\\tempstore"


class AV(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("AV cog loaded")


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
    

    @commands.command()
    async def play(self,ctx):
        os.chdir(path+"\\sounds")
        url = await AV.ahwnt(ctx)
        form = url[-3:]
        AV.dwn(url,"base."+form)
        if form == 'mp3' :
            clip = audi.from_mp3("base."+form)
        else :
            clip = audi.from_wav("base."+form)
        query = "base."+form
        chnnl= ctx.author.voice.channel 
        if chnnl == None :
            await ctx.send("JOIN A VOICE CHAT DUMBASS")
            return
        if ctx.voice_client is not None :
            await ctx.voice_client.move_to(chnnl)
        else :
            await chnnl.connect()
    
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        time.sleep(len(clip)/1000)
        await ctx.voice_client.disconnect()
 
    @commands.command()
    async def gain(self,ctx,db=6):
        os.chdir(path+"\\sounds")
        url = await AV.ahwnt(ctx)
        form = url[-3:]
        AV.dwn(url,"base."+form)
        if form == 'mp3' :
            clip = audi.from_mp3("base."+form)
        else :
            clip = audi.from_wav("base."+form)
        clip = clip.apply_gain(db)
        clip.export("amp.mp3", format="mp3")
        await ctx.send(file=discord.File('amp.mp3'))
 
    @commands.command()
    async def ytdown(self,ctx,url, quality="worst"):
        try :
            quality = quality.lower()
        except :
            ctx.send("thats not a word")
        if quality == "best" :
            ydl_opts = {
                'format': 'best',       
                'outtmpl': 'del',        
                'noplaylist' : True,        
            }
        elif quality == "worst" :
            ydl_opts = {
                'format': 'worst',       
                'outtmpl': 'del',        
                'noplaylist' : True,        
            }
        else : 
            ydl_opts = {
                'format': 'worst',       
                'outtmpl': 'del',        
                'noplaylist' : True,        
            }
        os.chdir(path+"\\sounds")
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    
        files=os.listdir()
        res = None
        for x in files :
            if x.find('del') > -1 :
                res = x
        try :
            video = VideoFileClip(res)
            video.write_videofile("base.mp4")
            os.remove(res)
        except :
            await ctx.send("Error downloading the video")
        try :
            await ctx.send(file=discord.File('base.mp4'))
        except:
            await ctx.send("File to large")
    
    @commands.command()  
    async def audiox(self,ctx):
    
        os.chdir(path+"\\sounds")
        url = await AV.mhwnt(ctx)
        form = url[-3:]
        AV.dwn(url,"base."+form)
        video = VideoFileClip("base."+form)
        audio = video.audio
        audio.write_audiofile("result.mp3")
        try :
            await ctx.send(file=discord.File('result.mp3'))
        except:
            await ctx.send("File to large")
    

 
    @commands.command()   
    async def vamp(self,ctx, db=12):
        os.chdir(path+"\\sounds")
        url = await AV.mhwnt(ctx)
        form = url[-3:]
        AV.dwn(url,"base."+form)
        video = VideoFileClip("base."+form)
        video = video.volumex(db/6)
        video.write_videofile("res.mp4")
        try :
            await ctx.send(file=discord.File('res.mp4')) 
        except:
            await ctx.send("File to large")

    @commands.command()  
    async def pvamp(self,ctx):
        os.chdir(path+"\\sounds")
        url = await AV.mhwnt(ctx)
        form = url[-3:]
        AV.dwn(url,"base."+form)
        video = VideoFileClip("base."+form)
        subs = []
        for x in range(1, int(video.duration*10)):
            pos1 = (x-1)/10
            pos2 = x/10
            if x == int(video.duration*10) :
                sub = video.subclip(t_start=pos2, t_end=video.duration)
            else :
                sub = video.subclip(t_start=pos1, t_end=pos2)
            sub = sub.volumex(pos2*1.1)
            subs.append(sub)
        fclip = concatenate_videoclips(subs)
        fclip.write_videofile("res.mp4")
        try :
            await ctx.send(file=discord.File('res.mp4')) 
        except:
            await ctx.send("File to large")
    
    @commands.command()  
    async def distort(self,ctx, ds=5, db=12):
        import moviepy.video.fx.all as vfx
        os.chdir(path+"\\sounds")
        url = await AV.mhwnt(ctx)
        form = url[-3:]
        AV.dwn(url,"base."+form)
        video = VideoFileClip("base."+form)
        video = video.volumex(db/6)
        video = vfx.colorx(video, int(ds))
        video.write_videofile("res.mp4")
        try :
            await ctx.send(file=discord.File('res.mp4')) 
        except:
            await ctx.send("File to large") 
 

    @commands.command()  
    async def pdistort(self,ctx, ds=5):
        import moviepy.video.fx.all as vfx
        os.chdir(path+"\\sounds")
        url = await AV.mhwnt(ctx)
        form = url[-3:]
        AV.dwn(url,"base."+form)
        video = VideoFileClip("base."+form)
        leng = video.duration
        seg = int(leng/10)
        clips = []
        for x in range(1,11) :
            if x == 10 :
                sub = video.subclip(t_start=(x-1)*seg, t_end=leng)
            else :
                sub = video.subclip(t_start=(x-1)*seg, t_end=seg*x)
                
            sub = vfx.colorx(sub,x)
            clips.append(sub)
        fclip = concatenate_videoclips(clips)
        fclip.write_videofile("res.mp4")
        try :
            await ctx.send(file=discord.File('res.mp4')) 
        except:
            await ctx.send("File to large") 

    @commands.command()  
    async def vshrink(self,ctx, ds=5):
        import moviepy.video.fx.all as vfx
        os.chdir(path+"\\sounds")
        url = await AV.mhwnt(ctx)
        form = url[-3:]
        AV.dwn(url,"base."+form)
        video = VideoFileClip("base."+form)
        w,h = video.size
        w = int(w/2)
        h = int(h/2)
        video = vfx.resize(video, (w,h))
        video.write_videofile("res.mp4")    
        try :
            await ctx.send(file=discord.File('res.mp4')) 
        except:
            await ctx.send("File to large") 
    
    @commands.command()  
    async def spedup(self,ctx, multi=12):
        import moviepy.video.fx.all as vfx
        os.chdir(path+"\\sounds")
        url = await AV.mhwnt(ctx)
        form = url[-3:]
        AV.dwn(url,"base."+form)
        video = VideoFileClip("base."+form)
        video = vfx.speedx(video, multi)
        video.write_videofile("res.mp4")
        try :
            await ctx.send(file=discord.File('res.mp4')) 
        except:
            await ctx.send("File to large")
 
    @commands.command() 
    async def vdownscale(self,ctx):
        import moviepy.video.fx.all as vfx
        os.chdir(path+"\\sounds")
        url = await AV.mhwnt(ctx)
        form = url[-3:]
        AV.dwn(url,"base."+form)
        video = VideoFileClip("base."+form)
        audio = video.audio
        audio.write_audiofile("temp.mp3")
        clip = audi.from_mp3("temp.mp3")
        clip = clip.set_frame_rate(24000)
        clip.export("temp.mp3", bitrate="16k", format="mp3")
        audio = AudioFileClip("temp.mp3")
        video = video.set_audio(audio)
        w,h = video.size
        w = int(w/16)
        h = int(h/16)
        video = vfx.resize(video, (w,h))
        #audio = audio.fx(resize, 0.125, method='bilinear')
        w = int(w*16)
        h = int(h*16)
        video = vfx.resize(video, (w,h))
        video.write_videofile("res.mp4")
        try :
            await ctx.send(file=discord.File('res.mp4')) 
        except:
            await ctx.send("File to large")
       
    @commands.command()  
    async def fhalf(self,ctx):
        import moviepy.video.fx.all as vfx
        os.chdir(path+"\\sounds")
        url = await AV.mhwnt(ctx)
        form = url[-3:]
        AV.dwn(url,"base."+form)
        video = VideoFileClip("base."+form)
        leng = video.duration
        mid = int(leng/2)
        cutr("base."+form, 0, mid, targetname="res.mp4")
        try :
            await ctx.send(file=discord.File('res.mp4')) 
        except:
            await ctx.send("File to large")
        
    @commands.command()   
    async def pvdownscale(self,ctx):
        import moviepy.video.fx.all as vfx
        os.chdir(path+"\\sounds")
        url = await AV.mhwnt(ctx)
        form = url[-3:]
        AV.dwn(url,"base."+form)
        video = VideoFileClip("base."+form)
        audio = video.audio
        audio.write_audiofile("temp.mp3")
        clip = audi.from_mp3("temp.mp3")
        clip = clip.set_frame_rate(24000)
        flag = True
        bit = 32
        seg = int(video.duration/6)
        aclips = []
        for x in range(1,7) :
            clip.export("temp.mp3", bitrate=str(bit)+'k', format="mp3")
            audio = AudioFileClip("temp.mp3")
            if x == 6 :
                taudio = audio.subclip((x)*seg, video.duration)

            else :
                taudio = audio.subclip((x-1)*seg, seg*x)
            bit/=2
            aclips.append(taudio)
        clips = []
        for x in range(1,7) :
            if x == 6 :
                print("fa")
                tvideo = video.subclip((x)*seg, video.duration)
            else :
                tvideo = video.subclip((x-1)*seg, seg*x)
            h,w=video.size
            h /= int(2*x)
            w /= int(2*x)
            tvideo = vfx.resize(tvideo, (w,h))
            h *= (2*x)
            w *= (2*x)
            tvideo = vfx.resize(tvideo, (w,h))
            tvideo = tvideo.set_audio(aclips[x-1])
            clips.append(tvideo)
            
        fclip = concatenate_videoclips(clips)
        fclip.write_videofile("res.mp4")
        try :
            await ctx.send(file=discord.File('res.mp4')) 
        except:
            await ctx.send("File to large")          

    @commands.command()
    async def bhalf(self,ctx):
        import moviepy.video.fx.all as vfx
        os.chdir(path+"\\sounds")
        url = await AV.mhwnt(ctx)
        form = url[-3:]
        AV.dwn(url,"base."+form)
        video = VideoFileClip("base."+form)
        leng = video.duration
        mid = int(leng/2)
        cutr("base."+form, mid, leng-1, targetname="res.mp4")
        try :
            await ctx.send(file=discord.File('res.mp4')) 
        except:
            await ctx.send("File to large")


    @commands.command()  
    async def lframe(self,ctx):
        import moviepy.video.fx.all as vfx
        os.chdir(path+"\\sounds")
        url = await AV.mhwnt(ctx)
        form = url[-3:]
        AV.dwn(url,"base."+form)
        video = VideoFileClip("base."+form)
        leng = video.duration
        video.save_frame("res.png",t=leng-1,withmask=True)
        try :
            await ctx.send(file=discord.File('res.png')) 
        except:
            await ctx.send("File to large")




            
    @commands.command()   
    async def mp4gif(self,ctx, db=12):
        os.chdir(path+"\\sounds")
        url = await AV.mhwnt(ctx)
        form = url[-3:]
        AV.dwn(url,"base."+form)
        video = VideoFileClip("base."+form)
        video.write_gif("res.gif")
        try :
            await ctx.send(file=discord.File('res.gif')) 
        except:
            await ctx.send("File to large")


    @commands.command()
    async def gifmp4(self,ctx) :
        import moviepy.video.fx.all as vfx
        os.chdir(path+"\\sounds")
        url = await AV.ghwnt(ctx)
        form = url[-3:]
        AV.dwn(url,"base."+form)
        video = VideoFileClip("base."+form)
        url = await AV.ahwnt(ctx)
        AV.dwn(url,"base.mp3")
        audio = AudioFileClip("base.mp3")
        clips = []
        if video.duration > audio.duration :
            clips.append(video.subclip(0, audio.duration))
        else :
            leng=audio.duration-video.duration
            clips.append(video)
            while leng >= video.duration :
                clips.append(video)
                leng -= video.duration
            clips.append(video.subclip(0,leng))
       
        video = concatenate_videoclips(clips)
        video = video.set_audio(audio)
        video.write_videofile("res.mp4")
        try :
            await ctx.send(file=discord.File('res.mp4')) 
        except:
            await ctx.send("File to large")

def setup(bot):
    bot.add_cog(AV(bot))
