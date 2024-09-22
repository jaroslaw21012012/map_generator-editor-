from PIL import Image
import os

folder_input = "assets/Player/Idle/Left"
folder_output = "assets/Player/Idle/Right"

files = os.listdir(folder_input)
for image in files:
    image_path = os.path.join(folder_input, image)
    img = Image.open(image_path)
    mirrored = img.transpose(Image.FLIP_LEFT_RIGHT)
    new_image_path = os.path.join(folder_output, image)
    mirrored.save(new_image_path)