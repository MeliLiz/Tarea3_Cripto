import unittest
from Point import Point

class TestPoint(unittest.TestCase):

    def test_init(self):
        x = 20.0
        y = -10.0
        p = Point()
        ## Por omisión, debe crear al punto (0, 0)
        self.assertTrue(p.x == 0)
        self.assertTrue(p.y == 0)

        p = Point(x,y)
        self.assertTrue(p.x == x)
        self.assertTrue(p.y == y)

    def test_str(self):
        p = Point()
        self.assertTrue(str(p) == '(0, 0)')
        x = 4
        y = -1
        p = Point(x, y)
        s = str(p)
        self.assertTrue(s[0] == '(')
        self.assertTrue(s[-1] == ')')
        s = s[1:-1] # '4, -1'
        s = s.split(' ')
        self.assertTrue(len(s) == 2)
        x_coord = s[0]
        y_coord = s[1]
        self.assertTrue(x_coord[-1] == ',')
        try:
            a = float(x_coord[:-1])
            b = float(y_coord)
            self.assertTrue(a == x)
            self.assertTrue(b == y)
        except ValueError:
            self.assertFail(f'{x_coord}, {y_coord}')

    def test_repr(self):
        ## Misma representación
        self.test_str()

    def test_eq(self):
        ## Igualdad de puntos
        p1 = None
        p2 = None
        self.assertTrue(p1 == p2)
        p1 = Point()
        self.assertFalse(p1 == p2)
        self.assertFalse(p1 == 'a')
        p2 = Point()
        self.assertIsInstance(p2, Point)
        self.assertTrue(p1 == p2)
        p2.set(1, -1)
        self.assertFalse(p1 == p2)
        p1.set(1, -1)
        self.assertTrue(p1 == p2)

    def test_set(self):
        p = Point()
        x = 1
        y = -1
        self.assertTrue(p.x == 0)
        self.assertTrue(p.y == 0)
        p.set(x, y)

        self.assertTrue(p.x == x)
        self.assertTrue(p.y == y)
        p.set('a', 'b')
        self.assertTrue(p.x == x)
        self.assertTrue(p.y == y)

    def test_infinite_point(self):
        self.assertIsNone(Point.infinite_point)

if __name__ == '__main__':
    unittest.main()
