import yt_dlp
import os
import json

class Controller:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': '',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                },
                {
                    'key': 'EmbedThumbnail',
                },
            ],
            'writethumbnail': True,
            'quiet':True,
        }

    def download(self, url: str):
        info = json.loads(json.dumps(yt_dlp.YoutubeDL({'quiet':True}).sanitize_info(yt_dlp.YoutubeDL({'quiet':True}).extract_info(url, download=False))))
        self.ydl_opts['outtmpl'] = os.path.join(os.path.dirname(__file__), '..', 'downloads', info['title'])
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            ydl.cache.remove()
            ydl.download([url])
        return info['title']+'.mp3'

    def delete(self, file: str):
        file_path = os.path.join(os.path.dirname(__file__),'..','downloads', file)
        if os.path.exists(file_path):
            os.remove(file_path)
        return