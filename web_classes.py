import urllib.request as rq
import urllib.parse as parse
from html.parser import HTMLParser
from pathlib import Path
import os

from helpers import *

# perhaps later, class methods will not just return a value.
# maybe they should set all gotten values to class properties
# then the main.py will be implemented to reflect this,
# or maybe just for some of the classes

# image_formats = ('.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp, '.webp', '.tiff', '.ico', '.heif', '.heic', '.svgz', '.ani')
# making it a set will ensure faster searching
image_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.tiff', '.eps', '.pdf', '.exif', '.pbm', '.pgm', '.ppm', '.pam', '.pfm', '.hdr', '.fits', '.ico', '.heif', '.bat', '.bpg', '.cgm', '.drw', '.dxf', '.emf', '.gerber', '.itc', '.sgl', '.odg', '.eps', '.raw', '.indd', '.ai', '.eps', '.pdf', '.xps', '.oxps', '.pct', '.pict', '.plt', '.wmf', '.svg', '.svgz', '.cgm', '.xar', '.sxd', '.v2d', '.vnd', '.wmz', '.emz', '.ani', '.cal', '.cin', '.fax', '.jbig', '.jng', '.mng', '.pcx', '.pict', '.pnm', '.ppm', '.qti', '.qtif', '.ras', '.tga', '.wbmp', '.xpm', '.xwd'}

class ImageFromHTML(HTMLParser):
    # the main class. Uses most others to produce result 
    # that will be returned once to the caller of self.feed
     
    def __init__(self, url=''):
        super().__init__()
        self.url = url
        self.img_srcs = set()
        self.css_srcs = set()
        self.css_texts = set()
        self.svg_texts = set()
        self.svg_found = 0
        self.css_found = 0

    def feed(self, data, url):
        # parse the html for all types of srcs
        # change later to be only url (it will get the data itself)
        super().feed(data)
        # get images from gotten css_srcs
        # update img_srcs as you get them...
        get_img_from_css = CSSParser()
        for css_src in self.css_srcs:
            self.img_srcs.update(
                get_img_from_css.start(url, css_src)
            )
        # get the image srcs from the css_texts
        for css_text in self.css_texts:
            self.img_srcs.update(
                get_img_from_css.parse_css(url, css_text)
            )
        return (self.img_srcs, self.svg_texts)
    
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
                # svg found. Start filling in the svg
                # resetting the past one in the process
                self.svg_found = 1
                attrs.append(("xmlns", "http://www.w3.org/2000/svg"))
                self.svg_text = f"<svg{str_attr(attrs)}>"
                        
            case "style":
                self.css_found = 1

        if self.svg_found and tag != "svg":
            # any other children of the svg, of course.
            self.svg_text += f"<{tag}{str_attr(attrs)}>"
                    
    def handle_data(self, data):
        if self.svg_found:
            self.svg_text += data
        if self.css_found:
            self.css_texts.add(data)
            self.css_found = 0
            
    def handle_endtag(self, tag):
        if self.svg_found:
            if tag != "svg":
                self.svg_text += f"</{tag}>\n"
            else:
                self.svg_text += "</svg>"
                self.svg_texts.add(self.svg_text)
                self.svg_found = 0

            
        
class ImageGetter:
    def start(self, website, src, folder):
        self.src = split_url(website, src)
        self.folder = folder
        file_name = Path(parse.urlparse(src).path).name
        self.name = find_right_name(file_name, folder)
        self.get_img_data()
        
    def get_img_data(self):
        with rq.urlopen(self.src) as online_img:
            with open(f"{self.name}", 'wb') as local_img:
                local_img.write(online_img.read())

class SVGMaker:
    def __init__(self):
        self.name_no = 0
    
    def start(self, svg_text, folder):
        self.name_no += 1
        self.name = find_right_name(f"svg{self.name_no}.svg", folder)
        self.svg_text = svg_text
        with open(self.name, 'w') as svg_file:
            svg_file.write(svg_text)


class CSSParser:
    #returns the background images srcs
    def start(self, website, src):
        self.website = website
        self.src = split_url(website, src)
        self.css_text = get_web_text(self.src)
        return self.parse_css(self.website, self.css_text)

    def parse_css(self, website, css_text):
        urls = set()
        found_url = css_text.find("url")
        while found_url+1:
            found_closing_brackets = css_text.find(')', found_url)
            if found_closing_brackets + 1:
            # scrape the url out and get the src inside the bracket
                url = css_text[found_url:found_closing_brackets]\
                .strip("\'\"url( ")
                # check if it is an image
                if Path(url).suffix and Path(url).suffix in  image_formats:
                    # add the website root to the url
                    url = split_url(website, url)
                    urls.add(url)
            # now find the next one
            found_url = css_text.find("url", found_closing_brackets)
        return urls
