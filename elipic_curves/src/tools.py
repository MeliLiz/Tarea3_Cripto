# Default alphabet
alphabet = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def isPrime(n):
    '''Nos dice si un número n es primo'''
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def inv_add(a, mod):
    '''Nos da el inverso aditivo tal que a + i == 0 modulo n'''
    return (-a) % mod

def inv_mult(a, mod):
    '''Nos da el inverso multiplicativo modulo n'''
    return pow(a, mod - 2, mod) #Por el teorema de Fermat

def table(elliptic_curve, alphabet = alphabet):
    '''Regresa una tabla de un abecedario mapeado a puntos de la curva elíptica e'''
    pts = elliptic_curve.points[1:]  # Excluimos el punto al infinito

    if len(pts) < len(alphabet):
        print(f"Advertencia: la curva tiene menos puntos ({len(pts)}) que los caracteres requeridos ({len(alphabet)})")
        l = alphabet[:len(pts)]
    else:
        l = alphabet

    # Creamos el diccionario de mapeo
    table = {}
    for i in range(len(l)):
        if i < len(pts):
            table[l[i]] = pts[i]

    return table


if __name__ == '__main__':
    print ((inv_mult(3, 7) * 3) % 7 == 1) 