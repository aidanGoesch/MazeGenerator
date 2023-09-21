import random


class Node:
    def __init__(self) -> None:
        self._value = ' '
        self._direction = []

    def set_value(self, value: str) -> None:
        self._value = value

    def get_value(self) -> str:
        return self._value

    def add_direction(self, direction: tuple[int]) -> None:
        """Adds the direction of what the node is connected to"""
        if direction == (1, 0):
            self._direction.append('North')
        elif direction == (-1, 0):
            self._direction.append('South')
        elif direction == (0, 1):
            self._direction.append('West')
        elif direction == (0, -1):
            self._direction.append('East')
        else:
            print('ERROR')

    def set_direction(self, direction: tuple[int]) -> None:
        """Sets the direction of what the node is connected to"""
        if direction == (-1, 0):
            self._direction.append('North')
        elif direction == (1, 0):
            self._direction.append('South')
        elif direction == (0, -1):
            self._direction.append('West')
        elif direction == (0, 1):
            self._direction.append('East')
        else:
            print('ERROR')

    def get_direction(self) -> list:
        return self._direction


class Maze:
    def __init__(self, width: int, height: int) -> None:
        self._width = width

        self._maze = [[Node() for x in range(width)] for y in range(width)]

        self._maze[0][0].set_value('M')
        self._maze[self._width - 1][self._width - 1].set_value('E')

        self._visited = [(0, 0)]  # creates the visited list with the first index being the start

    def get_maze(self) -> list[list[Node]]:
        return self._maze

    def add_visited(self, point: tuple[int, int], direction: tuple[int, int]) -> bool:
        point_y, point_x = point
        dir_y, dir_x = direction

        new_point = (point_y + dir_y, point_x + dir_x)

        if new_point in self._visited:
            return False
        else:
            self._maze[new_point[0]][new_point[1]].set_value('B')
            self._maze[new_point[0]][new_point[1]].add_direction(direction)
            self._visited.append(new_point)
            return True

    def get_visited(self) -> list[tuple]:
        return self._visited

    def get_possible_directions(self, coor: tuple[int, int]) -> list[str]:
        """returns a list of possible directions at a given coordinate"""
        possible_dirs = ['North', 'South', 'East', 'West']
        coor_y, coor_x = coor

        if coor_x - 1 < 0:
            possible_dirs.remove('West')
        if coor_x + 1 >= len(self._maze[0]):
            possible_dirs.remove('East')
        if coor_y - 1 < 0:
            possible_dirs.remove('North')
        if coor_y + 1 >= len(self._maze):
            possible_dirs.remove('South')

        return possible_dirs

    def generate_prim(self) -> bool:
        if len(self._visited) < self._width ** 2:
            added = False
            while not added:
                # get a random visited point
                point = random.choice(self._visited)

                # get the possible directions
                direction = get_rand_direction(self.get_possible_directions(point))

                added = self.add_visited(point, direction)
            self._maze[point[0]][point[1]].set_direction(direction)
            return True
        else:
            return False


def move_direction(direction: str, current_node: tuple) -> bool | tuple:
    direction_dict = {
        'North': (-1, 0),
        'South': (1, 0),
        'East': (0, 1),
        'West': (0, -1)
    }

    move = direction_dict[direction]

    return current_node[0] + move[0], current_node[1] + move[1]


def get_rand_direction(possible_directions: list[str]) -> tuple[int]:
    direction_dict = {
        'North': (-1, 0),
        'South': (1, 0),
        'East': (0, 1),
        'West': (0, -1)
    }

    return direction_dict[random.choice(possible_directions)]
