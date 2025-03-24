
# Hard-coded values for SHA256

# Initial hash values: The values are the first 32 bits of the fractional parts of the square roots of the first 8 primes.
h = ['0x6a09e667', '0xbb67ae85', '0x3c6ef372', '0xa54ff53a', '0x510e527f', '0x9b05688c', '0x1f83d9ab', '0x5be0cd19']

# To find out, use the following
# import math

# s_root = math.sqrt(2) # 1.4142135623730951
# fractions = math.modf(s_root)[0] # 0.41421356237309515
# fractions = hex(int(fractions * (2**32)))
# print(as_hex) #'0x6a09e667'


# Round Constants: The first 32 bits of the fractional parts of the cubic roots of the first 64 prime numbers.
k = ['0x428a2f98', '0x71374491', '0xb5c0fbcf', '0xe9b5dba5', '0x3956c25b', '0x59f111f1', '0x923f82a4','0xab1c5ed5', 
     '0xd807aa98', '0x12835b01', '0x243185be', '0x550c7dc3', '0x72be5d74', '0x80deb1fe','0x9bdc06a7', '0xc19bf174', 
     '0xe49b69c1', '0xefbe4786', '0x0fc19dc6', '0x240ca1cc', '0x2de92c6f','0x4a7484aa', '0x5cb0a9dc', '0x76f988da', 
     '0x983e5152', '0xa831c66d', '0xb00327c8', '0xbf597fc7','0xc6e00bf3', '0xd5a79147', '0x06ca6351', '0x14292967', 
     '0x27b70a85', '0x2e1b2138', '0x4d2c6dfc','0x53380d13', '0x650a7354', '0x766a0abb', '0x81c2c92e', '0x92722c85', 
     '0xa2bfe8a1', '0xa81a664b','0xc24b8b70', '0xc76c51a3', '0xd192e819', '0xd6990624', '0xf40e3585', '0x106aa070', 
     '0x19a4c116','0x1e376c08', '0x2748774c', '0x34b0bcb5', '0x391c0cb3', '0x4ed8aa4a', '0x5b9cca4f', '0x682e6ff3',
     '0x748f82ee', '0x78a5636f', '0x84c87814', '0x8cc70208', '0x90befffa', '0xa4506ceb', '0xbef9a3f7','0xc67178f2']

def translate(message):

    # string characters to unicode

    charcodes = [ord(char) for char in message]


    # Now convert unicode values to 8-bit strings

    bytes = []
    for char in charcodes:
        bytes.append(bin(char)[2:].zfill(8))


    # 8-bit strings to list of bits of integer
    bits = []

    for byte in bytes:
        for bit in byte:
            bits.append(int(bit))

    return bits

# Convert base 2 to base 16
# 4 bits in base 2 give a number in base 16, so we just have to group it four by four

BASE2_TO_BASE16 = {"0000": "0", "0001": "1", "0010": "2", "0011": "3",
                   "0100": "4", "0101": "5", "0110": "6", "0111": "7",
                   "1000": "8", "1001": "9", "1010": "a", "1011": "b",
                   "1100": "c", "1101": "d", "1110": "e", "1111": "f"}

def b2Tob16_myimplementation(value):

    # Convert to string for .join()
    value = [str(x) for x in value]

    # Convert to hexadecimal in chunks of 4 with the dictionary BASE2_TO_BASE16
    hex_representation = []
    for i in range(0,len(value),4):
        hex_representation.append(BASE2_TO_BASE16["".join(value[i:i+4])])

    return "".join(hex_representation)

def b2Tob16(value):
    # Takes list of 32 bits
    # Convert to string
    value = "".join([str(x) for x in value])

    # Create 4-bit chunks and add bit indicator "0b"
    binaries = []

    for d in range(0,len(value),4):
        binaries.append('0b' + value[d:d+4])

    
    # Transform to hexadecimal and remove hex-indicator
    hexes = ""
    for b in binaries:
        hexes += hex(int(b,2))[2:]

    return hexes 



# Fill zeros [This looks a bit convoluted...]
def fillZeros(bits, length=8, endian="LE"):
    l = len(bits)

    if endian=="LE":
        for i in range(l,length):
            bits.append(0)
    else:
        while l < length:
            bits.insert(0,0)
            l = len(bits)

    return bits


# THE Chunker

def chunker(bits, chunk_length=8):
    # divides bits into desired byte/word chunks

    chunked = []

    for b in range(0, len(bits), chunk_length):
        chunked.append(bits[b:b + chunk_length])
    return chunked



# To initialise the hard-coded values

def initializer(values):
    #convert from hex to python binary string (with cut bin indicator ('0b'))
    binaries = [bin(int(v, 16))[2:] for v in values]
    #convert from python string representation to a list of 32 bit lists
    words = []
    for binary in binaries:
        word = []
        for b in binary:
            word.append(int(b))
        words.append(fillZeros(word, 32, 'BE'))
    return words


if __name__ == "__main__":
    print(b2Tob16(translate("XO")))