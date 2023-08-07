#! /usr/bin/python
import sys
from pytube import YouTube
import requests 
import shutil
import os
import urllib.request
class Command_function:
    
    def Youtube_Download_video(self,url,resolution,user_path):
        print(f"Wait untill few seconds.. Your  Downloader is Processing..")
        yt = YouTube(url)
        stream = yt.streams.filter(res=resolution).first()
        return_value = stream.download(output_path=user_path)
        if return_value:
            return True
        else:
            return False
        
    def Youtube_Download_video_Resolution(self,url):
        yt = YouTube(url)
        streams = yt.streams.all()
        resolutions = []
        for stream in streams:
            if 'video/mp4' in str(stream.mime_type):
                return_value = resolutions.append(stream.resolution)
        if resolutions is not None:
            return resolutions
        else:
            return False
    

    def Youtube_Download_Audio(self,url,user_path):
        print(f"Wait untill few seconds.. Your Downloader is Processing..")
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        return_value = audio.download(output_path=user_path)
        if return_value:
            return True
        else:
            return False

    # def Other_Downloading_Resources(url):
    #     print(f"Wait untill few seconds.. Your Downloader is Processing..")
    #     ydl_opts = {}
    #     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #         return_value = ydl.download(f"{[url]}")
    #     if return_value:
    #         return True
    #     else:
    #         return False
        
    def Image_Download(self,url,path,filename):
        print(f"Wait untill few seconds.. Your Downloader is Processing..")
        response = requests.get(url)
        if response.status_code == 200:
            if not os.path.exists(path):
                os.makedirs(path)
            with open(os.path.join(path, filename), "wb") as f:
                f.write(response.content)
                return True
        else:
            return False
