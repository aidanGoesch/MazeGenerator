import pygame
import threading

import model
from helpers import *


class Grid:
    def __init__(self, dimension=40):
        if dimension < 5:  # set the minimum dimension to be 5
            print(1)
            self.dimension = 5
        else:
            self.dimension = dimension

        self.screen_dimension = 630

        self._maze = model.Maze(self.dimension, self.dimension)
        self._running = True
        self._surface = None
        self._generate = False

        # Variables used for solving
        self._depth_solving = False
        self._breadth_solving = False
        self._current_node = (0, 0)
        self._solve_timer = 0
        self._solved = False
        self._solution = []

    def run(self) -> None:
        """runs the script"""
        pygame.init()
        pygame.display.set_caption("Maze Generator & Solver")

        pygame_thread = threading.Thread(target=self.game_loop)
        pygame_thread.start()

        self._handle_events()

        pygame_thread.join()
        pygame.quit()

    def game_loop(self):
        try:
            if self.screen_dimension % self.dimension == 0:
                self._surface = pygame.display.set_mode((self.screen_dimension, self.screen_dimension))
            else:
                while self.screen_dimension % self.dimension != 0:
                    self.screen_dimension += 1

                self._surface = pygame.display.set_mode((self.screen_dimension, self.screen_dimension))

            clock = pygame.time.Clock()
            frames = 0

            can_update = True
            while self._running:
                clock.tick(60)
                frames += 1
                self._solve_timer += 1

                if not can_update:
                    self._generate = False
                    self._maze.get_maze()[self.dimension - 1][self.dimension - 1].set_value('E')

                if self._generate:
                    if frames >= 1:
                        can_update = self._maze.generate_prim()
                        frames = 0

                if self._solved:
                    self.show_solution()

                self._handle_events()
                self._draw_screen()

        finally:
            pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._generate = not self._generate
                elif event.key == pygame.K_1 and self._solve_timer >= ((self.dimension ** 2) + 10) and not self._depth_solving:
                    self._depth_solving = True
                    self.solve_depth_first(self._current_node)
                elif event.key == pygame.K_2 and self._solve_timer >= ((self.dimension ** 2) + 10) and not self._breadth_solving:
                    self._breadth_solving = True
                    self.solve_breadth_first()

    def _draw_screen(self) -> None:
        self._surface.fill(pygame.Color(0, 0, 0))

        self._draw_grid()

        pygame.display.flip()

    def _draw_grid(self) -> None:
        grid_width = self.screen_dimension // self.dimension
        temp_maze = self._maze.get_maze()

        for y in range(self.dimension):
            for x in range(self.dimension):
                top_left = x * grid_width, y * grid_width

                if temp_maze[y][x].get_value() != ' ':
                    # Draw the background and walls
                    if temp_maze[y][x].get_value() == 'B':
                        pygame.draw.rect(self._surface,
                                         pygame.Color(0, 0, 0),
                                         pygame.Rect(top_left, (grid_width, grid_width)))
                    elif temp_maze[y][x].get_value() == 'M':
                        pygame.draw.rect(self._surface,
                                         pygame.Color(255, 0, 0),
                                         pygame.Rect(top_left, (grid_width, grid_width)))

                    elif temp_maze[y][x].get_value() == "SOLUTION":
                        pygame.draw.rect(self._surface,
                                         pygame.Color(0, 255, 0),
                                         pygame.Rect(top_left, (grid_width, grid_width)))

                    self.draw_walls(temp_maze[y][x], top_left, grid_width)

                    # Draw start and end
                    pygame.draw.rect(self._surface,
                                     pygame.Color(0, 255, 0),
                                     pygame.Rect((0, 0), (grid_width, grid_width)))
                    pygame.draw.rect(self._surface,
                                     pygame.Color(0, 255, 0),
                                     pygame.Rect((self.screen_dimension - grid_width, self.screen_dimension - grid_width), (grid_width, grid_width)))
                else:
                    # Draw the grid lines
                    pygame.draw.rect(self._surface,
                                     pygame.Color(255, 255, 255),
                                     pygame.Rect(top_left, (grid_width, grid_width)), 1)

    def draw_walls(self, node: model.Node, top_left: tuple[int], grid_width: int) -> None:
        """Function that checks where each node is connected and then draws walls where the
        nodes are not connected"""
        if node.get_direction():
            if 'South' not in node.get_direction():
                pygame.draw.line(self._surface, pygame.Color(255, 255, 255),
                                 (top_left[0], top_left[1] + grid_width),
                                 (top_left[0] + grid_width, top_left[1] + grid_width))
            if 'West' not in node.get_direction():
                pygame.draw.line(self._surface, pygame.Color(255, 255, 255),
                                 (top_left[0], top_left[1] + grid_width),
                                 (top_left[0], top_left[1]))
            if 'North' not in node.get_direction():
                pygame.draw.line(self._surface, pygame.Color(255, 255, 255),
                                 (top_left[0] + grid_width, top_left[1]),
                                 (top_left[0], top_left[1]))
            if 'East' not in node.get_direction():
                pygame.draw.line(self._surface, pygame.Color(255, 255, 255),
                                 (top_left[0] + grid_width, top_left[1]),
                                 (top_left[0] + grid_width, top_left[1] + grid_width))

    def solve_depth_first(self, current_node: tuple) -> bool:
        """Recursively solves the maze by moving in every possible direction and
        then back tracking if there are no more directions to move in and the end has not
        been reached"""
        possible_directions = self._maze.get_maze()[current_node[0]][current_node[1]].get_direction()

        for direction in possible_directions:
            next_node = model.move_direction(direction, current_node)

            if -1 in next_node:
                continue
            else:
                if self._maze.get_maze()[next_node[0]][next_node[1]].get_value() == 'E':
                    return True
                elif self._maze.get_maze()[next_node[0]][next_node[1]].get_value() == 'M':
                    continue
                else:
                    if not self._solved:
                        self._maze.get_maze()[next_node[0]][next_node[1]].set_value('M')
                        pygame.time.wait(10)
                        self._draw_screen()
                        self._handle_events()
                        if self.solve_depth_first(next_node):
                            self._solved = True
                            self.compile_solution()
                            # pygame.time.wait(5000)  # this is what makes it freeze at the end
                            # quit()
                        else:
                            self._maze.get_maze()[next_node[0]][next_node[1]].set_value('B')

        return False

    def solve_breadth_first(self):
        _solving = True
        moved_nodes = [[(0, 0)]]

        while _solving:
            time_to_wait = 0
            edge_nodes = []
            for path in moved_nodes:  # gets all of the edges of the places that have been moved
                edge_nodes.append(path[-1])

            temp_node_list = []
            for i, node in enumerate(edge_nodes):  # gets a list of all the new places to move
                possible_directions  = self._maze.get_maze()[node[0]][node[1]].get_direction()
                for direction in possible_directions:
                    new_node = model.move_direction(direction, node)
                    if self._maze.get_maze()[new_node[0]][new_node[1]].get_value() != "M":  # if the place that is being moved has been visited before, don't visit it again
                        self._maze.get_maze()[new_node[0]][new_node[1]].set_value('M')

                        temp_node_list.append(moved_nodes[i] + [new_node])
                        time_to_wait += 10  # artifically slows the solving process to show the higher computational load with this solving method

                        if new_node == (self.dimension - 1, self.dimension - 1):  # check if the next node is the end
                            _solving = False
                            break


            pygame.time.wait(20)
            self._draw_screen()
            self._handle_events()

            moved_nodes = temp_node_list

        for sequence in moved_nodes:  # draws the solution
            if sequence[-1] == (self.dimension - 1, self.dimension - 1):
                for s in sequence:
                    self._maze.get_maze()[s[0]][s[1]].set_value('SOLUTION')



    def compile_solution(self):
        temp_maze = self._maze.get_maze()
        for y in range(len(temp_maze)):
            for x in range(len(temp_maze[y])):
                if temp_maze[y][x].get_value() == "M":
                    self._solution.append((y, x))

    def show_solution(self):
        for y, x in self._solution:
            self._maze.get_maze()[y][x].set_value("SOLUTION")


def main():
    running = True
    while running:
        Grid(init_dimension()).run()
        running = get_rerun()
        print(5 * '\n')


if __name__ == '__main__':
    main()
    # print(move([[(0, 0)]], [(1, 0), (0, 1)]))