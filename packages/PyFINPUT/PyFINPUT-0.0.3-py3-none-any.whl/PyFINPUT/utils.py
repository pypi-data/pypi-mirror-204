from io import TextIOWrapper

class AliasDict(dict):
    """
    A derivative of the dict class to allow for dictionary keys to be aliased.
    Stolen from jasonharper on StackOverflow (I won't tell if you don't!)
    Thanks Jason :)
    """

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.aliases = {}

    def __getitem__(self, key):
        return dict.__getitem__(self, self.aliases.get(key, key))

    def __setitem__(self, key, value):
        return dict.__setitem__(self, self.aliases.get(key, key), value)

    def add_alias(self, key, alias):
        self.aliases[alias] = key


def get_lines(file_object):
    assert isinstance(file_object, TextIOWrapper)
    return [l.strip() for l in file_object.readlines()]

def substr_in_str(string, substring, case_senstive = False):
    if not case_senstive:
        return substring.casefold() in string.casefold()
    else:
        return substring in string