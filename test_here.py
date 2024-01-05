import web_classes as w
import os

from importlib import reload
#listed in reversed chronological order
cls = lambda *nothing_really: exec("os.system('clear')")
def parse_css():
    # remember to add 'data' url support
    sample_style = r"""border-radius: fine;
    balablu: english'
    background: url("styles.css");
@import url("hi.css");
background-image: url("tellme.jpg")
;
    color: blue;
background: left right center 10% blue url("assets/tellme.jpg");
"""
    # used +1 to indicate if sth is not -1
    urls = set()
    found_url = sample_style.find("url") # use re later
    while found_url+1:
        found_closing_brackets = sample_style.find(')', found_url)
        if found_closing_brackets + 1:
            #scrape the url out and get the src inside the bracket
            url = sample_style[found_url:found_closing_brackets].strip("\'\"url( ")
            urls.add(url)
        # now find the next one
        found_url = sample_style.find("url", found_closing_brackets)
    return urls


def test_css_class():
    pass


def test_img_classes():
    html = w.get_html("https://www.squarespace.com/")
    html_img = w.ImageFromHTML("https://www.squarespace.com/")
    imgs = tuple(html_img.feed(html))
    print(len(imgs), imgs[0])
    img = w.ImageGetter()
    img.start(html_img.url, imgs[0], "imgs/")
    print(img.name)
    return {"imgs": imgs, "html_img": html_img, "img": img}
