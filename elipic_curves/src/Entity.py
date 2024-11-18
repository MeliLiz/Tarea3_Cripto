import random as r
from EllipticCurve import EllipticCurve
from tools import table
from Point import Point

class Entity:
    '''Clase que modela una entidad como Alice o Bob.'''

    def __init__(self, name, curve, generator_point, table):
        '''Construye un nuevo personaje con un mensaje para compartir
        Una entidad tiene:
        1. name: Nombre de la entidad
        2. curve: Una curva elíptica a compartir
        3. generator_point: Un punto generador a compartir
        4. table: Una codificacion de caracteres a puntos de la curva.

        Además, debe inicializar sus llaves, públicas y privadas:
        5. private_key: Un entero aleatorio entre 1 y el orden del punto generador-1
        6. private_point: Un punto aleatorio de la curva que no sea el punto al infinito
        ## 3 llaves públicas de esta entidad
        7. public_key_1, public_key_2, public_key_3 = None
        ## 3 llaves públicas de la otra entidad
        8. another_entity_public_key_1, another_entity_public_key_2, another_entity_public_key_3 = None'''
        self.name = name
        self.curve = curve
        self.generator_point = generator_point
        self.order = self.curve.order(generator_point)
        ## Cosas privadas
        self.private_key = r.randint(1, self.order - 1)
        # Cosas publicas
        self.public_key_1 = None #Public key using private point
        self.public_key_2 = None #Public key using only private key
        self.public_key_3 = None

        #Public keys from another entity
        self.another_entity_public_key_1 = None
        self.another_entity_public_key_2 = None
        self.another_entity_public_key_3 = None

        self.table = table

        while True:
            points = self.curve.points[1:]
            self.private_point = r.choice(points)
            if self.curve.sum(generator_point, self.private_point) is not None:
                break

    def set_private(self, private):
        self.private_key = private

    def descifrar(self, ciphered_msg):
        '''Descifra un conjunto de parejas de puntos (e1, e2) de una curva elíptica a un texto
        plano legible humanamente'''
        if not ciphered_msg:
            return ''
        
        message = ''
        for e1_encrypted, e2_encrypted in ciphered_msg:
            try:
                e1 = self.table[e1_encrypted]
                e2 = self.table[e2_encrypted]
                private_mult_e1 = self.curve.mult(self.private_key, e1)
                private_mult_anEnt_1 = self.curve.mult(self.private_key, self.another_entity_public_key_1)
                inv = self.curve.sum(private_mult_e1, private_mult_anEnt_1)
                inv = self.curve.sum(inv,self.another_entity_public_key_3)
                inv = self.curve.inv(inv)
                
                P = self.curve.sum(e2, inv)

                found_char = None
                for k, v in self.table.items():
                     if v == P:
                         message += k
                         found_char = True
                         break
                if not found_char:
                    message += list(self.table.keys())[0]
            except Exception as e:
                message += list(self.table.keys())[0]
                continue
        return message



    def cifrar(self, message):
        print("Message to encrypt: ", message)  
        '''Cifra el mensaje (self.message) a puntos de la curva elíptica. Cada caracter es 
        mapeado a una pareja de puntos (e1, e2) con e1, e2 en EC.'''
        # Se usa un random para cada símbolo
        # print(f'{self.name} cifra el mensaje "{self.message}" como: ')
        if not message:
            return []
        cipher = []

        for char in message:
            if char not in self.table:
                continue

            M = self.table[char]
            r_val = r.randint(1, self.order - 1)
            e1 = self.curve.mult(r_val, self.generator_point)

            beta_plus_r_mult_anEnt_1 = self.curve.mult(self.private_key + r_val, self.another_entity_public_key_1)
            inv_r_mult_another_entity_public_key_1 = self.curve.mult(r_val, self.another_entity_public_key_2)
            inv_r_mult_another_entity_public_key_1 = self.curve.inv(inv_r_mult_another_entity_public_key_1)       
            e2 = self.curve.sum(M, beta_plus_r_mult_anEnt_1)
            e2 = self.curve.sum(e2, inv_r_mult_another_entity_public_key_1)
            e2 = self.curve.sum(e2, self.another_entity_public_key_3)

            e1_encrypted = None
            e2_encrypted = None
            for k, v in self.table.items():
                if v == e1:
                    e1_encrypted = k
                elif v == e2:
                    e2_encrypted = k
                elif e1_encrypted and e2_encrypted:
                    break

            if e1_encrypted is not None and e2_encrypted is not None:
                cipher.append((e1_encrypted, e2_encrypted))
            else:
                
                #print("Error: No se encontró el punto en la tabla, se usará el primer carcater")
                char = list(self.table.keys())[0]
                cipher.append((char, char))
        return cipher
    

    def genera_llaves_publicas(self):
        '''Hace las operaciones correspondientes para generar la primera ronda de llaves
        públicas de esta entidad PK1 y PK2.'''
        sum_point = self.curve.sum(self.generator_point, self.private_point)
        self.public_key_1 = self.curve.mult(self.private_key, sum_point)
        self.public_key_2 = self.curve.mult(self.private_key, self.private_point)
        if self.public_key_1 is None or self.public_key_2 is None:
            raise ValueError("Error al generar llaves públicas")
        return [self.public_key_1, self.public_key_2]

    def recibe_llaves_publicas(self, public_keys):
        '''Recibe la llave publica de otra entidad y las guarda. (primera ronda solo guarda 2)
        o si ya es la segunda ronda, guarda la última llave (pk1, pk2 y pk3 != None)'''
        # print(public_keys) puede ser que alguna llave sea None, pero lo evitaremos por
        # motivos didácticos, pero no pasa nada, sigue funcionando
        print("Public keys recieved: ", public_keys)
        if len(public_keys) == 2:  # Primera ronda
            self.another_entity_public_key_1 = public_keys[0]
            self.another_entity_public_key_2 = public_keys[1]
        else:  # Segunda ronda
            self.another_entity_public_key_3 = public_keys[2]
            print("Public key 2: ", self.another_entity_public_key_2)
            # print(f'{self.name} recibe las llaves públicas de otra entidad y son: {public_keys}')

    def final_keys(self):
        '''Genera la última llave pública, en combinación con otra llave pública de otra entidad
        Regresa las 3 llaves públicas de esta entidad.'''
        self.public_key_3 = self.curve.mult(
            self.private_key,
            self.another_entity_public_key_2
        )
        return (self.public_key_1, self.public_key_2, self.public_key_3)

    def __str__(self):
        return (
            f"{self.name}:\n"
            f"EC: {self.curve}\n"
            f"G: {self.generator_point}\n"
            f"Private Key: {self.private_key}\n"
            f"Private Point: {self.private_point}\n"
        )
    
