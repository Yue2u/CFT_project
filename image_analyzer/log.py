from .models import ImageHolder

import os
import json
from datetime import datetime

from .utils import truncate_utf8_chars


def initialize_log_file(directory, file_name):
    """
    Initialize new log file like empty JSON array ('[]')
    :param file_name: str -> file_name
    :param directory: str -> destination folder
    :return: boolean -> True if new file created, else returns False
    """
    file_path = os.path.join(directory, file_name)

    if os.path.exists(file_path):  # Don't create new file if it exists
        return False

    with open(file_path, mode='w', encoding='utf-8') as file:
        file.write('[]')
    return True


def get_log_file_name():
    """
    Evaluate log file name based on current date & time (new file every 30 minutess)
    :return: str -> log file name
    """
    current_date = datetime.now()
    date = current_date.date()

    hour = f'0{current_date.hour}' if current_date.hour < 10 else str(current_date.hour)
    minutes = '00' if current_date.minute < 30 else '30'

    return f'{date}_{hour}-{minutes}.log'


def log_request(user_ip, operation, **kwargs):
    """
    Logging requests
    :param user_ip: str -> user' ip
    :param operation: str -> operation type (one of UPLOAD_NEW_IMAGE and GET_HEX_COUNT
    :param kwargs:
    :return: None
    """

    result = {key: value for key, value in kwargs.items()} | {'User': user_ip,
                                                              'operation_type': operation}  # merge dicts

    log_file = get_log_file_name()

    first_record = initialize_log_file('image_analyzer/logs/', log_file)
    path = os.path.join('image_analyzer/logs/', log_file)
    truncate_utf8_chars(path, count=1)  # remove last ']' symbol not to load full json file to memory

    with open(path, mode='a') as file:
        if not first_record:
            file.write(', ')
        file.write(json.dumps(result))
        file.write(']')  # Complete json array


def log_upload_image(user_ip, saved_image):
    """
    Log upload image request
    :param user_ip: str -> user' ip (version 4)
    :param saved_image: ImageHolder -> instance of Model class containing info about uploaded image
    :return: None
    """
    log_request(user_ip, operation='UPLOAD_NEW_IMAGE',
                image=str(saved_image.image), upload_date=str(saved_image.upload_date))


def log_count_hex(user_ip, hex_color, image_path):
    """
    Log upload image request
    :param user_ip: str -> user' ip (version 4)
    :param hex_color: str -> requested color in HEX format
    :param image_path: str ->
    :return: None
    """
    log_request(user_ip, operation='GET_HEX_COUNT',
                hex_color=hex_color, image=image_path)