import urllib.request as req
import urllib.parse as parse
from html.parser import HTMLParser
from pathlib import Path
import os

from helpers import *

def get_html(url, file=0):
    if file:
        with open(url, errors="ignore") as html_file:
            return html_file.read().lower()
    else:
        with req.urlopen(url) as html_file:
            return html_file.read().decode(errors="ignore").lower()

    
class ImageFromHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.img_srcs = set()
        self.css_srcs = set()
        self.css_texts = set()
        self.svg_texts = set()
        self.svg_found = 0
        self.css_found = 0

    def feed(self, data):
        super().feed(data)
        return self.img_srcs
    
    def handle_starttag(self, tag, attrs):
        match tag:
        
            case "img":
                #print("img")
                attributes = dict(attrs)
                if "src" in attributes:
                    self.img_srcs.add(attributes["src"])
                
            case "link":
                #print("link")
                attributes = dict(attrs)
                #check if rel value contains logo/icon/#addmore 
                if ("rel" in attributes):
                    if "href" in attributes:
                        if check_some(attributes["rel"], "logo", "icon"):
                            self.img_srcs.add(attributes["href"])
                        elif attributes["rel"]=="stylesheet":
                            self.css_srcs.add(attributes["href"])
                            #do the css parsing for backgrounds later
            case "svg":
                self.svg_found = 1
                self.svg_text = f"<svg {str_attr(attrs)}>"
                        
            case "style":
                attributes = dict(attrs)
                self.css_found = 1
                    
    def handle_data(self, data):
        if self.svg_found:
            self.svg_texts.add(self.svg_text+data+"</svg>")
            self.svg_found = 0
        if self.css_found:
            self.css_texts.add(data)
            self.css_found = 0
            
        
class ImageGetter:
    def start(self, website, src, folder):
        #use urllib.parse to query url given
        full_src = parse.urlparse(src)
        website = parse.urlparse(website)
        if not full_src.netloc:
            src_path = full_src.path
            #turn 'daniel.jpg' to 'danielongithub17.github.io/daniel.jpg'
            src = f"{website.netloc}{'' if src_path.startswith('/') else '/'}{src_path}"
        if not full_src.scheme:
            src = f"{website.scheme}://{src}"
        
        self.src = src
        self.folder = folder
        _name = Path(parse.urlparse(src).path).name
        name_ = _name
        same_name_count = 1
        images = os.listdir(folder)
        #if name already exists, add a digit (like version) to the end of name
        while _name in images:
            _name = f"{same_name_count}{name_}"
            same_name_count += 1
        self.name = _name
        self.get_img_data()
        
    def get_img_data(self):
        current = os.getcwd()
        os.chdir(self.folder)
        with req.urlopen(self.src) as online_img:
            with open(f"{self.name}", 'wb') as local_img:
                local_img.write(online_img.read())
        os.chdir(current)

class CSSParser:
    def start(self, website, src, folder):
        pass
    # i might not use any module. just find 'background' and 'background-image' in text
    # get where ';' is after the attribute.
    # extract text