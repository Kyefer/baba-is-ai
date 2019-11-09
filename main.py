from Levels import levels
from Game import Game, Movement
from utils import getch, clear

keyboard_mapping = {
    b'w': Movement.UP,
    b's': Movement.DOWN,
    b'a': Movement.LEFT,
    b'd': Movement.RIGHT,
    b'e': None,
    b'H': Movement.UP,
    b'P': Movement.DOWN,
    b'K': Movement.LEFT,
    b'M': Movement.RIGHT,
}


def get_action():
    action = getch()

    if action in keyboard_mapping.keys():
        action = keyboard_mapping[action]
    elif action is b'\xe0':
        action = getch()
        action = keyboard_mapping[action]
    else:
        action = Movement.NOTHING
    return action


def loop(game):
    clear()
    print(game)

    action = get_action()
    while action:
        res = game.perform(action)

        clear()
        print(game)
        
        if not res:
            action = get_action()
        else:
            print("YOU WIN!")
            break


if __name__ == "__main__":
    game = Game("Test Game", levels[0])

    loop(game)
