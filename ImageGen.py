

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

MAX_WIDTH = 800                                 # max width that the name should take up
TEMPLATE = "diploma_template.jpg"               # filename for the diploma template
FONT = "times.ttf"                              # font filename (must be ttf, must be in same folder)

NAME_FONT_SIZE = 65                             # default font size for the name on the diploma
NAME_POSITION = (1536/2, 1154/2 - 100)          # center point for drawing the name (aligned center / base-point)

DATE_FONT_SIZE = 40                             # default font size for the date on the diploma
DATE_POSITION = (1200, 880)                     # center point for drawing the date (aligned center / base-point)

# test names and dates (temporary)
test_data = [
    ("Matthew Merrill", "04/16/22"),
    ("Humongo-Long-Ass-Mother-Trucking-Giant-Name McDuff", "04/16/22")
]


def generate(name: str, date: str):
    """

    :param name: The name that should appear on the diploma
    :param date: The date that should appear on the diploma
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
    img_modified.text(NAME_POSITION, name, fill=(0, 0, 0), font=name_font, anchor="ms", align="center")

    # create date font object and draw date text onto image
    date_font = ImageFont.truetype(FONT, DATE_FONT_SIZE)
    img_modified.text(DATE_POSITION, date, fill=(0, 0, 0), font=date_font, anchor="ms", align="center")

    # save the image
    img.save(f"output/{name}_diploma.jpg")


# Runs test data if this is the main file
if __name__ == "__main__":
    for item in test_data:
        generate(*item)
