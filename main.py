
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import os
from datetime import datetime
import random
import argparse
from dataclasses import dataclass


@dataclass
class Params:

    size: dict = None
    min_rotation: float = 0.0
    max_rotation: float = 360.0
    flip_horizontal: float = 0.5
    flip_vertical: float = 0.5
    crop_width: int = 0
    crop_height: int = 0
    edges: bool = False
    color: float = 1.0
    brightness: float = 1.0
    contrast: float = 1.0
    sharpness: float = 1.0


def process_image(input_path, output_folder, output_count, params):
    name, extension = os.path.splitext(os.path.basename(input_path))
    date = datetime.now()
    output_folder = os.path.join(output_folder, "_".join([name, date.strftime("%m-%d-%Y-%H-%M-%S")]))

    for image_index in range(output_count):
        output_path = os.path.join(output_folder, "".join([str(image_index), extension]))
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        file = Image.open(input_path)

        file = apply_transformations(file, params)

        file.save(output_path, extension[1:])


def apply_transformations(file, params):
    file_width, file_height = file.size

    if file_width < params.crop_width or params.crop_width == 0:
        params.crop_width = file_width
    if file_height < params.crop_height or params.crop_height == 0:
        params.crop_height = file_height

    if params.size is None:
        params.size["width"] = file_width
        params.size["height"] = file_height

    crop_x = random.randint(0, file_width - params.crop_width)
    crop_y = random.randint(0, file_height - params.crop_height)

    file = file.crop((crop_x, crop_y, crop_x + params.crop_width, crop_y + params.crop_height))

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
                        crop_width=args.cwidth,
                        crop_height=args.cheight,
                        edges=args.edges,
                        color=args.color,
                        brightness=args.brightness,
                        sharpness=args.sharpness,
                        contrast=args.contrast)

    image_paths = []

    for path in paths:
        ext = os.path.splitext(path)[1]
        if ext in {".png", ".jpg", ".jpeg"}:
            image_paths.append(path)

    for index, path in enumerate(image_paths):
        process_image(os.path.join(in_folder, path), out_folder, int(args.count), parameters)
        print("/".join([str(index + 1), str(len(image_paths))]))


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
    parser.add_argument("--cwidth",
                        help="Width of crop window. Default (0) results in not cropping image",
                        default=0,
                        type=int)
    parser.add_argument("--cheight",
                        help="Height of crop window. Default (0) results in not cropping image",
                        default=0,
                        type=int)
    parser.add_argument("--size",
                        help="Output images size in format A,B. Default ((0,0)) results in not changing image size",
                        default=None,
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


if __name__ == '__main__':
    main(parse_arguments())
