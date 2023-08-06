from datetime import datetime
import re
from .constants import *
from typing import Union
import PIL.JpegImagePlugin as Img


def format_time(time: str) -> Union[None, str]:
    """
    validates and formats the time into a string that can be returned to a
    URL query

    :param time: the given time inputted as a string
    :return: the reformatted string version of the time
    """
    if isinstance(time, datetime):
        time = str(time).replace(" ", "T")
        return time
    elif isinstance(time, str):
        if re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{'
                                          '2}:[0-9]{2}:[0-9]{2}$', time):
            time = datetime.strptime(time, Const.DATE_TIME)
            time = time.strftime(Const.DATE_TIME)
            return time
        else:
            raise TypeError("Invalid time format. Must be in "
                             "'YYYY-MM-DDThh-mm-ss' format.")
    else:
        raise TypeError("Time should be of type string or datetime.")


def show_image(img: (None, Img.JpegImageFile)) -> None:
    """
    validates that inputted parameter exists as Image type before showing image.

    :param img: the input image; may be a None object
    :return: the image if it is valid, otherwise, error statement
    """

    if isinstance(img, Img.JpegImageFile):
        return img.show()
    else:
        raise TypeError("Invalid image format")


# Note, maybe validation here is unnecessary since directly calling an
# attribute that doesn't exist automatically returns an AttributeError before
# it reaches this validation function
def validate_size(size: Size) -> Union[None, Size]:
    """
    validates the inputted size of an image

    :param size: inputted Size parameter
    :return: the parameter if valid, otherwise, error statement
    """
    if size is None:
        raise TypeError("Size is a required parameter.")
    elif size in get_const(Size):
        return size
    else:
        raise ValueError("Invalid size parameter. Choose from options in "
                         "Constants module.")


def validate_wave(wave: Wave) -> Union[None, Wave]:
    """
    validates the inputted wave of an image

    :param wave: inputted wave parameter
    :return: the parameter if valid, otherwise, error statement
    """
    if wave is None:
        raise TypeError("Wave is a required parameter.")
    elif wave in get_const(Wave):
        return wave
    else:
        raise ValueError("Invalid wave parameter. Choose from options "
                         "in Constants module.")


def validate_param(param: Param) -> Union[None, Param]:
    """
    validates the inputted parameter as being of type string or int,
    and returns the appropriate parameter value from parameter dictionary in
    CONST Class.

    :param param: the inputted parameter value
    :return: a string of the parameter, or error if it's not an acceptable
    parameter
    """
    if param is None:
        raise TypeError("Param is a required parameter.")
    elif param in get_const(Param):
        return param
    else:
        raise ValueError("Invalid parameter. Choose from options in Constants "
                         "module.")
