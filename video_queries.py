import urllib.request
import re
import pafy

def yt_query(prompt):
  query = prompt + 'official audio'
  query = query.replace(' ','+')
  html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + query)
  video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
  url = 'https://www.youtube.com/watch?v=' + video_ids[0]
  video = pafy.new(url)
  return video.getbest()