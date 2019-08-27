from PIL import Image
import os
from datetime import datetime
import random


class Params:
    size = (0, 0)
    min_rotation = 0.0
    max_rotation = 360.0
#probabilities of applying flip
    flip_horizontal = 0.5
    flip_vertical = 0.5

    def __init__(self, size=(0, 0), min_rotation=0.0, max_rotation=360.0, flip_horizontal=0.5, flip_vertical=0.5):
        self.size = size
        self.min_rotation = min_rotation
        self.max_rotation = max_rotation
        self.flip_horizontal = flip_horizontal
        self.flip_vertical = flip_vertical


def process_image(input_path, output_count, params):
    name = os.path.splitext(input_path)[0]
    extension = os.path.splitext(input_path)[1]

    if extension not in {".png", ".jpg"}:
        return

    date = datetime.now()
    output_folder = name + date.strftime("%m-%d-%Y-%H-%M-%S")

    image_index = 0
    while image_index < output_count:
        output_path = output_folder + "/" + str(image_index) + extension
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        degrees = random.uniform(params.min_rotation, params.max_rotation)

        file = Image.open(input_path)

        file = file.rotate(degrees)

        if random.random() < params.flip_horizontal:
            file = file.transpose(Image.FLIP_LEFT_RIGHT)

        if random.random() < params.flip_vertical:
            file = file.transpose(Image.FLIP_TOP_BOTTOM)

        file = file.resize(params.size)
        file.save(output_path, "PNG")
        image_index += 1


input_folder = "/home/kwoznicki/Documents/GenPic/data"
paths = os.listdir(input_folder)
parameters = Params()
for path in paths:
    process_image(input_folder + "/" + path, 3, parameters)