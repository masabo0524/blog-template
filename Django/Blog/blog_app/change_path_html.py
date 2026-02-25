from bs4 import BeautifulSoup
import os

def change_path(html_file, path_media):
    with open(html_file,"r") as html_file:
        html = html_file.read()
        soup = BeautifulSoup(html, 'html.parser')

        img = soup.find('img')
        if img:
            img_name = os.path.basename(img["src"])
            img["src"] = os.path.join(path_media, img_name)

        movie = soup.find('movie')
        if movie:
            movie_name = os.path.basename(movie["src"])
            movie["src"] = os.path.join(path_media, movie_name)
        
        new_html = str(soup)

    modified_file = os.path.join("modified_", html_file)
    with open(modified_file, "w") as save_file:
        save_file.write(new_html)
