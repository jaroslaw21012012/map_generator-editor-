from PIL import Image

image = Image.open("assets/Aurora Tileset.png")

size = 32
blocks = []
for j in range(0, image.size[1], size):
    for i in range(0, image.size[0], size):
        box = (i, j, i+size, j+size)
        block = image.crop(box)
        blocks.append(block)

for x, block in enumerate(blocks):
     block.save(f"assets/cutter/aurora_{x}.png")