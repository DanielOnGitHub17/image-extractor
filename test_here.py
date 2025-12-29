import web_classes as w


def parse_css() -> set[str]:
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
    urls: set[str] = set()
    found_url = sample_style.find("url")  # use re later
    while found_url + 1:
        found_closing_brackets = sample_style.find(")", found_url)
        if found_closing_brackets + 1:
            # scrape the url out and get the src inside the bracket
            url = sample_style[found_url:found_closing_brackets].strip("'\"url( ")
            urls.add(url)
        # now find the next one
        found_url = sample_style.find("url", found_closing_brackets)
    return urls


def test_css_class():
    pass


def test_img_classes() -> (
    dict[str, tuple[set[str], set[str]] | w.ImageFromHTML | w.ImageGetter]
):
    html = w.get_web_text("https://www.squarespace.com/")
    html_img = w.ImageFromHTML()
    imgs = html_img.feed(html, "https://www.squarespace.com/")
    print(len(imgs), imgs[0])
    img = w.ImageGetter()
    img.start(html_img.url, imgs[0].pop(), "imgs/")
    print(img.name)
    return {"imgs": imgs, "html_img": html_img, "img": img}
