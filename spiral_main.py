from manim import *
import numpy as np
import os

debug = open("debug.txt", "w")
def fib(n):
    fibs = [1, 1]
    for i in range (2, n+1):
        fibs.append(fibs[-1] + fibs[-2])

    return fibs[-1]
def draw_fib_squares():
    dir = [UP, LEFT, DOWN, RIGHT]
    corners = [UL, UR]
    angles = [-PI / 2, PI / 2, PI / 2, -PI / 2]

    squares = VGroup()
    arcs = VGroup()
    nums = VGroup()

    for i in range(0, 15):
        square = Square(side_length=fib(i), color=WHITE, stroke_width=20)

        if i == 0:
            square.shift(-square.get_corner(DL))
        else:
            square.next_to(squares, dir[i % 4], buff=0)

        points = [square.get_corner(corners[i % 2]), square.get_corner(-corners[i % 2])]
        arcs.add(ArcBetweenPoints(points[0], points[1], angle=angles[i % 4], color=BLUE, stroke_width=20))
        squares.add(square)

        num = Text(str(fib(i)))
        num.move_to(square.get_center())
        nums.add(num)

    return squares, nums, arcs


def draw_plane(squares):
    plane = (NumberPlane(x_range=[-10, 10], y_range=[-10, 10], axis_config={"color": WHITE}).add_coordinates())
    labels = plane.get_axis_labels(x_label="x", y_label="y")

    plane.move_to(squares[0].get_corner(DL))
    print(squares[0].get_corner(DL))
    plane.scale(1 / squares[0].get_width())
    plane.shift(0.12 * RIGHT)
    plane.shift(0.12 * DOWN)

    return plane, labels


def draw_log_spiral():
    golden_ratio = (1 + np.sqrt(5)) / 2
    print(golden_ratio)
    a = 1
    b = (2 * np.log(golden_ratio)) / PI

    start_angle = 0
    def polar_to_cartesian(theta):
        r = a * np.exp(b * theta)
        x = r * np.cos(theta + start_angle)
        y = r * np.sin(theta + start_angle)
        return np.array([x*0.5, y*0.5, 0])

    theta_max = 7 * PI
    golden_spiral = ParametricFunction(polar_to_cartesian, t_range=[start_angle, theta_max], color=WHITE, stroke_width=20)
    golden_spiral.shift(ORIGIN)
    return golden_spiral

def draw_sqrt_spiral(n):
    def calc_points(n):
        outer_points = [[1, 0, 0]]
        theta = 0
        for i in range(0,n):
            hyp_length = np.sqrt(2+i)
            theta += np.arcsin(1/hyp_length)
            outer_points.append([hyp_length * np.cos(theta),
                                 hyp_length * np.sin(theta), 0])

            debug.write("Triangle " + str(i) + "\n")
            debug.write("Hypotenuse length: " + str(hyp_length) + "\n")
            debug.write("Theta: " + str(theta) + "\n")
            debug.write("Points: " + str(outer_points) + "\n")

        return outer_points

    triangles = VGroup()
    points = calc_points(n)
    for i in range(0, len(points)-1):
        triangle = Polygon(points[i], points[i+1], [0,0,0], color=WHITE, stroke_width=5)
        triangles.add(triangle)


    return triangles




class DrawSqrtSpiral(MovingCameraScene):
    def construct(self):

        triangles = draw_sqrt_spiral(100)
        curr_max_width = 0
        curr_max_height = 0
        for i in range(0, len(triangles)):
            curr_max_width = np.max([curr_max_width, triangles[i].width + 10])
            curr_max_height = np.max([curr_max_height, triangles[i].height + 10])
            if (i < 15):
                animation_time = 1.0
            else:
                animation_time = 0.1
            self.play(self.camera.frame.animate.set(width=curr_max_width,
                                                    height=curr_max_height), run_time=animation_time)
            self.play(Create(triangles[i]), run_time=animation_time)



        self.wait(2)

class DrawSpirals(MovingCameraScene):
    def construct(self):
        squares, nums, arcs = draw_fib_squares()
        for i in range(0, len(squares)):
            curr_squares = VGroup(*squares[:i + 1])
            self.play(self.camera.frame.animate.set(width=np.max([10, curr_squares[i].width + 15]),
                                                    height=np.max([10, curr_squares[i].height + 15])))
            self.play(Create(squares[i]), Write(nums[i]), Create(arcs[i]))

        self.wait(2)
        self.play(self.camera.frame.animate.set(width=10, height=10))
        self.wait(2)

        # self.clear()

        plane, labels = draw_plane(squares)
        self.play(Create(plane), Write(labels))

        golden_spiral = draw_log_spiral()
        self.play(self.camera.frame.animate.set(width=plane.width + 5, height=plane.height))

        self.play(Create(golden_spiral), self.camera.frame.animate.set(width=golden_spiral.width+ 5, height=golden_spiral.height), run_time=20)

        self.wait(2)
