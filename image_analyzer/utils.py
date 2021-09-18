import os
from PIL import Image, ImageColor


def get_client_ip(request):
    """
    Get current client ip (version 4)
    Supports proxy users
    :param request: HttpRequest
    :return: string -> user' ip
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def truncate_utf8_chars(filename, count, ignore_newlines=True):
    """
    Truncates last `count` characters of a text file encoded in UTF-8.
    :param filename: The path to the text file to read
    :param count: Number of UTF-8 characters to remove from the end of the file
    :param ignore_newlines: Set to true, if the newline character at the end of the file should be ignored
    """
    with open(filename, 'rb+') as f:
        size = os.fstat(f.fileno()).st_size

        offset = 1
        chars = 0
        while offset <= size:
            f.seek(-offset, os.SEEK_END)
            b = ord(f.read(1))

            if ignore_newlines:
                if b == 0x0D or b == 0x0A:
                    offset += 1
                    continue

            if b & 0b10000000 == 0 or b & 0b11000000 == 0b11000000:
                # This is the first byte of a UTF8 character
                chars += 1
                if chars == count:
                    # When `count` number of characters have been found, move current position back
                    # with one byte (to include the byte just checked) and truncate the file
                    f.seek(-1, os.SEEK_CUR)
                    f.truncate()
                    return
            offset += 1


def black_white_diff(image_path):
    """
    Get difference between amount of black (#000000)
    and white (#ffffff) pixels on chosen image
    :param image_path: str -> full path to the image (media/....)
    :return: tuple -> (count of white pixels, count of black pixels)
    """
    image = Image.open(image_path.lstrip('/'))
    pixels = image.load()
    black_count = white_count = 0
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            r, g, b = pixels[x, y][0], pixels[x, y][1], pixels[x, y][2]  # To avoid bug with floating Alpha
            if r == g == b == 255:
                white_count += 1
            elif r == g == b == 0:
                black_count += 1

    return white_count, black_count


def get_pixel_amount_by_hex(hex_color, image_path):
    """
    Get amount of pixels with given color (hex_color)
    :param hex_color: str - > color in hex format (#......)
    :param image_path: str -> path to the image
    :return: int -> count of pixels with given color
    """
    ex_r, ex_g, ex_b = ImageColor.getcolor(hex_color, "RGB")

    image = Image.open(image_path.lstrip('/'))
    pixels = image.load()
    pixel_count = 0

    for x in range(image.size[0]):
        for y in range(image.size[1]):
            r, g, b = pixels[x, y][0], pixels[x, y][1], pixels[x, y][2]
            if r == ex_r and g == ex_g and b == ex_b:
                pixel_count += 1

    return pixel_count
