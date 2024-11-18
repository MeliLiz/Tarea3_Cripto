class Point:
    '''Clase que representa un punto en un plano 2D'''

    #Punto al infinito
    infinite_point = None

    def __init__(self, x = 0, y = 0):
        '''Constructor: Construye un punto en un plano 2D con coordenadas (x,y)'''
        self.x = x
        self.y = y

    def __str__(self):
        '''Representación en cadena. Usamos str(p)'''
        cadena = '({}, {})'.format(self.x, self.y)
        return cadena

    def __repr__(self):
        '''Representación en cadena x2. Usamos print(p)'''
        cadena = '({}, {})'.format(self.x, self.y)
        return cadena

    def __eq__(self, another_point):
        '''Comparación entre 2 puntos. Usamos ==
        another_point debe ser instancia de Point'''
        if not isinstance(another_point, Point):
            return False
        return self.x == another_point.x and self.y == another_point.y

    def set(self, x, y):
        '''Reescribe los valores de x y y a este punto.
        @raise ValueError si x o y no son números enteros'''
        # if not isinstance(x, int) or not isinstance(y, int):
        #     raise ValueError('x y y deben ser int')
        if isinstance(x, int) and isinstance(y, int):
            self.x = x
            self.y = y

