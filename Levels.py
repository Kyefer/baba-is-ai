from Game import Entity, Level, Object, Modifier

levels = []


def level00():
    level = Level("00", 33, 18)
    level.setup_entities({
        (6, 11): Entity.NOUN(Object.BABA),
        (6, 12): Entity.IS(),
        (6, 13): Entity.MOD(Modifier.YOU),
        (6, 19): Entity.NOUN(Object.FLAG),
        (6, 20): Entity.IS(),
        (6, 21): Entity.MOD(Modifier.WIN),

        # (7, 20): Entity.OBJ(Object.BABA),

        (14, 11): Entity.NOUN(Object.WALL),
        (14, 12): Entity.IS(),
        (14, 13): Entity.MOD(Modifier.STOP),
        (14, 19): Entity.NOUN(Object.ROCK),
        (14, 20): Entity.IS(),
        (14, 21): Entity.MOD(Modifier.PUSH),
    })

    walls = {}
    for i in range(11):
        walls[(8, i + 11)] = Object.WALL
        walls[(12, i + 11)] = Object.WALL
    level.setup_objects(walls)

    level.setup_objects({
        (9, 16): Object.ROCK,
        (10, 16): Object.ROCK,
        (11, 16): Object.ROCK,
        (10, 12): Object.BABA,
        (10, 20): Object.FLAG,
    })

    return level


levels.append(level00())
