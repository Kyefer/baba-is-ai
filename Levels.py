from Game import Entity, Level, Object, Description

levels = []


def level00():
    level = Level("00", 33, 18)
    level.setup({
        (6, 11): Entity.NOUN(Object.BABA),
        (6, 12): Entity.IS(),
        (6, 13): Entity.DESC(Description.YOU),
        (6, 19): Entity.NOUN(Object.FLAG),
        (6, 20): Entity.IS(),
        (6, 21): Entity.DESC(Description.WIN),

        (9, 16): Entity.OBJ(Object.ROCK),
        (10, 16): Entity.OBJ(Object.ROCK),
        (11, 16): Entity.OBJ(Object.ROCK),

        (7, 20): Entity.OBJ(Object.BABA),
        # (10, 12): Entity.OBJ(Object.BABA),
        (10, 20): Entity.OBJ(Object.FLAG),

        (14, 11): Entity.NOUN(Object.WALL),
        (14, 12): Entity.IS(),
        (14, 13): Entity.DESC(Description.STOP),
        (14, 19): Entity.NOUN(Object.ROCK),
        (14, 20): Entity.IS(),
        (14, 21): Entity.DESC(Description.PUSH),
    })

    walls = {}
    for i in range(11):
        walls[(8, i + 11)] = Entity.OBJ(Object.WALL)
        walls[(12, i + 11)] = Entity.OBJ(Object.WALL)
    level.setup(walls)

    return level


levels.append(level00())
