from Point import Point
from tools import *


class EllipticCurve:
    '''Clase que crea una curva elíptica usando un campo finito modulo p > 3'''

    # Punto al infinito siempre será None. Ignorar esta prueba unitaria
    inf_p = None

    def __init__(self, prime=3, a=1, b=1):
        '''Construimos la curva elíptica a partir de los parámetros a, b modulo p'''
        if not isPrime(prime):
            raise ValueError("No se proporcionó un número primo")

        if (4 * (a ** 3) + 27 * (b ** 2)) % prime == 0:
            raise ValueError("La curva elíptica no es válida para estos parámetros.")

        self.prime = prime

        self.a = a 
        self.b = b 

        self.points = []
        self.points.append(None)
        for x in range(self.prime):
            for y in range(self.prime):
                point = Point(x, y)
                if self.isInCurve(point):
                    self.points.append(point)

    def __str__(self):
        '''La curva debe ser representada como: y^2 = x^3 + ax + b mod p'''
        return f"y^2 = x^3 + {self.a}x + {self.b} mod {self.prime}"

    def isInCurve(self, point):
        '''Nos dice si un punto "point" pertenece a esta curva'''
        if point is None:
            return True
        
        if not isinstance(point, Point):
            return False

        left = point.y **2 % self.prime
        right = (point.x ** 3 + self.a * point.x + self.b) % self.prime
        return left == right

    def get_points(self):
        '''Nos da todos los puntos que pertenecen a la curva elíptica'''
        return self.points
        

    def sum(self, p, q):
        '''Suma p + q  regresando un nuevo punto modulo prime
        como está definido en las curvas elípticas. Recuerda que el punto al
        infinito funciona como neutro aditivo'''
        # Casos con el punto al infinito
        if p is None:
            return q
        if q is None:
            return p        

        if p == q:  #Si son el mismo punto
            if p.y == 0: 
                return None
            m = ((3 * p.x ** 2 + self.a) * inv_mult((2 * p.y), self.prime)) % self.prime
        elif p.x == q.x and p.y == inv_add(q.y, self.prime): # Si tienen la misma x pero el inverso de y
            return None #Punto al infinito
        elif p.x == q.x: #Si tienen la misma x pero diferente y
            return None
        else:  #Si son puntos diferentes
            m = ((q.y - p.y) * inv_mult(q.x - p.x, self.prime)) % self.prime

        #Coordenadas del punto resultante
        x = (m * m - p.x - q.x) % self.prime
        y = (m * (p.x - x) - p.y) % self.prime

        return Point(x, y)

    def mult(self, k, p):
        '''Suma  k veces el punto p (o k(P)).
        Si k < 0 entonces se suma el inverso de P k veces'''
        if not self.isInCurve(p):
            raise ValueError("El punto no está en la curva")
        if k < 0:
            return self.mult(-k, self.inv(p))
        
        if k == 0:
            return None

        result = None  # Empezamos con el punto al infinito
        sum_ = p
        while k > 0:
            if k % 2 == 1:
                result = self.sum(result, sum_)
            sum_ = self.sum(sum_, sum_)
            k = k // 2
        return result

    def order(self, p):
        '''Dado el punto p que pertenece a la curva elíptica, nos regresa el mínimo entero k
        tal que  k(P) = punto al infinito.'''
        if not self.isInCurve(p):
            raise ValueError("El punto no pertenece a la curva")

        k = 1
        acc= p
        while acc is not None and k <= len(self.points):
            acc = self.sum(acc, p)
            k += 1
        return k

    def cofactor(self, p):
        '''Dado el punto p de la curva, regresa el total de puntos de la curva entre el orden
        de ese punto'''
        if not self.isInCurve(p):
            raise ValueError("El punto debe pertenecer a la curva")
        return len(self.points) / self.order(p)

    def inv(self, p):
        '''Regresa el inverso aditivo de este punto. Recuerda que es el mismo punto reflejado
        en el eje x'''
        if p is None:  #inf_p inverso es inf_p
            return None
        
        if not self.isInCurve(p):
            raise ValueError("El punto no pertenece a la curva")

        return Point(p.x, inv_add(p.y, self.prime))
    

if __name__ == "__main__":
    curve = EllipticCurve(23, 1, 17)
    # print(curve)
    points = curve.get_points()
    #print(points)

    assign = table(curve, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
    print(assign)



