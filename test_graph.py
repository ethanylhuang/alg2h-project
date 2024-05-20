from manim import *
import numpy as np
import copy

config.frame_height = 10
config.frame_width = 10
config.pixel_width = 1000
config.pixel_height = 1000
class MakeFibSquares(MovingCameraScene):

    def construct(self):
        fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711]
        dir = ["DOWN", "RIGHT", "UP", "LEFT"]

        #initialize curr_points for side length 1 square
        curr_points = {
            "bottom_left" : [0, 0, 0],
            "bottom_right" : [1, 0, 0],
            "top_right" : [1, 1, 0],
            "top_left" : [0, 1, 0]
        }

        square_points = [
            [
                [0, 0, 0],
                [1, 0, 0],
                [1, 1, 0],
                [0, 1, 0]
            ]
        ]

        for i in range (0, 9):
            #create square with curr_points
            points = list(curr_points.values())
            square = Polygon(*points, color=WHITE)

            #create text with value curr fib value
            text = Text(str(fib[i]))
            text.move_to(square.get_center())
            if (i < 5):
                self.play(Create(square))
            else:
                self.play(Create(square), run_time=0.3)
            self.play(self.camera.frame.animate.scale(np.power(1.05, i+1)))

            curr_direction = dir[i % 4]
            if curr_direction == "DOWN":
                curr_points ["bottom_left"][1] -= fib[i+1]
                curr_points ["bottom_right"][1] -= fib[i+1]
                print(curr_points)

            if curr_direction == "RIGHT":
                curr_points["top_right"][0] += fib[i+1]
                curr_points["bottom_right"][0] += fib[i+1]
                print(curr_points)

            if curr_direction == "UP":
                curr_points["top_left"][1] += fib[i+1]
                curr_points["top_right"][1] += fib[i+1]
                print(curr_points)

            if curr_direction == "LEFT":
                curr_points["top_left"][0] -= fib[i+1]
                curr_points["bottom_left"][0] -= fib[i+1]
                print(curr_points)


        self.wait(2)
class DrawLogSpiral(MovingCameraScene):
    def construct(self):
        plane = (NumberPlane(x_range=[-100, 100], y_range=[-100, 100], axis_config={"color": WHITE}).add_coordinates())
        labels = plane.get_axis_labels(x_label="x", y_label="y")

        self.play(DrawBorderThenFill(plane), Write(labels))

        golden_ratio = (1 + np.sqrt(5)) / 2

        a = 1
        b = np.log(golden_ratio) / (np.pi / 2)

        theta_values = np.linspace(0, 4 * PI, 1000)
        r_values = a * np.exp(b * theta_values)

        x_values = r_values * np.cos(theta_values)
        y_values = r_values * np.sin(theta_values)

        spiral_points = np.column_stack([x_values, y_values, np.zeros_like(x_values)])

        spiral = VMobject().set_points_as_corners(spiral_points)
        self.play(Create(spiral), run_time=5)


        self.wait(3)