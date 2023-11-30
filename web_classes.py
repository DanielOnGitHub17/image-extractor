import urllib.request as req
import urllib.parse as parse
from html.parser import HTMLParser
from pathlib import Path
import os

from helpers import *
    
class ImageFromHTML(HTMLParser):
    def __init__(self, url=''):
        super().__init__()
        self.url = url
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
        self.src = split_url(website, src)
        self.folder = folder
        file_name = Path(parse.urlparse(src).path).name
        self.name = find_right_name(file_name, folder)
        #self.get_img_data()
        
    def get_img_data(self):
        current = os.getcwd()
        os.chdir(self.folder)
        with req.urlopen(self.src) as online_img:
            with open(f"{self.name}", 'wb') as local_img:
                local_img.write(online_img.read())
        os.chdir(current)

class SVGMaker:
    def start(self, svg_text, name="svg.svg"):
        self.svg_text = svg_text
        with open(name, 'w') as svg_file:
            svg_file.write(svg_text)


class CSSParser:
    #returns the background images srcs
    def start(self, website, src):
        self.src = split_url(website, src)
        self.css_text = get_web_text(self.src)
        #now for parsing
        #implement later.
    # i might not use any module. just find 'background' and 'background-image' in text
    # get where ';' is after the attribute.
    # extract text