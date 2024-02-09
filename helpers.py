import os
import urllib.parse as ps
import urllib.request as rq
from pathlib import Path
# Use cookies to prevent forbidden requests in future
def check_some(base, *possibles):
    """This function returns true if any member of possibles is present in base"""
    return any(value in base for value in possibles)
    

def str_attr(attrs):
    """Works for html elements with both start and end tags
    Turns the dict to string replace commas by nothing
    replace colons by equals
    """
    return ' ' + ' '.join(
        f"{name}=\"{value}\"" for name, value in attrs
        ) if attrs else ''

def split_url(website, src):
    #use urllib.parse to query url given
    full_src = ps.urlparse(src)
    website = ps.urlparse(website)
    if not full_src.netloc:
        src_path = full_src.path
        #turn 'daniel.jpg' to 'danielongithub17.github.io/daniel.jpg'
        src = f"{website.netloc}{'' if src_path.startswith('/') else '/'}{src_path}"
    if not full_src.scheme:
        src = f"{website.scheme}://{src}"
    return src

def find_right_name(name, folder):
    name_hold = Path(name).stem
    extension = Path(name).suffix
    same_name_count = 1
    folder = os.listdir(folder)
    #if name already exists, add a digit (like version) to the end of name
    while name in folder:
        name = f"{name_hold}_{same_name_count}{extension}"
        same_name_count += 1
    return name

def get_web_text(url, file=0):
    if file:
        with open(url, errors="ignore") as html_file:
            return html_file.read().lower()
    else:
        with rq.urlopen(url) as html_file:
            return html_file.read().decode(errors="ignore").lower()
