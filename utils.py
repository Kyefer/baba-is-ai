from os import system, name

if name == 'nt':
    # pylint: disable=import-error
    import msvcrt
else:
    import sys
    import tty
    # pylint: disable=import-error
    import termios


class Getch:
    def __init__(self):
        try:
            self.impl = GetchWindows()
        except ImportError:
            self.impl = GetchUnix()

    def __call__(self):
        return self.impl()


class GetchUnix:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class GetchWindows:
    def __call__(self):
        return msvcrt.getch()


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


getch = Getch()
