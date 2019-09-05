# GenPic

For given directory this script creates sets of randomly transformed images based on images in directory and supplied arguments.

## Usage
Run by typing ```python3``` followed by path to script and arguments, e.g. ```python3 genpic.py 10 input output```.

## Command line arguments
```
positional arguments:
  count                 Output images count for each input image
  input                 Input folder
  output                Output folder

optional arguments:
  -h, --help            show this help message and exit
  --minrot MINROT       Min value of randomized degree for rotation
  --maxrot MAXROT       Max value of randomized degree for rotation
  --fliph FLIPH         Horizontal flip probability
  --flipv FLIPV         Vertical flip probability
  --cwidth CWIDTH       Width of crop window. Default (0) results in not
                        cropping image
  --cheight CHEIGHT     Height of crop window. Default (0) results in not
                        cropping image
  --size SIZE [SIZE ...]
                        Output images size in format A,B. Default ((0,0))
                        results in not changing image size
  --edges EDGES         Detect edges
  --color COLOR         Adjust color balance. 0.0 is black and white, 1.0 is
                        original
  --brightness BRIGHTNESS
                        Adjust brightness. 0.0 is black, 1.0 is original
  --contrast CONTRAST   Adjust contrast. 0.0 is solid grey, 1.0 is original
  --sharpness SHARPNESS
                        Adjust sharpness. 0.0 is blurred, 1.0 is original, 2.0
                        is sharpened
  -r, --recurse         Process images in all child directories
```