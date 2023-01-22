# youtube search scraper
import requests
import json
from bs4 import BeautifulSoup
import re

response = requests.get(
    "https://www.youtube.com/results?search_query=indonesia").text

soup = BeautifulSoup(response, 'lxml')

try:
    script = soup.find_all('script', text=re.compile('ytInitialData'))
    json_text = re.search(
        r'ytInitialData = ({.*?});', script[0].string, re.DOTALL).group(1)
    with open('data.json', 'w', encoding="utf-8") as outfile:
        outfile.write(json_text)
    json_data = json.loads(json_text)
    contents = json_data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
    with open('contents.json', 'w', encoding="utf-8") as outfile:
        outfile.write(json.dumps(contents))
    for i, content in enumerate(contents):
        if 'itemSectionRenderer' in content:
            for item in content['itemSectionRenderer']['contents']:
                if 'videoRenderer' in item:
                    video = item['videoRenderer']
                    title = video['title']['runs'][0]['text']
                    video_id = video['videoId']
                    published_time = video['publishedTimeText']['simpleText']
                    view_count = video['viewCountText']['simpleText']
                    obj = {
                        "title": title,
                        "video_id": video_id,
                        "published_time": published_time,
                        "view_count": view_count,
                    }
                    print("Video:", obj)
                elif 'playlistRenderer' in item:
                    playlist = item['playlistRenderer']
                    title = playlist['title']['simpleText']
                    playlist_id = playlist['playlistId']
                    video_count = playlist['videoCount']
                    obj = {
                        "title": title,
                        "playlist_id": playlist_id,
                        "video_count": video_count,
                    }
                    print("Playlist:", obj)
except Exception as e:
    print(str(e))
