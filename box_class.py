class BoxPoints(object):
    """docstring"""
    def __init__(self):
        """Constructor"""
        self.__x_left = []
        self.__x_right = []
        self.__y_left = []
        self.__y_right = []
    def add_point(self, x, arg):
        if arg == 'xleft':
            self.__x_left.append(x)
        if arg == 'xright':
            self.__x_right.append(x)
        if arg == 'yleft':
            self.__y_left.append(x)
        if arg == 'yright':
            self.__y_right.append(x)
    def get_points(self, arg):
        if arg == 'xleft':
            #print(self.__x_left)
            return self.__x_left
        if arg == 'xright':
            return self.__x_right
        if arg == 'yleft':
            return self.__y_left
        if arg == 'yright':
            return self.__y_right
