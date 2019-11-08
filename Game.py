from enum import Enum
from typing import Dict, Callable

import numpy as np


class Object(Enum):
    BABA = 1
    FLAG = 2
    WALL = 3
    ROCK = 4
    KEY = 5


class Link(Enum):
    IS = 1
    AND = 2


class Description(Enum):
    YOU = 1
    WIN = 2
    STOP = 3
    PUSH = 4
    MOVE = 5


class EntityType(Enum):
    EMPTY = 0
    OBJ = 1
    NOUN = 2
    LINK = 3
    DESC = 4


class Entity():
    def __init__(self, name: str, entity_type: EntityType, subtype=None):
        self.name = name
        self.type = entity_type
        self.subtype = subtype

        if len(name) > 4:
            # error
            pass

    def __str__(self):
        return "{}[{}]".format(self.name, self.type.name)

    def in_board(self):
        name4 = self.name + " " * (4 - len(self.name))
        return [name4[:2], name4[2:]]

    @classmethod
    def EMPTY(cls):
        return Entity("", EntityType.EMPTY)

    @classmethod
    def IS(cls):
        return Entity("IS", EntityType.LINK, Link.IS)

    @classmethod
    def AND(cls):
        return Entity("AND", EntityType.LINK, Link.AND)

    @classmethod
    def OBJ(cls, obj: Object):
        return Entity(obj.name.lower(), EntityType.OBJ, obj)

    @classmethod
    def NOUN(cls, obj: Object):
        return Entity(obj.name, EntityType.NOUN, obj)

    @classmethod
    def DESC(cls, desc: Description):
        return Entity(desc.name, EntityType.DESC, desc)


class Level:
    def __init__(self, descriptor: str, width: int, height: int):
        self.descriptor = descriptor
        self.width = width
        self.height = height
        self.board: np.ndarray = np.full((height, width), Entity.EMPTY())

    def setup(self, entities: Dict[np.ndarray, Entity]):
        for pos, entity in entities.items():
            self.board[pos] = entity

    def __str__(self):
        lines = []
        for i in range(self.height):
            line = ["", ""]
            for j in range(self.width):
                cell = self.board[i, j]
                in_board = cell.in_board()
                line[0] += in_board[0]
                line[1] += in_board[1]

                if j < self.width - 1:
                    line[0] += " | "
                    line[1] += " | "
            lines += line
            if i < self.height - 1:
                lines.append("-" * (5 * self.width - 1))
        return "\n".join(lines)

    def copy(self) -> "Level":
        new = Level(self.descriptor, self.width, self.height)
        new.board = np.copy(self.board)
        return new


class Movement(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    NOTHING = 5


class Game:
    def __init__(self, desciptor, level: Level):
        self.desciptor = desciptor
        self.in_progress = False
        self.level = level.copy()
        self.level_next = level.copy()
        self.initial_level = level.copy()

    def perform(self, action: Movement):
        if not self.in_progress:
            print("Starting game {} playig level {}".format(self.desciptor, self.initial_level.descriptor))
            self.in_progress = True

        rules = self.parse_rules()
        yous = self.find(lambda ent: ent.type is EntityType.OBJ and ent.subtype in rules[Description.YOU])
        moves = self.find(lambda ent: ent.type is EntityType.OBJ and ent.subtype in rules[Description.MOVE])

        if action is Movement.LEFT:
            delta = np.array((0, -1))
        elif action is Movement.RIGHT:
            delta = np.array((0, 1))
        elif action is Movement.UP:
            delta = np.array((-1, 0))
        elif action is Movement.DOWN:
            delta = np.array((1, 0))
        else:
            return

        will_move = []
        for you in yous:
            entities = [you]

            adj = list(you + delta)
            cell = self.level.board.item(*adj)
            while not self.empty(adj):
                cell = self.level.board.item(*adj)
                if cell.type is EntityType.OBJ and cell.subtype in rules[Description.STOP]:
                    entities = []
                    break
                elif cell.type is EntityType.OBJ and cell.subtype in rules[Description.PUSH]:
                    pass
                elif cell.type is EntityType.OBJ:
                    # Neither stop nor push -- treat as empty
                    break

                entities = [adj] + entities
                adj = list(np.array(adj) + delta)
            # if action is Movement.DOWN or action is Movement.RIGHT:
            will_move += entities
            # else:
            #     will_move += entities

        for move in will_move:
            self.move(move, delta)

        self.level = self.level_next
        self.level_next = self.level_next.copy()

        
        yous = self.find(lambda ent: ent.type is EntityType.OBJ and ent.subtype in rules[Description.YOU])
        moves = self.find(lambda ent: ent.type is EntityType.OBJ and ent.subtype in rules[Description.MOVE])
        wins = self.find(lambda ent: ent.type is EntityType.OBJ and ent.subtype in rules[Description.WIN])

        # if not (yous + moves):
        #     print("Failed")
        #     return False
        # elif np.intersect1d(yous, wins):
        #     print("You Win")
        #     return True

    def parse_rules(self):
        rules = {
            Description.YOU: [],
            Description.WIN: [],
            Description.STOP: [],
            Description.MOVE: [],
            Description.PUSH: []
        }

        for i in range(self.level.height - 2):
            for j in range(self.level.width - 2):
                cell00 = self.cell(i, j)
                cell01 = self.cell(i, j + 1)
                cell02 = self.cell(i, j + 2)
                cell10 = self.cell(i + 1, j)
                cell20 = self.cell(i + 2, j)

                if cell00.type is EntityType.NOUN and cell01.subtype is Link.IS and cell02.type is EntityType.DESC:
                    rules[cell02.subtype].append(cell00.subtype)

                if cell00.type is EntityType.NOUN and cell10.subtype is Link.IS and cell20.type is EntityType.DESC:
                    rules[cell20.subtype].append(cell00.subtype)

        return rules

    def cell(self, row, col) -> Entity:
        return self.level.board[row, col]

    def find(self, func: Callable[[Entity], bool]):
        pos = []
        for i in range(self.level.height):
            for j in range(self.level.width):
                if func(self.level.board[i, j]):
                    pos.append((i, j))
        return pos

    def move(self, pos, delta):
        new = list(np.array(pos) + delta)
        self.level_next.board[new[0], new[1]] = self.level_next.board.item(*pos)
        self.level_next.board[pos[0], pos[1]] = Entity.EMPTY()

    def empty(self, pos):
        return self.level.board.item(*pos).type == EntityType.EMPTY
