import unittest
from EllipticCurve import EllipticCurve
from Point import Point

class TestEllipticCurve(unittest.TestCase):
    '''Curvas elípticas a probar: EC_17(2, 2), EC_37(2, 9) y EC_233(-2, 8)'''

    e0 = EllipticCurve()
    e1 = EllipticCurve(prime = 17, a = 2, b = 2)
    e2 = EllipticCurve(37, 2, 9)
    e3 = EllipticCurve(233, -2, 8)

    def test_init(self):
        e = self.e0

        ## Por omisión, crear la curva elíptica más sencilla EC_3(1, 1)
        self.assertTrue(e.prime == 3)
        self.assertTrue(e.a == 1)
        self.assertTrue(e.b == 1)

        #Otras pruebas de curvas
        self.assertTrue((4*e.a**3 + 27*e.b**2) != 0)
        e = self.e1
        self.assertTrue((4*e.a**3 + 27*e.b**2) != 0)
        e = self.e2
        self.assertTrue((4*e.a**3 + 27*e.b**2) != 0)
        e = self.e3
        self.assertTrue((4*e.a**3 + 27*e.b**2) != 0)

        self.assertIsNotNone(e.points)
        self.assertTrue(len(e.points) > 0)

    def test_str(self):
        s = 'y^2 = x^3 + {0}x + {1} mod {2}'
        e = self.e3

        self.assertTrue(str(e) == s.format(-2, 8, 233))

    def test_points(self):
        e = self.e0

        self.assertTrue(None in e.points)
        self.assertTrue(len(e.points) == 4)
        f = [None, (0, 1), (0, 2), (1, 0)]
        for p in e.points:
            if p:
                s = (p.x, p.y)
                self.assertTrue(s in f)

        e = self.e1

        # Puntos a probar
        f = [None, (0, 6), (0, 11), (3, 1), (3, 16), (5, 1), (5, 16), (6, 3), (6, 14), (7, 6), (7, 11), (9, 1), (9, 16), (10, 6), (10, 11), (13, 7), (13, 10), (16, 4), (16, 13)]
        self.assertTrue(len(e.points) == len(f))
        for p in e.points:
            if p:
                s = (p.x, p.y)
                self.assertTrue(s in f)

        self.assertTrue(e.points == e.get_points())

        e = self.e3
        self.assertTrue(Point(188, 141) in e.points)
        self.assertTrue(Point(232, 230) in e.points)
        self.assertFalse(Point(232, 231) in e.points)
        self.assertFalse(Point(0, 5) in e.points)
        self.assertTrue(len(e.points) == 216)

    def test_is_in_curve(self):
        e = self.e0
        self.assertTrue(e.isInCurve(None))

        p = (0, 1)
        # Deben ser instancia de Point
        self.assertFalse(e.isInCurve(p))
        self.assertTrue(e.isInCurve(Point(0, 1)))
        self.assertTrue(e.isInCurve(Point(0, 2)))
        self.assertTrue(e.isInCurve(Point(1, 0)))
        self.assertFalse(e.isInCurve(Point(1, 1)))

        # Puntos a probar
        f1 = [None, (0, 6), (0, 11), (3, 1), (3, 16), (5, 1), (5, 16), (6, 3), (6, 14), (7, 6), (7, 11), (9, 1), (9, 16), (10, 6), (10, 11), (13, 7), (13, 10), (16, 4), (16, 13)]
        f2 = [None] + [(x, y) for x in range(0, 17) for y in range(0, 17)]
        e = self.e1
        for p in f2:
            if not p in f1:
                self.assertFalse(e.isInCurve(Point(p[0], p[1])))

    def test_sum(self):
        p = None
        q = None
        ## Casos especiales con puntos
        e = self.e0
        self.assertTrue(e.isInCurve(p))
        self.assertTrue(e.isInCurve(q))
        self.assertTrue(e.sum(p, q) == None)

        p = Point(0, 1)
        self.assertTrue(e.isInCurve(p))
        # La suma es comutativa con el neutro aditivo
        self.assertTrue(e.sum(p, q) == p)
        self.assertTrue(e.sum(q, p) == p)

        q = Point(0, 2)
        # El inverso aditivo. Es la recta paralela al eje y
        self.assertTrue(e.sum(p, q) == None)
        self.assertTrue(e.sum(q, p) == None)
        # El punto que corta la curva en X
        p = Point(1, 0)
        self.assertTrue(e.isInCurve(p))
        self.assertTrue(e.sum(p, p) == None)

        # Sumar en sí
        e = self.e1
        f = [(5,1), (6, 3), (10, 6), (3, 1), (9, 16), (16, 13), (0, 6), (13, 7), (7, 6), (7, 11), (13, 10), (0, 11), (16, 4), (9, 1), (3, 16), (10, 11), (6, 14), (5, 16), None]

        p = Point(5, 1) #f[0] = (5, 1) = Punto generador
        for i in range(len(f) -1):
            t0 = f[i]
            t1 = f[i+1]
            q = Point(t0[0], t0[1])
            if t1:
                self.assertTrue(e.sum(p, q) == Point(t1[0], t1[1]))
            else:
                self.assertTrue(e.sum(p, q) == None)

    def test_mult(self):
        e = self.e1
        p = None

        self.assertTrue(e.isInCurve(p))
        self.assertTrue(e.mult(-1, p) is None)
        self.assertTrue(e.mult(2**64, p) is None)

        # k < 0, entonces es sumar el inverso del punto P k veces

        f = [(5,1), (6, 3), (10, 6), (3, 1), (9, 16), (16, 13), (0, 6), (13, 7), (7, 6), (7, 11), (13, 10), (0, 11), (16, 4), (9, 1), (3, 16), (10, 11), (6, 14), (5, 16)]

        p = Point(5, 1) #f[0] = (5, 1) = Punto generador
        q = Point(5, 16)
        r = e.inv(p)
        self.assertTrue(e.sum(p, q) is None)
        self.assertTrue(r == q)
        self.assertTrue(e.mult(-1, p) == r)

        for i in range(len(f)):
            pos = f[i]
            pos = Point(pos[0], pos[1])
            neg = f[-i-1]
            neg = Point(neg[0], neg[1])

            self.assertTrue(e.mult(i+1, p) == pos)  # 1*(5,1) = (5,1)
            self.assertTrue(e.mult(i+1, q) == neg)  # -1*(5,1) = 1*(5, 16)
            self.assertTrue(e.mult(-i-1, p) == neg) # -1*(5,1)
            self.assertTrue(e.mult(-i-1, q) == pos) # -1*(5, 16) == 1*(5, 16)

        # Casualmente el número de puntos es la multiplicacion máxima con cualquier punto
        eli = [self.e0, self.e1, self.e2, self.e3]
        # 4, 19, 43, 216 
        for e in eli:
            self.assertTrue(e.mult(len(e.points), e.points[-1]) == None)


    def test_order(self):
        # Casualmente el número de puntos es la multiplicacion máxima con cualquier punto
        eli = [self.e0, self.e1, self.e2, self.e3]
        order = [2, 19, 43, 216]

        for i in range(len(eli)):
            try:
                # Lanzar exception si no se encuentra el punto de partida
                eli[i].order(Point(0,0))
                self.assertFail()
            except:
                pass
            self.assertTrue(eli[i].order(eli[i].points[-1]) == order[i])

        # Hay 3 ciclos en esta curva
        e = EllipticCurve(31, 2, 1)
        self.assertTrue(e.order(e.points[-1]) == 8)

    def test_cofactor(self):
        eli = [self.e1, self.e2, self.e3]
        for e in eli:
            try:
                # Lanzar exception si no se encuentra el punto de partida
                eli[i].cofactor(Point(0,0))
                self.assertFail()
            except:
                pass
            self.assertTrue(e.cofactor(e.points[-1]) == 1)

        # Hay 2 ciclos en e0
        e = self.e0
        self.assertFalse(e.cofactor(Point(1, 0)) == 1)
        self.assertTrue(e.cofactor(Point(1, 0)) > 1)

        # Hay 3 ciclos en e
        e = EllipticCurve(31, 2, 1)
        self.assertTrue(e.cofactor(e.points[-1]) == 3)

    def test_inv(self):
        e = self.e1
        p = None
        self.assertTrue(e.inv(p) == None)

        p = Point(0,0)
        try:
            # P debe estar dentro de e
            e.inv(p)
            self.assertFail()
        except:
            pass

        f = e.points
        for p in f:
            if p:
                inv = e.inv(p)
                self.assertTrue(inv.x == p.x)
                self.assertTrue(e.sum(inv, p) == None)
                self.assertTrue(e.sum(p, inv) == None)
                if inv.y == p.y:
                    self.assertTrue(p == inv)

if __name__ == '__main__':
    unittest.main()

