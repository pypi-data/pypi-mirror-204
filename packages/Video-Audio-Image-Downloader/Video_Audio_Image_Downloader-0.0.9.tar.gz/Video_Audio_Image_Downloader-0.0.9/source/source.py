#! /usr/bin/python
import sys
from pytube import YouTube
from .lib.Argument import Argument
from .lib.Command_function import Command_function
from .lib.help import help
# import youtube_dl
import requests 
import shutil
import urllib.request
Command_function=Command_function()
help=help()

Argument=Argument(sys.argv)

def Help():
    print("<Downloder> [Options].. ")



def main():
    
    if Argument.hasCommands(['Youtube']):
        if Argument.hasCommands(['video']): # Check the option has video or audio
            if Argument.hasOptionValue('-source'):
                if Argument.hasOptionValue('-resolution'):
                    if Argument.hasOptionValue('-path'):
                        if Argument.hasOptionValue('-resolution'):
                            url = Argument.getoptionvalue('-source')
                            resolution = Argument.getoptionvalue('-resolution')
                            path = Argument.getoptionvalue('-path')
                            if Youtube_Download_video(url,resolution,path):
                                print("Your Video is succesfully Downloaded")
                            else:
                                print("Your Video downloading operation is failed")
                                    
            elif Argument.hasOption(['-h']) or Argument.hasOption(['--help']):
                help.Youtube_Download_video_help() 
                
            elif Argument.hasOption(['-get_resolution']):
                if Argument.hasOptionValue('-get_url'):
                    url = Argument.getoptionvalue('-get_url')
                    resolution = Youtube_Download_video_Resolution(url)
                    print(f"Available Resolution :: {resolution}")
                elif Argument.hasOption(['-h']) or Argument.hasOption(['--help']):
                    help.Youtube_Download_video_Resolution_help()
                    
        else:
            help.Youtube_Download_video_help()
        
                                
        if Argument.hasCommands(['Audio']):
            if Argument.hasOptionValue('-source'):
                if Argument.hasOptionValue('-filename'):
                    if Argument.hasOptionValue('-path'):
                        url = Argument.getoptionvalue('-source')
                        path = Argument.getoptionvalue('-path')
                        filename = Argument.getoptionvalue('-filename')
                        if Youtube_Download_Audio(url,path,filename):
                            print("Your Audio file is Successfully Downloaded")
                            print(f"Your Audio file is saved in this Location :: {Argument.getoptionvalue('-path')}")
                            print(f"Your Audio file name is :: {Argument.getoptionvalue('-filename')}")
                        else:
                            print("Your Audio downloading operation is failed")
            elif Argument.hasOption(['-h']) or Argument.hasOption(['--help']):
                help.Youtube_Download_Audio_help()
            else:
                help.Youtube_Download_Audio_help()
                    
    if Argument.hasCommands(['Image']):  #TODO: to download any type of picture formates like .png, .jpg ...
        if Argument.hasOptionValue('-source'):
            if Argument.hasOptionValue('-filename'):
                if Argument.hasOptionValue('-path'):
                    url = Argument.getoptionvalue('-source')
                    path = Argument.getoptionvalue('-path')
                    filename = Argument.getoptionvalue('-filename')
                    if Command_function.Image_Download(url,path,filename):
                        print("Your Image file is Successfully Downloaded")
                        print(f"Your Image file is saved in this Location :: {Argument.getoptionvalue('-path')}")
                        print(f"Your Image file name is :: {Argument.getoptionvalue('-filename')}")
                    else:
                        print("Your Image downloading operation is failed")
                        
        elif Argument.hasOption(['-h']) or Argument.hasOption(['--help']):
            help.Image_Download_help()
        else:
            help.Image_Download_help()
    if Argument.hasOption(['-h']) or Argument.hasOption(['--help']):
        Help()
     
     
            
if __name__ == "__main__":
    main()

                
                