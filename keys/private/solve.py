def decrypt(text, shift):
    result = bytearray()
    for symbol in text:
        result.append((symbol - shift + 256) % 256)
    return result

with open("../public/encrypted.bin", "rb") as f:
    data = f.read()

with open("result.bin", "wb") as f:
    for shift in range(256):
        f.write(decrypt(data, shift))
        f.write(b'\n')
