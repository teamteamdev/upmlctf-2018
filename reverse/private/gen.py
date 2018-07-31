# swap it to get solution
fin = open("pic.png", "rb")
fout = open("../public/file.bin", "wb")

data = fin.read()[::-1]
result = bytearray()
for byte in data:
    high = byte >> 4
    low = byte & 0xF
    rbyte = (low << 4) + high
    result.append(rbyte)
fout.write(result)
fout.close()

