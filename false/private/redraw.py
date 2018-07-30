from PIL import Image
from PIL.PngImagePlugin import PngInfo

FLAG = "dWN0Zl9pX2RlY29kZWRfcXJzX3llcw"

inf = PngInfo()
inf.add_text("png", FLAG)

name = input()
im = Image.open(name)
px = im.load()

for j in range(im.height):
    for i in range(im.width):
        if px[i, j] == (0, 0, 0):
            px[i, j] = (254, 254, 254)
im.save("../public/task.png", pnginfo=inf)

