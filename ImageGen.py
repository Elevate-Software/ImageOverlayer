# Description
# -------------
# Overlays a name on top of a diploma template image and saves output to /output folder.

# Resources
# -------------
# Pillow Image Draw: https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
# Pillow Image Font: https://pillow.readthedocs.io/en/stable/reference/ImageFont.html

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

TEMPLATE = "diploma_template.png"               # filename for the diploma template
FONT = "Gilroy-Bold.ttf"                        # font filename (must be ttf, must be in same folder)

NAME_FONT_SIZE = 65                             # default font size for the name on the diploma
NAME_POSITION = (1391 // 2, 983 // 2 - 80)      # center point for drawing the name (x_pos, y_pos)
NAME_COLOR = (74, 79, 77)                       # color (r, g, b)
MAX_WIDTH = 800                                 # max width that the name should take up

# test names only
test_data = [
    "Matthew Merrill",
    "Humongo-Long-Ass-Mother-Trucking-Giant-Name McDuff",
    "James Hernandez-Chavez Smithsonian"
]


def generate(name: str):
    """
    Generates a single diploma image given a name and date.

    :param name: The name that should appear on the diploma
    :return:
    """

    # open template image and create new draw object
    img = Image.open(TEMPLATE)
    img_modified = ImageDraw.Draw(img)

    # create font object for name
    name_font = ImageFont.truetype(FONT, NAME_FONT_SIZE)

    # adjust name font size if output would be too long
    font_size = NAME_FONT_SIZE
    while name_font.getsize(name)[0] > MAX_WIDTH:
        font_size -= 1
        name_font = ImageFont.truetype(FONT, font_size)

    # draw name text onto image
    img_modified.text(NAME_POSITION, name, fill=NAME_COLOR, font=name_font, anchor="ms", align="center")

    # save the image
    img.save(f"output/{name}_diploma.png")


# Runs test data if this is the main file
if __name__ == "__main__":
    for item in test_data:
        generate(item)
