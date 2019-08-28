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
    width = 0
    height = 0

    def __init__(self, size, min_rotation=0.0, max_rotation=360.0, flip_horizontal=0.5, flip_vertical=0.5, width=0, height=0):
        self.size = size
        self.min_rotation = min_rotation
        self.max_rotation = max_rotation
        self.flip_horizontal = flip_horizontal
        self.flip_vertical = flip_vertical
        self.width = width
        self.height = height


def process_image(input_path, output_folder, output_count, params):
    name = os.path.splitext(os.path.basename(input_path))[0]
    extension = os.path.splitext(input_path)[1]

    date = datetime.now()
    output_folder += "/" + name + date.strftime("%m-%d-%Y-%H-%M-%S")

    image_index = 0
    while image_index < output_count:
        output_path = output_folder + "/" + str(image_index) + extension
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        file = Image.open(input_path)

        if file.size[0] < params.width or params.width == 0:
            params.width = file.size[0]
        if file.size[1] < params.height or params.height == 0:
            params.width = file.size[1]

        crop_x = random.randint(0, file.size[0] - params.width)
        crop_y = random.randint(0, file.size[1] - params.height)

        file = file.crop((crop_x, crop_y, crop_x + params.width, crop_y + params.height))

        degrees = random.uniform(params.min_rotation, params.max_rotation)
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
parameters = Params((1000, 800), width=500, height=600)
path_index = 0
while path_index < len(paths):
    ext = os.path.splitext(paths[path_index])[1]
    if ext not in {".png", ".jpg", ".jpeg"}:
        paths.remove(paths[path_index])
    else:
        path_index += 1
for index, path in enumerate(paths):
    process_image(in_folder + "/" + path, out_folder, 3, parameters)
    print(str(index + 1) + "/" + str(len(paths)))

