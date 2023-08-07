from setuptools import setup, find_packages
import os

requirements = os.popen("/usr/local/bin/pipreqs main --print").read().splitlines()
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='Video_Audio_Image_Downloader',
    version='0.1.0',
    author='Sridhar',
    author_email='dcsvsridhar@gmail.com',
    #  to help download videos and audio files from Youtube
    description="In this tool is help to Download the Youtube Video,Audio and Any type of Google and other site's Images",
    packages=find_packages(),
    url='https://git.selfmade.ninja/SRIDHARDSCV/audio_video_image_downloder-1',
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'Downloader=source.source:main',
        ],
    },
)
