import math

def calculate_circle_area(radius: float) -> float:
    return round(math.pi * radius ** 2, 4)


def calculate_rectangle_area(length: float, width: float) -> float:
    return round(length * width, 4)

def calculate_triangle_area(base: float, height: float) -> float:
    return round(0.5 * base * height, 4)