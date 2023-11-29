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

def find_right_name(name, folder):
    pass