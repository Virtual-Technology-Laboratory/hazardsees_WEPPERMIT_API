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

    def __init__(self, top_slope_percent, avg_slope_percent, toe_slope_percent, x_coord_init, y_coord_init, length):
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
        Slopes.x_coord_top = Slopes.length * .1
        Slopes.y_coord_top = Slopes.x_coord_top * math.tan(math.radians(Slopes.top_slope)) # Default math is in radians, but converting to degrees is conceptually simpler in this case

        Slopes.x_coord_avg = Slopes.length * .8
        Slopes.y_coord_avg = Slopes.x_coord_avg * math.tan(math.radians(Slopes.avg_slope))

        Slopes.x_coord_toe = Slopes.length * .1
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
        hillslope_data = {
            "height": round(hill.height, 2),
            "x_coord_init": round(hill.x_coord_init, 2),
            "y_coord_init": round(hill.y_coord_init, 2),
            "x_coord_top": round(hill.x_coord_top, 2),
            "y_coord_top": round(hill.y_coord_top, 2),
            "x_coord_avg": round(hill.x_coord_avg, 2),
            "y_coord_avg": round(hill.y_coord_avg, 2),
            "x_coord_toe": round(hill.x_coord_toe, 2),
            "y_coord_toe": round(hill.y_coord_toe, 2)
        }
        return hillslope_data
