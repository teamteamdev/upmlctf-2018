def encrypt(text, shift):
    result = bytearray()
    for symbol in text:
        result.append((symbol + shift) % 256)
    return result

TEXT = b"it was easy, huh? do you want some flag? yes? okay, here is your flag: uctf_caesar_can_be_not_only_for_letters"
SHIFT = 117

with open("../public/encrypted.bin", "wb") as f:
    f.write(encrypt(TEXT, SHIFT))

    