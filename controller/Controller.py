import youtube_dl
import os


class Controller:
    ydl_opts = None

    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '../downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    def download(self, url: str):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.cache.remove()
            ydl.download([url])
            info = ydl.extract_info(url, download=False)
            title = info['title']
        title = title.replace("|", "_").replace(":", " -")
        return title+".mp3"

    def delete(self, file: str):
        os.system('rm -rf ../downloads/\"'+file+"\"")
        return