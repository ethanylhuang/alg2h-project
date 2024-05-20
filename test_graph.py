from manim import *
import numpy as np

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
