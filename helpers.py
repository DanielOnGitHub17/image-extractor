import os
import urllib.parse as parse

def check_some(book, *texts):
    """This function returns true if """
    return bool(sum(value in book for value in texts))
    

def str_attr(attrs):
    """Works for html elements with both start and end tags
    Turns the dict to string
    replace commas by nothing
    replace colons by equals
    """
    return ' '.join(f"{name}=\"{value}\"" for name, value in attrs)

def split_url(website, src):
    #use urllib.parse to query url given
    full_src = parse.urlparse(src)
    website = parse.urlparse(website)
    if not full_src.netloc:
        src_path = full_src.path
        #turn 'daniel.jpg' to 'danielongithub17.github.io/daniel.jpg'
        src = f"{website.netloc}{'' if src_path.startswith('/') else '/'}{src_path}"
    if not full_src.scheme:
        src = f"{website.scheme}://{src}"
    return src

def find_right_name(name, folder):
    name_hold = name
    same_name_count = 1
    folder = os.listdir(folder)
    #if name already exists, add a digit (like version) to the end of name
    while name in folder:
        name = f"{name_hold}_{same_name_count}"
        same_name_count += 1
    return name
