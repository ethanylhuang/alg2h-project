from manim import *
import numpy as np

def fade_out(scene):
    animations = []
    for mobject in scene.mobjects:
        animations.append(FadeOut(mobject))
    scene.play(*animations)

class DrawAxes(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-10, 10],
            y_range=[-10, 10],
            axis_config={"color": WHITE},
        )
        self.play(Create(axes))

class ShowFib(Scene):
    def construct(self):
        fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        text = Text("Fibonacci Numbers: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...")
        self.play(Write(text))
        fade_out(self)
        boxes = []
        dir = [DOWN, RIGHT, UP, LEFT]
        for i in range (0, 4):
            curr = fib[i]
            text = Text(str(curr))
            square = Square(side_length=curr) 
            
            if (i > 0):
                square.next_to(boxes[i-i], dir[(i-1)%4], buff=0)
                if (i >= 2):
                    square.shift(dir[(i-2)%4] * boxes[i-1].get_height() / 2)

            
            text.move_to(square.get_center())
            boxes.append(square)
            self.play(Write(text), Create(square))
        
        self.wait(2)


class Main(Scene):
    def construct(self):
        ShowFib.construct(self)