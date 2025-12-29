"""Import this for image extraction"""
from web_classes import ImageFromHTML, ImageGetter, SVGMaker

# functions
from helpers import get_web_text


def extract_images(url: str, destination: str = "None", is_file: bool=False) -> set[str]:
    url = input("Enter web/file url:")

    html_text = get_web_text(url, is_file=is_file)
    img_srcs, svg_texts = ImageFromHTML(url).feed(html_text, url)

    return img_srcs or svg_texts
