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
    hyp_angles = []
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
            hyp_angles.append(theta)

        return outer_points

    triangles = VGroup()
    sqrt_spiral = VGroup()
    inner_lines1 = VGroup()
    inner_lines2 = VGroup()
    hyp_labels = VGroup()
    leg_labels = VGroup()
    points = calc_points(n)

    debug.write("Hyp Angles: " + str(hyp_angles) + "\n")
    for i in range(0, len(points)-1):

        inner_lines1.add(Line(points[i], [0,0,0], color=WHITE, stroke_width=5))
        inner_lines2.add(Line(points[i+1], [0,0,0], color=WHITE, stroke_width=5))
        sqrt_spiral.add(Line(points[i], points[i+1], color=WHITE, stroke_width=5))
        triangles.add(Polygon(points[i], points[i+1], [0,0,0], color=WHITE, stroke_width=5))
        #hyp_label = MathTex(r"\sqrt{" + str(2+i) + "}").move_to(Line([0, 0, 0], points[i+1]).get_center())
        #yp_label.scale(0.7)
        #leg_label = MathTex("1").move_to(Line(points[i+1], points[i]).get_center())
        #leg_label.scale(0.7)
        #leg_label.shift(hyp_angles[i] * 0.2)
        #hyp_labels.add(hyp_label)
        #leg_labels.add(leg_label)

    return triangles, sqrt_spiral, inner_lines1, inner_lines2, hyp_labels, leg_labels

def draw_arch_spiral():
    a = 1
    b = 1
    start_angle = 1

    def polar_to_cartesian(theta):
        r = a * (theta+start_angle)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return np.array([x*0.525, y*0.525, 0])

    theta_max = 15 * PI
    arch_spiral = ParametricFunction(polar_to_cartesian,
                                     t_range=[0, theta_max],
                                     color=BLUE,
                                     stroke_width=20)
    arch_spiral.shift(ORIGIN)
    return arch_spiral

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
        self.play(DrawBorderThenFill(plane), Write(labels))

        golden_spiral = draw_log_spiral()
        self.play(self.camera.frame.animate.set(width=plane.width + 5, height=plane.height))

        self.play(Create(golden_spiral), self.camera.frame.animate.set(width=golden_spiral.width+ 5, height=golden_spiral.height), run_time=15)

        self.wait(1)

        self.play(FadeOut(golden_spiral), FadeOut(labels), FadeOut(arcs), FadeOut(squares), FadeOut(plane))
        self.clear()

        triangles, sqrt_spiral, inner_lines1, inner_lines2, hyp_labels, leg_labels = draw_sqrt_spiral(300)
        curr_max_width = 0
        curr_max_height = 0
        for i in range(0, 15):
            curr_max_width = np.max([curr_max_width, sqrt_spiral[i].width + 10])
            curr_max_height = np.max([curr_max_height, sqrt_spiral[i].height + 10])
            self.play(self.camera.frame.animate.set(width=curr_max_width, height=curr_max_height), run_time=0.4)
            self.play(Create(sqrt_spiral[i]), Create(inner_lines1[i]), Create(inner_lines2[i]), run_time=0.4)

        self.play(Create(sqrt_spiral[15:]), Create(inner_lines1[15:]), Create(inner_lines2[15:]),
                  self.camera.frame.animate.set(width=sqrt_spiral.width + 5, height=sqrt_spiral.height + 5),
                  run_time=15)

        self.play(FadeOut(inner_lines1), FadeOut(inner_lines2))
        self.wait(2)

        self.play(self.camera.frame.animate.set(width=10, height=10))
        plane, labels = draw_plane(triangles)
        self.play(DrawBorderThenFill(plane), Write(labels))
        arch_spiral = draw_arch_spiral()
        self.play(Create(arch_spiral),
                  self.camera.frame.animate.set(width=arch_spiral.width + 5, height=arch_spiral.height + 5),
                  run_time=15)

        self.wait(2)
