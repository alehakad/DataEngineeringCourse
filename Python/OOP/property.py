class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = value

    @property
    def area(self):
        return self.width * self.height
    
if __name__ == "__main__":
    r = Rectangle(2, 3)
    print(r.width, r.height, r.area)
    try:
        r.height = -1
    except ValueError as e:
        print(e)
    r.width = 4
    print(r.area)
        