BASE64_ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
B64_ALPH    = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def encode(text, alph):
    assert(len(text) % 3 == 0)
    
    result = ""
    
    for i in range(0, len(text), 3):
        piece = int.from_bytes(text[i:i+3], "big")
        
        segment = ""
        for j in range(4):
            segment += alph[piece & 63]
            piece >>= 6
        
        result += segment[::-1]
    
    return result

def decode(text, alph):
    assert(len(text) % 4 == 0)
    
    result = b""
    
    for i in range(0, len(text), 4):
        piece = 0
        for s in text[i:i+4]:
            piece <<= 6
            piece += alph.find(s)
        
        result += piece.to_bytes(3, "big")
    
    return result
            

FLAG = "uctf_ba5364_c1a5Sic_a1ph4b3t_j0ke".encode()
print(encode(FLAG, B64_ALPH))

# test work
import base64
print(base64.b64encode(FLAG).decode() == encode(FLAG, BASE64_ALPH))
print(decode(encode(FLAG, BASE64_ALPH), BASE64_ALPH))
