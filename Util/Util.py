import re 

def sort_alphanumeric(data):
    """ Sorts a list alphanumerically """
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0.9]+)', key)]
    return(sorted(data, key=alphanum_key))