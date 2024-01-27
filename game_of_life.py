import random
from time import time


class Life:
    """Cell class for Game of Life."""

    def __init__(self, x, y, alive=False, color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.alive = alive
        self.color = color

    def _clone(self):
        return Life(self.x, self.y, self.alive, self.color)

    def __hash__(self):
        return str(self.x) + " " + str(self.y)

    def __repr__(self):
        return f"Life: x={self.x} y={self.y}"


class GameOfLife:
    """Game Of Life simulation class."""

    def __init__(
        self,
        width=0,
        height=0,
        random_count=30,
        color_old=(128, 0, 128),
        color_new=(255, 0, 0),
        coords=None,
        custom=False,
    ):
        self.lives = [[Life(j, i) for j in range(width)] for i in range(height)]
        self.count = 0
        self.height = height
        self.width = width
        self.random_count = random_count
        self.color_new = color_new
        self.color_old = color_old
        self.coords = coords
        if custom:
            self.initialize(width, height, [(-1, -1)])
            self.custom_coords = dict()
        else:
            self.initialize(width, height, coords)

    def update(self):
        """progress step for game of life.

        Returns:
            is_updated: bool, whether any changes are made.
        """
        new_lives = [[col._clone() for col in row] for row in self.lives]
        is_updated = False
        for row in self.lives:
            for life in row:
                count = self.get_neighbors(life, life.alive)
                if life.alive and count not in (2, 3):
                    new_lives[life.y][life.x].alive = False
                    is_updated = True
                elif life.alive and count in (2, 3):
                    new_lives[life.y][life.x].color = self.color_old
                    self.count -= 1
                elif not life.alive and count == 3:
                    new_lives[life.y][life.x].alive = True
                    new_lives[life.y][life.x].color = self.color_new
                    is_updated = True
                    self.count += 1
        self.lives = new_lives
        return is_updated

    def restart(self):
        """restart the game of life."""
        self.lives = [
            [Life(j, i) for j in range(self.width)] for i in range(self.height)
        ]
        self.initialize(self.width, self.height, self.coords)

    def initialize(self, width, height, coords):
        """initialize game of life cells with alive information.

        Args:
            width (int): width of grid
            height (int): height of grid
            coords (iterable[tuple(int, int)]): alive cells coordinates.
        """
        self.count = 0
        if coords:
            for i, j in coords:
                try:
                    self.get(i, j).alive = True
                    self.get(i, j).color = self.color_new
                    self.count += 1
                except ValueError:
                    pass
        else:
            self.coords = list()
            for i in range(width):
                for j in range(height):
                    if random.random() > 1.0 - (self.random_count / (width * height)):
                        self.get(i, j).alive = True
                        self.get(i, j).color = self.color_new
                        self.coords.append((i, j))
                        self.count += 1

    def get_neighbors(self, life, alive):
        """get neighbors of life cell.

        Args:
            life (Life): cell for which need to find neighbors.
            alive (boolean): whether life cell is alive.

        Returns:
            int: count of neighbors.
        """
        count = 0
        x, y = life.x, life.y
        for i in [-1, 0, +1]:
            for j in [-1, 0, +1]:
                if i == 0 and j == 0:
                    continue
                try:
                    if self.get(x + i, y + j).alive:
                        count += 1
                    if alive and count > 3:
                        return count
                except ValueError:
                    pass
        return count

    def get(self, x, y):
        """get cell at x, y position."""
        if not (0 <= y < self.height and 0 <= x < self.width):
            raise ValueError
        return self.lives[y][x]

    def get_coords(self):
        """get coordinates of currently alive cells."""
        return [
            (j, i)
            for j in range(self.width)
            for i in range(self.height)
            if self.lives[i][j].alive
        ]

    def toggle_cell(self, x, y):
        """toggle alive state for cell at x,y position."""
        cell = self.get(x, y)
        dt = time() - self.custom_coords.get((x, y), 0)
        if dt > 0.5:
            self.custom_coords[(x, y)] = time()
            if cell.alive:
                cell.alive = False
                self.count -= 1
            else:
                cell.color = self.color_new
                cell.alive = True
                self.count += 1
