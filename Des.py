###### DES using the Diffie Hellman key exchange ######


##################################### Constants #####################################
INITIAL_PERMUTATION =   [58, 50, 42, 34, 26, 18, 10, 2,60, 52, 44, 36, 28, 20, 12, 4,
                        62, 54, 46,38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
                        57, 49,41, 33, 25, 17, 9, 1,59, 51, 43, 35, 27, 19, 11, 3,
                        61, 53, 45, 37, 29, 21, 13, 5,63, 55, 47, 39, 31, 23, 15,7]

FINAL_PERMUTATION = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7,47, 15, 55, 23, 63, 31,
                    38, 6, 46,14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
                    36, 4, 44, 12,52, 20, 60, 28,35, 3, 43, 11, 51, 19, 59, 27,
                    34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

P_PERMUTATION_TABLE =   [16, 7, 20, 21, 29, 12, 28, 17,
                        1, 15, 23, 26, 5, 18,31, 10,
                        2, 8, 24,14, 32, 27, 3, 9,
                        19, 13, 30, 6, 22, 11,4, 25]

PC1_PERMUTATION_TABLE = [57, 49, 41, 33,25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
                        10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
                        63, 55, 47, 39, 31, 23, 15,7, 62, 54, 46, 38, 30, 22,
                        14, 6, 61, 53, 45, 37, 29,21, 13, 5, 28, 20, 12, 4]

PC2_PERMUTATION_TABLE = [14, 17, 11, 24, 1, 5,3, 28, 15, 6, 21, 10,
                        23, 19, 12, 4, 26, 8,16, 7, 27, 20, 13, 2,
                        41, 52, 31, 37, 47, 55,30, 40, 51, 45, 33, 48,
                        44, 49, 39, 56, 34, 53,46, 42, 50, 36, 29, 32]

ROTATIONS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1] #Rotations per round

