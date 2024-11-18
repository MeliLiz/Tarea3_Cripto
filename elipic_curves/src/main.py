from EllipticCurve import EllipticCurve
from Entity import Entity
from tools import table
from Point import Point
import sys

# Crear el alfabeto ASCII de 256 caracteres
ascii_alphabet = ''.join(map(chr, range(256)))

# Curva que soporta 256 caracteres
eli = EllipticCurve(233, -2, 8)
g = eli.points[-1]

# Usar el alfabeto ASCII para la tabla de mapeo
code = table(eli, ascii_alphabet)

print("CREACIÓN DE ENTIDADES CON CURVAS\n\n")
a = Entity("Allice", eli, g, code)
b = Entity("Bob", eli, g, code)

# Mensaje específico a cifrar
msg = "Perro salchicha, gordo bachicha"

print(a)
print(b)
print(f"\nMensaje a cifrar: {msg}\n")

print("INTERCAMBIO DE LLAVES TIPO DIFFIE-HELLMAN")
pub_k_a = a.genera_llaves_publicas()
pub_k_b = b.genera_llaves_publicas()

print('Ronda 1: ')
print(f'{a.name} PKs: {pub_k_a}')
print(f'{b.name} PKs: {pub_k_b}')

a.recibe_llaves_publicas(pub_k_b)
b.recibe_llaves_publicas(pub_k_a)

pub_k_a = a.final_keys()
pub_k_b = b.final_keys()
print('\nRonda2:')
print(f'{a.name} PKs: {pub_k_a}')
print(f'{b.name} PKs: {pub_k_b}')

a.recibe_llaves_publicas(pub_k_b)
b.recibe_llaves_publicas(pub_k_a)

print()
print("CIFRADO DE MENSAJE")
enc = a.cifrar(msg)  # Alice cifra el mensaje
print("Mensaje cifrado:", enc)
denc = b.descifrar(enc)  # Bob descifra el mensaje
print("Mensaje descifrado:", denc)
print("Son iguales?", "Sí" if msg == denc else "No")