
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


def process_image(input_path: str, output_folder: str, output_count: int, params: Params):
    name, extension = os.path.splitext(os.path.basename(input_path))
    date: str = datetime.now()
    output_folder = os.path.join(output_folder, "_".join([name, date.strftime("%m-%d-%Y-%H-%M-%S")]))

    for image_index in range(output_count):
        output_path: str = os.path.join(output_folder, "".join([str(image_index), extension]))
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        image: Image = Image.open(input_path)

        image = apply_transformations(image, params)

        image.save(output_path, extension[1:])


def apply_transformations(image: Image, params: Params):
    image_width, image_height = image.size

    if image_width < params.crop_width or params.crop_width == 0:
        params.crop_width = image_width
    if image_height < params.crop_height or params.crop_height == 0:
        params.crop_height = image_height

    if params.size is None:
        params.size["width"] = image_width
        params.size["height"] = image_height

    crop_x: int = random.randint(0, image_width - params.crop_width)
    crop_y: int = random.randint(0, image_height - params.crop_height)

    image = image.crop((crop_x, crop_y, crop_x + params.crop_width, crop_y + params.crop_height))

    degrees: float = random.uniform(params.min_rotation, params.max_rotation)
    image = image.rotate(degrees)

    if random.random() < params.flip_horizontal:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)

    if random.random() < params.flip_vertical:
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

    image = image.convert("RGB")
    if params.edges:
        image = image.filter(ImageFilter.FIND_EDGES)

    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(params.brightness)

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(params.contrast)

    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(params.sharpness)

    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(params.color)

    return image.resize(tuple(params.size))


def main(args):

    invalid_path: bool = False

    if not os.path.exists(args.input):
        print("Input folder does not exist")
        invalid_path = True

    if not os.path.exists(args.output):
        print("Output folder does not exist")
        invalid_path = True

    if invalid_path:
        return

    paths: list = []

    if args.recurse:
        for root, directories, names in os.walk(args.input):
            for name in names:
                paths.append("/".join([root, name]))
    else:
        paths = os.listdir(args.input)

    parameters: Params = Params(size=args.size,
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

    image_paths: list = []

    for path in paths:
        ext: str = os.path.splitext(path)[1]
        if ext in {".png", ".jpg", ".jpeg"}:
            image_paths.append(path)

    if len(image_paths) == 0:
        print("No images to process in input folder")

    for index, path in enumerate(image_paths):
        process_image(os.path.join(args.input, path), args.output, int(args.count), parameters)
        print("/".join([str(index + 1), str(len(image_paths))]))


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("count",
                        help="Output images count for each input image",
                        type=int)
    parser.add_argument("input",
                        help="Input folder")
    parser.add_argument("output",
                        help="Output folder")
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
    parser.add_argument("-r",
                        "--recurse",
                        help="Process images in all child directories",
                        action="store_true")

    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arguments())
