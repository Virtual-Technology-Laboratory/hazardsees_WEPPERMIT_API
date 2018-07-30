import math

class Slopes:

    top_slope_percent = 0
    avg_slope_percent = 0
    toe_slope_percent = 0

    top_slope = 0
    avg_slope = 0
    toe_slope = 0

    x_coord_init = 0
    y_coord_init = 0

    length = 0
    height = 0

    top_slope = 0
    avg_slope = 0
    toe_slope = 0
    x_coord_top = 0
    y_coord_top = 0
    x_coord_avg = 0
    y_coord_avg = 0
    x_coord_toe = 0
    y_coord_toe = 0

    def __init__(self, top_slope_percent, avg_slope_percent, toe_slope_percent, x_coord_init, y_coord_init):
        """Initializes the data."""
        Slopes.top_slope_percent = top_slope_percent
        Slopes.avg_slope_percent = avg_slope_percent
        Slopes.toe_slope_percent = toe_slope_percent
        Slopes.x_coord_init = x_coord_init
        Slopes.y_coord_init = y_coord_init
        Slopes.length = length

    def __convert_percent_slope_to_theta(self):
        Slopes.top_slope = Slopes.top_slope_percent * -0.9
        Slopes.avg_slope = Slopes.avg_slope_percent * -0.9
        Slopes.toe_slope = Slopes.toe_slope_percent * -0.9

    def __find_relative_coordinates(self):
        Slopes.x_coord_top = Slopes.length/3
        Slopes.y_coord_top = Slopes.x_coord_top * math.tan(math.radians(Slopes.top_slope)) # Default math is in radians, but converting to degrees is conceptually simpler in this case

        Slopes.x_coord_avg = Slopes.length/3
        Slopes.y_coord_avg = Slopes.x_coord_avg * math.tan(math.radians(Slopes.avg_slope))

        Slopes.x_coord_toe = Slopes.length/3
        Slopes.y_coord_toe = Slopes.x_coord_toe * math.tan(math.radians(Slopes.toe_slope))

    def __find_absolute_coordinates(self):
        Slopes.x_coord_top += Slopes.x_coord_init
        Slopes.y_coord_top += Slopes.y_coord_init

        Slopes.x_coord_avg += Slopes.x_coord_top
        Slopes.y_coord_avg += Slopes.y_coord_top

        Slopes.x_coord_toe += Slopes.x_coord_avg
        Slopes.y_coord_toe += Slopes.y_coord_avg

        Slopes.height = Slopes.y_coord_toe * -1


    def slope_calculations(self):
        self.__convert_percent_slope_to_theta()
        self.__find_relative_coordinates()
        self.__find_absolute_coordinates()


    @classmethod
    def current_data(hill):
        """Prints the current hillslope information."""
        print("Hillslope Data:\n")
        print("Percentage Top Slope Input = {}.".format(hill.top_slope))
        print("Percentage Avg Slope Input = {}.".format(hill.avg_slope))
        print("Percentage Toe Slope Input = {}.".format(hill.toe_slope))
        print("Length = {}.".format(hill.length))
        print("Height = {}.".format(hill.height))
        print("Points =")
        print("({},{}), ({},{}), ({},{}), ({},{})".format(hill.x_coord_init, hill.y_coord_init, hill.x_coord_top, hill.y_coord_top, hill.x_coord_avg, hill.y_coord_avg, hill.x_coord_toe, hill.y_coord_toe))



top_slope_percent = int(input("Enter Top Slope Percentage: "))
avg_slope_percent = int(input("Enter Avg Slope Percentage: "))
toe_slope_percent = int(input("Enter Toe Slope Percentage: "))
length = int(input("Enter total hillslope length (in feet): "))
x_coord_init = int(input("Preferred Starting Point X (0 if unsure): "))
y_coord_init = int(input("Preferred Starting Point Y (0 if unsure): "))
hillslope = Slopes(top_slope_percent, avg_slope_percent, toe_slope_percent, x_coord_init, y_coord_init)
hillslope.slope_calculations()
hillslope.current_data()