import web_classes as w

from importlib import reload
#listed in reversed chronological order

def parse_css():
    pass

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