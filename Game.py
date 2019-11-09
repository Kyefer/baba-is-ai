from __future__ import annotations

from enum import Enum
from typing import Dict, Callable, List, Tuple


import numpy as np


class Object(Enum):
    BABA = 1
    FLAG = 2
    WALL = 3
    ROCK = 4
    KEY = 5
    WATER = 6
    COG = 7
    ROBOT = 8


class Link(Enum):
    IS = 1
    AND = 2


class Modifier(Enum):
    YOU = 1
    WIN = 2
    STOP = 3
    PUSH = 4
    MOVE = 5
    FLOAT = 6
    HOT = 7
    SINK = 8
    DEFEAT = 9


class EntityType(Enum):
    OBJ = 1
    NOUN = 2
    LINK = 3
    MOD = 4


class Entity():
    def __init__(self, name: str, entity_type: EntityType, subtype=None):
        self.name = name
        self.type = entity_type
        self.subtype = subtype

    def __str__(self) -> str:
        return "{}[{}]".format(self.name, self.type.name)

    @classmethod
    def IS(cls) -> Entity:
        return Entity(Link.IS.name, EntityType.LINK, Link.IS)

    @classmethod
    def AND(cls) -> Entity:
        return Entity(Link.AND.name, EntityType.LINK, Link.AND)

    @classmethod
    def NOUN(cls, obj: Object) -> Entity:
        return Entity(obj.name, EntityType.NOUN, obj)

    @classmethod
    def MOD(cls, desc: Modifier) -> Entity:
        return Entity(desc.name, EntityType.MOD, desc)


class Tile:
    def __init__(self):
        self.entity: Entity = None
        self.objects: List[Object] = []

    def view(self, rules) -> Tuple(str, str):
        if self.entity:
            return Tile.split4(self.entity.name)

        if not self.objects:
            return ("  ", "  ")

        for obj in self.objects:
            if obj in rules[Modifier.YOU]:
                return Tile.split4(obj.name.lower())

        for obj in self.objects:
            if obj in rules[Modifier.PUSH]:
                return Tile.split4(obj.name.lower())

        for obj in self.objects:
            if obj in rules[Modifier.STOP]:
                return Tile.split4(obj.name.lower())

        return Tile.split4(self.objects[0].name.lower())

    @classmethod
    def split4(cls, name):
        name4 = name + " " * (4 - len(name))
        return (name4[:2], name4[2:])


class Level:
    def __init__(self, descriptor: str, width: int, height: int):
        self.descriptor = descriptor
        self.width = width
        self.height = height
        self.board = np.array([[Tile() for _ in range(height)] for _ in range(width)], dtype=Tile)

    def setup_entities(self, entities: Dict[np.ndarray, Entity]):
        for pos, entity in entities.items():
            self.board[pos].entity = entity

    def setup_objects(self, objects: Dict[np.ndarray, Object]):
        for pos, obj in objects.items():
            self.board[pos].objects.append(obj)

    def copy(self) -> Level:
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
        self.rules = self.parse_rules()

    def parse_rules(self):
        rules = {
            Modifier.YOU: set(),
            Modifier.WIN: set(),
            Modifier.STOP: set(),
            Modifier.MOVE: set(),
            Modifier.PUSH: set()
        }

        for j in range(self.level.height - 2):
            for i in range(self.level.width - 2):
                cell00 = self.level.board[i, j].entity
                cell01 = self.level.board[i, j+1].entity
                cell02 = self.level.board[i, j+2].entity
                cell10 = self.level.board[i+1, j].entity
                cell20 = self.level.board[i+2, j].entity

                if cell00 and cell01 and cell02 and cell00.type is EntityType.NOUN and cell01.subtype is Link.IS and cell02.type is EntityType.MOD:
                    rules[cell02.subtype].add(cell00.subtype)

                if cell00 and cell10 and cell20 and cell00.type is EntityType.NOUN and cell10.subtype is Link.IS and cell20.type is EntityType.MOD:
                    rules[cell20.subtype].add(cell00.subtype)

        return rules

    def perform(self, action: Movement):
        if not self.in_progress:
            print("Starting game '{}' playig level '{}'".format(self.desciptor, self.initial_level.descriptor))
            self.in_progress = True

        self.rules = self.parse_rules()
        you_indexes = self.find(lambda tile: set(tile.objects) & self.rules[Modifier.YOU])

        if action is Movement.LEFT:
            delta = np.array((-1, 0))
        elif action is Movement.RIGHT:
            delta = np.array((1, 0))
        elif action is Movement.UP:
            delta = np.array((0, -1))
        elif action is Movement.DOWN:
            delta = np.array((0, 1))
        else:
            return False

        will_move = []
        for you_idx in you_indexes:
            you = self.level.board.item(*you_idx)

            adj_idx = list(you_idx + delta)
            adj = self.level.board.item(*adj_idx)

            tiles = [(you, adj)]

            while self.has_entity(adj):
                if set(adj.objects) & self.rules[Modifier.STOP]:
                    tiles = []
                    break

                adj_idx = list(np.array(adj_idx) + delta)
                nxt = self.level.board.item(*adj_idx)
                tiles = [(adj, nxt)] + tiles
                adj = nxt

            will_move += tiles

        for tile_a, tile_b in will_move:
            self.move_entity(tile_a, tile_b)

        self.level = self.level_next
        self.level_next = self.level_next.copy()

        you_indexes = self.find(lambda tile: set(tile.objects) & self.rules[Modifier.YOU])
        win_indexes = self.find(lambda tile: set(tile.objects) & self.rules[Modifier.WIN])

        return you_indexes & win_indexes

    def find(self, func: Callable[[Entity], bool]):
        pos = set()
        for j in range(self.level.height):
            for i in range(self.level.width):
                if func(self.level.board[i, j]):
                    pos.add((i, j))
        return pos

    def move_entity(self, a: Tile, b: Tile):
        if a.entity:
            b.entity = a.entity
            a.entity = None
        else:
            for obj in a.objects:
                if obj in self.rules[Modifier.YOU].union(self.rules[Modifier.PUSH]):
                    b.objects.append(obj)
                    a.objects.remove(obj)
                    break

    def has_entity(self, tile) -> bool:
        return tile.entity or set(tile.objects) & self.rules[Modifier.PUSH].union(self.rules[Modifier.STOP])

    def __str__(self) -> str:
        lines = []
        for j in range(self.level.height):
            line = [" ", " "]
            for i in range(self.level.width):
                tile = self.level.board[i, j]
                in_board = tile.view(self.parse_rules())
                line[0] += in_board[0]
                line[1] += in_board[1]

                if i < self.level.width - 1:
                    line[0] += " | "
                    line[1] += " | "
            lines += line
            if j < self.level.height - 1:
                lines.append("-" * (5 * self.level.width - 1))
        return "\n".join(lines)