S_BOXES = [ [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],[0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],[15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
            
            [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],[3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],[13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
            
            [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],[13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],[1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
            
            [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],[13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],[3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
            
            [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],[14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],[11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
            
            [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],[10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],[4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
            
            [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],[13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],[6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
            
            [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],[1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],[2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

EXPANSION = [32, 1, 2, 3, 4, 5, 4, 5,6, 7, 8, 9, 8, 9, 10, 11,
            12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20,21, 20, 21,
            22, 23, 24, 25, 24, 25,26, 27, 28, 29, 28, 29, 30, 31, 32, 1]


##################################### Functions for DES #####################################

# Function to permutate a block of bits according to the table
def permutation(block, table):
    result = []
    for i in table:
        result.append(block[i - 1])
    return result

#Execute an XOR between two blocks of bits
def xor(block1, block2):
    result = []
    for b1,b2 in zip(block1, block2):
        result.append(b1 ^ b2)
    return result

#Apply the S-boxes on a 48-bit block
def apply_sbox(block):
    result = []
    for i in range(8):
        part = block[i * 6:(i + 1) * 6]
        row = part[0] * 2 + part[5] 
        col = part[1] * 8 + part[2] * 4 + part[3] * 2 + part[4]
        value = S_BOXES[i][row][col]
        to_add = []
        for b in f'{value:04b}':
            to_add.append(int(b))
        result += to_add
    return result

#Feistel function, receives the right half and the key
def feistel(right, key):
    expanded_half = permutation(right, EXPANSION) # Expand the 32-bit half to 48 bits
    xor_result = xor(expanded_half, key)  
    substituted = apply_sbox(xor_result)  #Substitution with S-boxes
    return permutation(substituted, P_PERMUTATION_TABLE) 

#Apply a Feistel round, receives the left half, right half and the key
def feistel_round(left, right, key):
    new = xor(left, feistel(right, key)) 
    return right, new  #Change the right half with the new right half

#Generate the 16 subkeys
def get_subkeys(key):
    key = permutation(key, PC1_PERMUTATION_TABLE) 
    #Split the key in two
    r1 = key[:28]
    r2 =key[28:]

    subkeys = []
    for i in range(16):
        #Get the rotations
        r1 = r1[ROTATIONS[i]:] + r1[:ROTATIONS[i]]
        r2 = r2[ROTATIONS[i]:] + r2[:ROTATIONS[i]]
        #Get the subkey from the permuted key
        permuted = permutation(r1 + r2, PC2_PERMUTATION_TABLE)
        subkeys.append(permuted)
    return subkeys


##################################### String, bits and hex related #####################################

#Padding for the text to be multiple of 64 bits
def pad(text):
    length = len(text) % 8 #8 bytes = 64 bits
    pad_len = 8 - length
    total_pad = chr(pad_len) * pad_len
    return text + total_pad

#Remove the padding
def unpad(text):
    pad_len = ord(text[-1])
    return text[:-pad_len]

def text_to_bits(text):
    bits = []
    for char in text:
        to_add =[]
        for bit in f'{ord(char):08b}':
            to_add.append(int(bit))
        bits += to_add
    return bits

def bits_to_text(bits):
    chars = []
    for b in range(0, len(bits), 8):
        byte = bits[b:b + 8]
        bits1 = ''.join([str(bit) for bit in byte])
        chars.append(chr(int(bits1, 2)))
    return ''.join(chars)

#To get an hexadecimal representation instead of weird characters
def bits_to_hex(bits):
    hex_str = ''
    for i in range(0, len(bits), 4):
        nibble = bits[i:i+4]
        hex_str += f'{int("".join(map(str, nibble)), 2):x}'
    return hex_str

def hex_to_bits(hex_str):
    bits = []
    for char in hex_str:
        bits += [int(bit) for bit in f'{int(char, 16):04b}']
    return bits

##################################### DES #####################################

############## Encryption ##############

#Encrypt a 64-bit block (16 rounds)
def encrypt_block(block, keys):
    permuted_block = permutation(block, INITIAL_PERMUTATION)
    left = permuted_block[:32]
    right = permuted_block[32:]

    for i in range(16):
        left, right = feistel_round(left, right, keys[i])

    final_block = permutation(right + left, FINAL_PERMUTATION)
    return final_block

def encrypt(text, shared_point): # Receives text, not bits, the key is given as bits
    text = text_to_bits(pad(text))
    
    #The subkeys are generated form the key obtained from the shared point
    subkeys = get_subkeys(point_to_key(shared_point))

    #Cipher in 64-bit blocks
    encrypted_bits = []
    for i in range(0, len(text), 64):
        block = text[i:i + 64]
        encrypted_bits += encrypt_block(block, subkeys)
    return encrypted_bits

############## Decryption ##############

#Decryption of a 64-bit block (16 rounds)
def decrypt_block(block, keys):
    permuted_block = permutation(block, INITIAL_PERMUTATION)
    left, right = permuted_block[:32], permuted_block[32:]

    for i in range(15, -1, -1):
        left, right = feistel_round(left, right, keys[i])

    final_block = permutation(right + left, FINAL_PERMUTATION)
    return final_block

def decrypt(bits, shared_point): # Receives bits, not text
    
    #The subkeys are generated form the key obtained from the shared point
    subkeys = get_subkeys(point_to_key(shared_point))

    # Descifrado en bloques de 64 bits
    decrypted_bits = []
    for i in range(0, len(bits), 64):
        block = bits[i:i + 64]
        decrypted_bits += decrypt_block(block, subkeys)
    return bits_to_text(decrypted_bits)

# Convert a point of a curve to a key
def point_to_key(point):
    x, y = point
    key = f'{x:032b}{y:032b}' 
    # Return 64 bits
    return [int(bit) for bit in key]

"""# Text to encrypt
    key = "llavesct" #8 characters key

    #Encrypt
    ciphertext_bits = encrypt(plaintext, key)
    print("Texto cifrado en bits:")
    for bit in ciphertext_bits:
        print(bit, end="")
    print()

    #Get the hexadecimal representation
    ciphertext_hex = bits_to_hex(ciphertext_bits)
    print("Texto cifrado hexadecimal:", ciphertext_hex)

    #DEcrypt the bits gotten from the encryption
    decrypted_text = decrypt(ciphertext_bits, key)
    print("Texto descifrado:", decrypted_text)"""

if __name__ == '__main__':
    plaintext = "lunes"
    #key = point_to_key((1, 2))
    ciphertext_bits = encrypt(plaintext, (18,18))
    for bit in ciphertext_bits:
        print(bit, end="")
    print()

    #Get the hexadecimal representation
    ciphertext_hex = bits_to_hex(ciphertext_bits)
    print("Texto cifrado hexadecimal:", ciphertext_hex)

    #DEcrypt the bits gotten from the encryption
    decrypted_text = decrypt(ciphertext_bits, (18,18))
    print("Texto descifrado:", decrypted_text)
   
    