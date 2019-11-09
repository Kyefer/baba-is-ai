from Game import Game, Movement, Object
from Levels import level00


def test_stop():
    game = Game("STOP TEST", level00())

    game.perform(Movement.UP)
    game.perform(Movement.UP)
    game.perform(Movement.UP)

    if Object.BABA not in game.level.board[12, 9].objects:
        return False
    if Object.BABA in game.level.board[12, 8].objects:
        return False
    if Object.WALL in game.level.board[12, 7].objects:
        return False

    return True


def test_push():
    game = Game("PUSH TEST", level00())

    game.perform(Movement.RIGHT)
    game.perform(Movement.RIGHT)
    game.perform(Movement.RIGHT)
    game.perform(Movement.RIGHT)

    if Object.BABA not in game.level.board[16, 10].objects:
        return False
    if Object.ROCK not in game.level.board[16, 11].objects:
        return False
    return True

def test_win():
    game = Game("WIN TEST", level00())

    game.perform(Movement.RIGHT)
    game.perform(Movement.RIGHT)
    game.perform(Movement.RIGHT)
    game.perform(Movement.RIGHT)
    game.perform(Movement.RIGHT)
    game.perform(Movement.RIGHT)
    game.perform(Movement.RIGHT)
    return game.perform(Movement.RIGHT)

def run_tests():
    tests = [
        test_stop,
        test_push,
        test_win
    ]
    for test in tests:
        print("Running test - {:10s}".format(test.__name__))
        if not test():
            print("------------FAILED------------")
            print("ABORTING")
            return False
        else:
            print("------------SUCCESS------------")
    return True
