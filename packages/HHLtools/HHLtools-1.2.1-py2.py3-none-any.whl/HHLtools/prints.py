from HHLtools.Herror import *
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
    DEFAULT = 0
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PURPLE = 45
    CYAN = 46
    WHITE = 47

def prints(content,fontStyle=FontStyle.DEFAULT,fontColor=FontColor.WHITE,backgroundColor=BackgroundColor.DEFAULT):
    if type(fontStyle) != int:
        error(TypeError, f'the fontStyle must an integer, not {str(type(fontStyle))[7:-1]}')
    if type(fontColor) != int:
        error(TypeError, f'the fontColor must an integer, not {str(type(fontColor))[7:-1]}')
    if type(backgroundColor) != int:
        error(TypeError, f'the backgroundColor must an integer, not {str(type(backgroundColor))[7:-1]}')
    if fontStyle < 0:
        error(TypeError, f'the fontStyle must an positive integer')
    if fontColor < 0:
        error(TypeError, f'the fontColor must an positive integer')
    if backgroundColor < 0:
        error(TypeError, f'the backgroundColor must an positive integer')

    print("\033[{};{};{}m{}\033[0m".format(fontStyle,fontColor,backgroundColor,content))


