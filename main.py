from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import os
from datetime import datetime
import random
import argparse


class Params:
    size = [0, 0]
    min_rotation = 0.0
    max_rotation = 360.0
    flip_horizontal = 0.5
    flip_vertical = 0.5
    width = 0
    height = 0
    edges = False
    color = 1.0
    brightness = 1.0
    contrast = 1.0
    sharpness = 1.0

    def __init__(self,
                 size=[0, 0],
                 min_rotation=0.0,
                 max_rotation=360.0,
                 flip_horizontal=0.5,
                 flip_vertical=0.5,
                 width=0,
                 height=0,
                 edges=False,
                 color=1.0,
                 brightness=1.0,
                 contrast=1.0,
                 sharpness=1.0):
        self.size = size
        self.min_rotation = min_rotation
        self.max_rotation = max(min_rotation, max_rotation)
        self.flip_horizontal = flip_horizontal
        self.flip_vertical = flip_vertical
        self.width = width
        self.height = height
        self.edges = edges
        self.color = color
        self.brightness = brightness
        self.contrast = contrast
        self.sharpness = sharpness


def process_image(input_path, output_folder, output_count, params):
    name = os.path.splitext(os.path.basename(input_path))[0]
    date = datetime.now()
    output_folder += "/" + name + date.strftime("%m-%d-%Y-%H-%M-%S")

    extension = os.path.splitext(input_path)[1]
    image_index = 0
    while image_index < output_count:
        output_path = output_folder + "/" + str(image_index) + extension
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        file = Image.open(input_path)

        file = apply_transformations(file, params)

        file.save(output_path, extension[1:])
        image_index += 1


def apply_transformations(file, params):
    if file.size[0] < params.width or params.width == 0:
        params.width = file.size[0]
    if file.size[1] < params.height or params.height == 0:
        params.height = file.size[1]

    if params.size[0] == 0:
        params.size[0] = file.size[0]
    if params.size[1] == 0:
        params.size[1] = file.size[1]

    crop_x = random.randint(0, file.size[0] - params.width)
    crop_y = random.randint(0, file.size[1] - params.height)

    file = file.crop((crop_x, crop_y, crop_x + params.width, crop_y + params.height))

    degrees = random.uniform(params.min_rotation, params.max_rotation)
    file = file.rotate(degrees)

    if random.random() < params.flip_horizontal:
        file = file.transpose(Image.FLIP_LEFT_RIGHT)

    if random.random() < params.flip_vertical:
        file = file.transpose(Image.FLIP_TOP_BOTTOM)

    file = file.convert("RGB")
    if params.edges:
        file = file.filter(ImageFilter.FIND_EDGES)

    enhancer = ImageEnhance.Brightness(file)
    file = enhancer.enhance(params.brightness)

    enhancer = ImageEnhance.Contrast(file)
    file = enhancer.enhance(params.contrast)

    enhancer = ImageEnhance.Sharpness(file)
    file = enhancer.enhance(params.sharpness)

    enhancer = ImageEnhance.Color(file)
    file = enhancer.enhance(params.color)

    return file.resize(tuple(params.size))


def main(args):
    if not args.input:
        in_folder = os.getcwd()
    else:
        in_folder = args.input
    if args.output:
        out_folder = args.output
    else:
        out_folder = in_folder

    paths = os.listdir(in_folder)
    parameters = Params(size=args.size,
                        min_rotation=args.minrot,
                        max_rotation=args.maxrot,
                        flip_horizontal=args.fliph,
                        flip_vertical=args.flipv,
                        width=args.width,
                        height=args.height,
                        edges=args.edges,
                        color=args.color,
                        brightness=args.brightness,
                        sharpness=args.sharpness,
                        contrast=args.contrast)

    path_index = 0
    while path_index < len(paths):
        ext = os.path.splitext(paths[path_index])[1]
        if ext not in {".png", ".jpg", ".jpeg"}:
            paths.remove(paths[path_index])
        else:
            path_index += 1
    for index, path in enumerate(paths):
        process_image(in_folder + "/" + path, out_folder, int(args.count), parameters)
        print(str(index + 1) + "/" + str(len(paths)))


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("count",
                        help="Output images count for each input image",
                        default=1,
                        type=int)
    parser.add_argument("--input",
                        help="Input folder",
                        default="")
    parser.add_argument("--output",
                        help="Output folder",
                        default="")
    parser.add_argument("--minrot",
                        help="Min value of randomized degree for rotation",
                        default=0,
                        type=int)
    parser.add_argument("--maxrot",
                        help="Max value of randomized degree for rotation",
                        default=360,
                        type=int)
    parser.add_argument("--fliph",
                        help="Horizontal flip probability",
                        default=0.5,
                        type=float)
    parser.add_argument("--flipv",
                        help="Vertical flip probability",
                        default=0.5,
                        type=float)
    parser.add_argument("--width",
                        help="Width of crop window. Default (0) results in not cropping image",
                        default=0,
                        type=int)
    parser.add_argument("--height",
                        help="Height of crop window. Default (0) results in not cropping image",
                        default=0,
                        type=int)
    parser.add_argument("--size",
                        help="Output images size in format A,B. Default ((0,0)) results in not changing image size",
                        default=[0, 0],
                        nargs="+",
                        type=int)
    parser.add_argument("--edges",
                        help="Detect edges",
                        default=False,
                        type=bool)
    parser.add_argument("--color",
                        help="Adjust color balance. 0.0 is black and white, 1.0 is original",
                        default=1.0,
                        type=float)
    parser.add_argument("--brightness",
                        help="Adjust brightness. 0.0 is black, 1.0 is original",
                        default=1.0,
                        type=float)
    parser.add_argument("--contrast",
                        help="Adjust contrast. 0.0 is solid grey, 1.0 is original",
                        default=1.0,
                        type=float)
    parser.add_argument("--sharpness",
                        help="Adjust sharpness. 0.0 is blurred, 1.0 is original, 2.0 is sharpened",
                        default=1.0,
                        type=float)

    return parser.parse_args()


main(parse_arguments())
