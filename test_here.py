import web_classes as w
html = w.get_html("https://www.squarespace.com/")
html_imgs = w.ImageFromHTML("https://www.squarespace.com/")
imgs = tuple(html_imgs.feed(html))
print(len(imgs), imgs[0])
img = w.ImageGetter()

img.start(html_imgs.url, imgs[0], "imgs/")
print(img.name)
