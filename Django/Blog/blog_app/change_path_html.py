from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
import os

def Screening_path(inmemory_file, path_media):
    html = inmemory_file.read()
    decoded_html = html.decode("utf-8", errors='replace')
    soup = BeautifulSoup(html, 'html.parser')

    img = soup.find('img')
    if img:
        img_name = os.path.basename(img["src"])
        img["src"] = os.path.join(path_media, img_name)
        
    movie = soup.find('movie')
    if movie:
        movie_name = os.path.basename(movie["src"])
        movie["src"] = os.path.join(path_media, movie_name)
            
    audio = soup.find('audio')
    if audio:
        audio_name = os.path.basename(audio["src"])
        audio["src"] = os.path.join(path_media, audio_name)

    return ContentFile(str(soup).encode("utf-8"))
