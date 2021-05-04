class GridItem:

    def __init__(self, pos):
        self._pos = pos

    @ property
    def x(self):
        return self._pos[0]

    @ x.setter
    def x(self, value):
        self._pos[0] = value

    @ property
    def y(self):
        return self._pos[1]

    @ y.setter
    def y(self, value):
        self._pos[1] = value

    @property
    def pos(self):
        return self._pos

    
# Data structure to quickly find items on grid
class Grid:

    def __init__(self, N, items):
        self.__N = N
        self.__data = [[None for j in range(N)] for i in range(N)]

        # build and apply periodic boundaries
        for item in items:
            item.x = item.x % N
            item.y = item.y % N
            self.__data[item.x][item.y] = item

    def get(self, x, y):
        return self.__data[x][y]

    def sense(self, radius, x, y):
        tuples = []
        for i in range(-radius, radius+1):
            for j in range(-radius, radius+1):
                x_ = (x + i) % self.__N
                y_ = (y + j) % self.__N

                item = self.__data[x_][y_]

                if item is not None and (x_ != x or y_ != y):
                    tuples.append(((x_,y_), item))

        return tuples

                