def cifrar1():
    msg = 'quiero vacaciones'
    curve = EllipticCurve(23, 1, 17)
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 
                't', 'u', 'v', 'w', 'x', 'y', 'z']
    tabl = table(curve, alphabet)
    #print(tabl)
    generator = Point(2,2)
    a = Entity('Alice', curve, generator, tabl)
    b = Entity('Bob', curve, generator, tabl)

    b.recibe_llaves_publicas(a.genera_llaves_publicas())
    a.recibe_llaves_publicas(b.genera_llaves_publicas())

    b.recibe_llaves_publicas(a.final_keys())
    a.recibe_llaves_publicas(b.final_keys())

    msg_cipher = a.cifrar(msg)
    print("Mensaje cifrado: ", msg_cipher)

    dec_msg = b.descifrar(msg_cipher)
    print("Mensaje descifrado: ", dec_msg)

def cifrar2():
    msg = 'lunes'
    curve = EllipticCurve(23, 1, 17)
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 
                't', 'u', 'v', 'w', 'x', 'y', 'z']
    tabl = table(curve, alphabet)
    #print(tabl)
    generator = Point(2,2)
    a = Entity('Alice', curve, generator, tabl)
    a.set_private(5)
    b = Entity('Bob', curve, generator, tabl)
    b.set_private(7)

    pub1 = curve.mult(5, generator) #Alice
    pub2 = curve.mult(7, generator) #Bob

    gen = curve.mult(5, pub2) #Alice
    gen1 = curve.mult(7, pub1) #Bob

    print(pub1)
    print(pub2)
    print(gen)
    print(gen1)

    """b.recibe_llaves_publicas(a.genera_llaves_publicas())
    a.recibe_llaves_publicas(b.genera_llaves_publicas())

    b.recibe_llaves_publicas(a.final_keys())
    a.recibe_llaves_publicas(b.final_keys())

    msg_cipher = a.cifrar(msg)
    print("Mensaje cifrado: ", msg_cipher)

    dec_msg = b.descifrar(msg_cipher)
    print("Mensaje descifrado: ", dec_msg)"""


if __name__ == '__main__':
    cifrar1()
   #cifrar2()

                