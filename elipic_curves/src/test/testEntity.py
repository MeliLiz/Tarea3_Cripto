import unittest
from EllipticCurve import EllipticCurve
from Entity import Entity
from Point import Point
from tools import *

class TestEntity(unittest.TestCase):
    '''Curva elíptica a probar: EC_37(2, 9)'''
    e = EllipticCurve(37, 2, 9)
    # Punto generador
    c = Point(9, 4)
    # Mapeo de caracteres
    t = table(e)


    def test_init(self):
        a = Entity('Alice', self.e, self.c, self.t)

        self.assertTrue(a.name != None)
        # Debería impolementar el método __eq__
        self.assertTrue(a.curve != None)
        self.assertTrue(a.generator_point == self.c)
        self.assertTrue(a.table != None)

        # Private Key
        self.assertTrue(a.private_key in [x for x in range(1, a.curve.order(self.c))])
        # Private Point
        self.assertTrue(a.private_point != None)
        self.assertTrue(a.private_point in self.e.points)
        inv = a.curve.inv(self.c)
        self.assertTrue(self.e.sum(a.private_point, inv) != None)


        # Public owner keys
        self.assertTrue(a.public_key_1 is None)
        self.assertTrue(a.public_key_2 is None)
        self.assertTrue(a.public_key_3 is None)

        # Public keys from another entity
        self.assertTrue(a.another_entity_public_key_1 is None)
        self.assertTrue(a.another_entity_public_key_2 is None)
        self.assertTrue(a.another_entity_public_key_3 is None)

        self.assertTrue(a.table is not None)

    def test_str(self):
        a = Entity('Alice', self.e, self.c, self.t)
        s = f'''{a.name}:
EC: {a.curve}
G: {a.generator_point}
Private Key: {a.private_key}
Private Point: {a.private_point}
'''
        self.assertTrue(str(a) == s)

    def test_genera_llaves_publicas(self):
        # print('\n--------------- TEST GENERA LLAVES -------------')'
        a = Entity('Alice', self.e, self.c, self.t)

        # alpha = a.private_key
        # C = (9, 4)
        # PrivatePoint = A = a.private_point
        # A1 = alpha(C + A)
        # A2 = alpha(C)
        a1_a2 = a.genera_llaves_publicas()
        self.assertTrue(a.public_key_1 is not None)
        self.assertTrue(a.public_key_2 is not None)

        for x in a1_a2:
            self.assertIsNotNone(x)
            self.assertIsInstance(x, Point)
            self.assertTrue(x in self.e.points)

    def test_recibe_llaves_publicas(self):
        # print('\n--------------- TEST RECIBE LLAVES -------------')
        a = Entity('Alice', self.e, self.c, self.t)
        a1_a2 = a.genera_llaves_publicas()

        b = Entity('Bob', self.e, self.c, self.t)
        b1_b2 = b.genera_llaves_publicas()

        self.assertTrue(a.another_entity_public_key_1 is None)
        self.assertTrue(a.another_entity_public_key_2 is None)
        self.assertTrue(a.another_entity_public_key_3 is None)
        self.assertTrue(b.another_entity_public_key_1 is None)
        self.assertTrue(b.another_entity_public_key_2 is None)
        self.assertTrue(b.another_entity_public_key_3 is None)

        # Primera ronda, solo existen A1, A2, B1 y B2
        self.assertTrue(len(a1_a2 + b1_b2) == 4)

        a.recibe_llaves_publicas(b1_b2)
        b.recibe_llaves_publicas(a1_a2)

        # Solo asignamos
        self.assertTrue(a.another_entity_public_key_1 is not None)
        self.assertTrue(a.another_entity_public_key_2 is not None)
        self.assertTrue(a.another_entity_public_key_3 is None)
        self.assertTrue(b.another_entity_public_key_1 is not None)
        self.assertTrue(b.another_entity_public_key_2 is not None)
        self.assertTrue(b.another_entity_public_key_3 is None)

        # Esto supone que la prueba final_keys() está bien
        a1_a2_a3 = a.final_keys()
        b1_b2_b3 = b.final_keys()
        # Segunda ronda, deben existir todos
        b.recibe_llaves_publicas(a1_a2_a3)
        a.recibe_llaves_publicas(b1_b2_b3)

        self.assertTrue(a.another_entity_public_key_1 is not None)
        self.assertTrue(a.another_entity_public_key_2 is not None)
        self.assertTrue(a.another_entity_public_key_3 is not None)
        self.assertTrue(b.another_entity_public_key_1 is not None)
        self.assertTrue(b.another_entity_public_key_2 is not None)
        self.assertTrue(b.another_entity_public_key_3 is not None)

    def test_final_keys(self):
        # print('\n--------------- TEST FINAL LLAVES -------------')
        a = Entity('Alice', self.e, self.c, self.t)
        a1_a2 = a.genera_llaves_publicas()

        b = Entity('Bob', self.e, self.c, self.t)
        b1_b2 = b.genera_llaves_publicas()

        a.recibe_llaves_publicas(b1_b2)
        b.recibe_llaves_publicas(a1_a2)

        # Solo asignamos
        self.assertTrue(a.public_key_1 is not None)
        self.assertTrue(a.public_key_2 is not None)
        self.assertTrue(a.public_key_3 is None)
        self.assertTrue(b.public_key_1 is not None)
        self.assertTrue(b.public_key_2 is not None)
        self.assertTrue(b.public_key_3 is None)

        # Esto supone que la prueba final_keys() está bien
        a1_a2_a3 = a.final_keys()
        b1_b2_b3 = b.final_keys()
        b.recibe_llaves_publicas(a1_a2_a3)
        a.recibe_llaves_publicas(b1_b2_b3)

        for x in a1_a2_a3 + b1_b2_b3:
            self.assertIsNotNone(x)
            self.assertIsInstance(x, Point)
            self.assertTrue(x in self.e.points)


        self.assertTrue(a.public_key_1 is not None)
        self.assertTrue(a.public_key_2 is not None)
        self.assertTrue(a.public_key_3 is not None)
        self.assertTrue(b.public_key_1 is not None)
        self.assertTrue(b.public_key_2 is not None)
        self.assertTrue(b.public_key_3 is not None)

    def cifrar(self):
        msg = 'quiero vacaciones'
        curve = EllipticCurve(23, 1, 17)
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        tabl = table(curve, alphabet)
        generator = Point(2,2)
        a = Entity('Alice', curve, generator, tabl)
        b = Entity('Bob', curve, generator, tabl)

        b.recibe_llaves_publicas(a.genera_llaves_publicas())
        a.recibe_llaves_publicas(b.genera_llaves_publicas())

        b.recibe_llaves_publicas(a.final_keys())

        msg_cipher = a.cifrar(msg)

        print(msg_cipher)



    def test_cifrar_descifrar(self):
        # print('\n--------------- TEST CIFRAR/DESCIFRAR -------------')
        # Puras minúsculas por lo mientras
        msg = 'el semestre se pondra de color de hormiga'
        # minusculas, mayusculas, espacio
        alphabet = [' '] + [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)]

        tabl = table(self.e, alphabet)
        a = Entity('Alice', self.e, self.c, tabl)
        b = Entity('Bob', self.e, self.c, tabl)

        b.recibe_llaves_publicas(a.genera_llaves_publicas())
        a.recibe_llaves_publicas(b.genera_llaves_publicas())

        b.recibe_llaves_publicas(a.final_keys())
        a.recibe_llaves_publicas(b.final_keys())

        msg_cipher = a.cifrar(msg)

        self.assertTrue(len(msg_cipher) == len(msg))
        for p in msg_cipher:
            self.assertTrue(p is not None)
            self.assertTrue(p[0] in alphabet)
            self.assertTrue(p[1] in alphabet)
            self.assertTrue(tabl[p[0]] in self.e.points)
            self.assertTrue(tabl[p[1]] in self.e.points)

        # Donde la puerca tuerce el rabo. Solo hay una respuesta correcta
        dec_msg = b.descifrar(msg_cipher)
        self.assertTrue(msg == dec_msg)


if __name__ == '__main__':
    # unittest.main()
    test = TestEntity()
    test.cifrar()
