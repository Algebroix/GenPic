from PIL import Image
import os
import sys
from datetime import datetime
import random


class Params:
    size = (1, 1)
    min_rotation = 0.0
    max_rotation = 360.0
#probabilities of applying flip
    flip_horizontal = 0.5
    flip_vertical = 0.5

    def __init__(self, size, min_rotation=0.0, max_rotation=360.0, flip_horizontal=0.5, flip_vertical=0.5):
        self.size = size
        self.min_rotation = min_rotation
        self.max_rotation = max_rotation
        self.flip_horizontal = flip_horizontal
        self.flip_vertical = flip_vertical


def process_image(input_path, output_folder, output_count, params):
    name = os.path.splitext(os.path.basename(input_path))[0]
    extension = os.path.splitext(input_path)[1]

    if extension not in {".png", ".jpg", ".jpeg"}:
        return

    date = datetime.now()
    output_folder += "/" + name + date.strftime("%m-%d-%Y-%H-%M-%S")

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
        file.save(output_path, extension[1:])
        image_index += 1


if len(sys.argv) < 2:
    in_folder = os.getcwd()
else:
    in_folder = sys.argv[1]
if len(sys.argv) == 3:
    out_folder = sys.argv[2]
else:
    out_folder = in_folder

paths = os.listdir(in_folder)
parameters = Params((1000, 800))
for path in paths:
    process_image(in_folder + "/" + path, out_folder, 3, parameters)

