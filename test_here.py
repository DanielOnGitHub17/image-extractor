import web_classes as w
html = w.get_html("tester.html", 1)
html_imgs = w.ImageFromHTML()
imgs = html_imgs.feed(html)
