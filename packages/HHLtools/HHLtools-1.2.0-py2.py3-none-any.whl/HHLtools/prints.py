class FontStyle:
    DEFAULT = 0
    BOLD = 1
    UNDERLINE = 4
    BLINK = 5
    REVERSE = 7

class FontColor:
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    WHITE = 37

class BackgroundColor:
    DEFAULT = ''
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PURPLE = 45
    CYAN = 46
    WHITE = 47

def prints(content,fontStyle=FontStyle.DEFAULT,fontColor=FontColor.WHITE,backgroundColor=BackgroundColor.DEFAULT):
    print("\033[{};{};{}m{}\033[0m".format(fontStyle,fontColor,backgroundColor,content))
