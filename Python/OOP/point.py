import unittest

class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        if not isinstance(x, (float, int)) or not isinstance(y, (float, int)):
            raise TypeError(
                f"x and y must be of type float or int, got x={type(x)} and y={type(y)}"
            )
        self.x = float(x)
        self.y = float(y)

    def distance_from_origin(self):
        return round((self.x**2 + self.y**2) ** 0.5, 3)


if __name__ == "__main__":
    class PointTestCase(unittest.TestCase):
        def test_distance_from_origin(self):
            # Test case 1: Point at (3, 4)
            p1 = Point(3, 4)
            self.assertEqual(p1.distance_from_origin(), 5.0)

            # Test case 2: Point at (-2, -2)
            p2 = Point(-2, -2)
            self.assertEqual(p2.distance_from_origin(), 2.828)

        def test_default_point(self):
            # Test case 3: Default point at (0, 0)
            p3 = Point()
            self.assertEqual(p3.distance_from_origin(), 0.0)

        def test_error_throwing(self):
            # Test case 4: Invalid input type
            with self.assertRaises(TypeError):
                Point("a", 2)
    
    unittest.main()