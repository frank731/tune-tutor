import yt_dlp

URLS = ['https://www.youtube.com/watch?v=t7MBzMP4OzY']

ydl_opts = {
    'format': 'bestaudio',
    'outtmpl': '%(id)s.mp3',
    'extract_audio': True
}

id = ""


with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URLS)
    #y, sr = librosa.load(f"{ydl.extract_info(URLS[0], download=False)['id']}.mp3")
    #id_chord(y, sr)