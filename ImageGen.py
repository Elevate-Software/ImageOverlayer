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
FONT_LIGHT = "Gilroy-Light.ttf"

NAME_FONT_SIZE = 65                             # default font size for the name on the diploma
NAME_POSITION = (1391 // 2, 983 // 2 - 80)      # center point for drawing the name (x_pos, y_pos)
NAME_COLOR = (74, 79, 77)                       # color (r, g, b)
MAX_WIDTH = 800                                 # max width that the name should take up

TOKEN_FONT_SIZE = 20
TOKEN_POSITION = (1320, 70)
TOKEN_COLOR = (104, 109, 107)


def generate(name: str, token: int):
    """
    Generates a single diploma image given a name and date.

    :param name: The name that should appear on the diploma.
    :param token: NFT token ID for the image to be generated.
    :return:
    """

    # open template image and create new draw object
    img = Image.open(TEMPLATE)
    img_modified = ImageDraw.Draw(img)

    # create font object for name and token watermark
    name_font = ImageFont.truetype(FONT, NAME_FONT_SIZE)
    token_font = ImageFont.truetype(FONT_LIGHT, TOKEN_FONT_SIZE)

    # adjust name font size if output would be too long
    font_size = NAME_FONT_SIZE
    while name_font.getsize(name)[0] > MAX_WIDTH:
        font_size -= 1
        name_font = ImageFont.truetype(FONT, font_size)

    # draw name text onto image
    img_modified.text(NAME_POSITION, name, fill=NAME_COLOR, font=name_font, anchor="ms", align="center")

    # draw token ID onto image
    img_modified.text(TOKEN_POSITION, f'Token-ID : {token}', fill=TOKEN_COLOR, font=token_font, anchor="rs", align="center")

    # save the image
    img.save(f"output/{name}_diploma.png")


# generates images for all names in the test data
if __name__ == "__main__":
    test_data = [
        ("Matthew Merrill", 20),
        ("Humongo-Long-Ass-Mother-Trucking-Giant-Name McDuff", 210020),
        ("James Hernandez-Chavez Smithsonian", 22)
    ]

    for item in test_data:
        generate(*item)
