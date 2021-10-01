import discord
import asyncio
import pafy
import re
import urllib.request

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(ytdl, url):
        if not url.startswith('https://www.youtube.com/watch?v='):
                query = url.replace(' ','+')
                html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + query)
                video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
                url = 'https://www.youtube.com/watch?v=' + video_ids[0]
        filename = pafy.new(url)
        return filename.getbest()