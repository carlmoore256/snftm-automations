#  convert ~/Downloads/282000007.png -resize "3840x2160^" -gravity center -extent 3840x2160 ~/Documents/SNFTM_Utilities/data/images/memories-of-qilin-7.
#  convert input.png -resize "3840x2160^" -gravity center -extent 3840x2160 output.png

from wand.image import Image
from wand.color import Color
from wand.exceptions import WandException
import argparse

from wand.image import Image
from wand.color import Color
import os


from defaults import DEFAULT_IMAGE_FORMAT, IMAGE_OUTPUT_ROOT, DEFAULT_RESOLUTION
from files import create_output_path, delete_if_exists, make_dir_if_not_exists

# def resize_and_extent(input_path, output_path, resolution=DEFAULT_RESOLUTION):
#     with Image(filename=input_path) as img:
#         img_ratio = img.width / img.height
#         size_ratio = resolution['width'] / resolution['height']
#         # Determine whether to resize based on width or height
#         if img_ratio > size_ratio:
#             # Image is wider than desired size, resize based on width
#             new_width = resolution['width']
#             new_height = int(new_width / img_ratio)
#         else:
#             # Image is taller than desired size, resize based on height
#             new_height = resolution['height']
#             new_width = int(new_height * img_ratio)
#         # Resize the image
#         img.transform(resize=f"{new_width}x{new_height}")
#         # Center the image
#         img.gravity = 'center'
#         with Image(width=resolution['width'], height=resolution['height'], background=Color('black')) as canvas:
#             canvas.composite(img, left=(resolution['width'] - img.width) // 2, top=(resolution['height'] - img.height) // 2)
#             canvas.save(filename=output_path)


def resize_and_extent(input_path, output_path, resolution=DEFAULT_RESOLUTION, inner_rotate=False):
    with Image(filename=input_path) as img:
        img_ratio = img.width / img.height
        size_ratio = resolution['width'] / resolution['height']
        if img_ratio > size_ratio:
            # Image is wider than desired size, resize based on width
            # rotate the image
            img.transform(resize=f"{resolution['width']}x")
        else:
            if inner_rotate:
                img.rotate(90)
            # img.rotate(90)
            img.transform(resize=f"x{resolution['height']}")        
            # Image is taller than desired size, resize based on height
        # Center the image
        img.gravity = 'center'
        with Image(width=resolution['width'], height=resolution['height'], background=Color('black')) as canvas:
            canvas.composite(img, left=(resolution['width'] - img.width) // 2, top=(resolution['height'] - img.height) // 2)
            canvas.save(filename=output_path)

def rotate(input_path, output_path, degrees):
    with Image(filename=input_path) as img:
        img.rotate(degrees)
        img.save(filename=output_path)

def resize_and_rotate(input_path, output_path=None, resolution=DEFAULT_RESOLUTION, inner_rotate=False):
    if output_path is None:
        output_path = create_output_path(input_path, IMAGE_OUTPUT_ROOT, DEFAULT_IMAGE_FORMAT)
    # make a version that has ROTATE_0 and ROTATE_90
    output_path_0 = os.path.splitext(output_path)[0] + "_ROTATE_0" + os.path.splitext(output_path)[1]
    output_path_90 = os.path.splitext(output_path)[0] + "_ROTATE_90" + os.path.splitext(output_path)[1]

    output_path_0_pre_rotate = os.path.splitext(output_path)[0] + "_ROTATE_0_PRE_ROTATE" + os.path.splitext(output_path)[1]
    output_path_90_pre_rotate = os.path.splitext(output_path)[0] + "_ROTATE_90_PRE_ROTATE" + os.path.splitext(output_path)[1]
    
    # pre_rotate_path = output_path.split('.')[0] + "_PRE_ROTATE" + os.path.splitext(output_path)[1]
    temp_pre_rotate = os.path.splitext(input_path)[0] + "_PRE_ROTATE" + os.path.splitext(input_path)[1]
    rotate(input_path, temp_pre_rotate, 90)

    resize_and_extent(input_path, output_path_0, resolution, inner_rotate)
    rotate(output_path_0, output_path_90, -90)

    resize_and_extent(temp_pre_rotate, output_path_0_pre_rotate, resolution, inner_rotate)
    rotate(output_path_0_pre_rotate, output_path_90_pre_rotate, -90)

    

    print(f'Wrote files to: {output_path_0} | {output_path_90} | {output_path_0_pre_rotate} | {output_path_90_pre_rotate}')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="The path to the input image")
    parser.add_argument("output_path", help="The path to the output image")
    parser.add_argument("width", help="The desired width of the output image", type=int)
    parser.add_argument("height", help="The desired height of the output image", type=int)
    args = parser.parse_args()
    resize_and_extent(args.input_path, args.output_path, {'width': args.width, 'height': args.height})

    rotate(args.output_path, args.output_path, 90)