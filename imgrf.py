# Resize images to fit specified width and height,
# empty space is filled with white.
#
# Requires package: python3-pillow

import argparse
from PIL import Image, UnidentifiedImageError
import glob

parser = argparse.ArgumentParser(description='Resize images to fill exactly the specified size.')
parser.add_argument('target_width', metavar='WIDTH', type=int,
                    help='target width')
parser.add_argument('target_height', metavar='HEIGHT', type=int,
                    help='target height')
parser.add_argument('files', metavar='FILE', type=str, nargs='+',
                    help='files')
args = parser.parse_args()
target_width = args.target_width
target_height = args.target_height

target_ratio = target_width / target_height
files = glob.iglob(args.files)

for filename in args.files:
    print(filename)
    try:
        im = Image.open(filename, "r")
    except FileNotFoundError:
        print("File not found: %s" % filename)
        continue
    except UnidentifiedImageError:
        print("File is not an image: %s" % filename)
        continue
    
    source_width, source_height = im.size
    source_ratio = float(source_width) / float(source_height)
    
    if source_ratio > target_ratio:
        width = target_width
        height = round(float(source_height * target_width) / float(source_width))
    else:
        height = target_height
        width = round(float(source_width * target_height) / float(source_height))
    
    image_resized = im.resize((width, height), Image.LANCZOS)
    background = Image.new('RGBA', (target_width, target_height), (255, 255, 255, 255))
    offset = (int(round(((target_width - width) / 2), 0)), int(round(((target_height - height) / 2),0)))
    
    background.paste(image_resized, offset)
    im.close()
    
    background_rgb = background.convert('RGB')
    background_rgb.save(filename)

