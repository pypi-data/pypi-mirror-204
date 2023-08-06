from PIL import Image as PIL_Image
from io import BytesIO
import requests
from .util.converters import *
from .util.validators import *


# accessor methods

def get_img_jpeg(info_type: InfoType,
                 wave: Wave,
                 st_time: Union[str, datetime],
                 size: Size,
                 param: Param = None) -> PIL_Image:
    """
    retrieves an AIA image or a parameter image depending on info_type.

    info_type, wave, st_time, and size are all required arguments. If
    info_type is 'PARAM', then the param argument is required as well.

    :param info_type: the type of information to return: Allowed inputs are
    InfoType.X with X being 'AIA' or 'PARAM'.

    :param wave: the wavelength channel of the image. Value is wavelength
    retrieved from constants.Wave class. Allowed inputs are Wave.WAVE_# with #
    being '94', '131', '171', '193', '211', '304', '355', '1600', or '1700'

    :param st_time: the start time corresponding to the image. Allowed input
    is of type string or datetime with 'YYYY-MM-DDThh:mm:ss' format

    :param size: the size of the image. Value is size retrieved
    from the constants.Size class. Allowed inputs are Size.SIZE_# with # being
    '2k', '512', '256'

    :param param: (only for PARAM image). the image parameter. Value is
    parameter index retrieved from the constants.Param class. Allowed inputs
    are Param.X with X being 'ENTROPY', 'MEAN', 'ST_DEVIATION',
    'FRACTAL_DIMENSION', 'SKEWNESS', 'KURTOSIS', 'UNIFORMITY',
    'RELATIVE_SMOOTHNESS', 'TAMURA_CONTRAST', or 'TAMURA_DIRECTIONALITY'

    :return: a JPEG image as PIL.Image object
    """
    if info_type == 'aia':
        return __get_img_jpeg(size, wave, st_time)
    elif info_type == 'param':
        return __get_img_param_jpeg(size, wave, st_time, param)
    else:
        raise ValueError("Invalid info_type. Please choose 'AIA' or 'PARAM' "
                         "as the info_type.")


def get_img_param(data_format: Format,
                  wave: Wave,
                  st_time: Union[str, datetime]) \
        -> Union[elemTree.Element, list]:
    """
    retrieves an XML or JSON parameter image depending on data_format.

    data_format, wave, and st_time, are all required arguments.

    :param data_format: the type of image to return. Allowed inputs are
    Format.X with X being 'XML' or 'JSON'.

    :param wave: the wavelength channel of the image. Value is wavelength
    retrieved from constants.Wave class. Allowed inputs are Wave.WAVE_# with #
    being '94', '131', '171', '193', '211', '304', '355', '1600', or '1700'

    :param st_time: the start time corresponding to the image. Allowed input
    is of type string or datetime with 'YYYY-MM-DDThh:mm:ss' format

    :return: an `xml.etree.ElementTree.Element` or a list of dictionaries
    """

    if data_format == 'XML':
        return __get_img_param_xml(wave, st_time)
    elif data_format == 'JSON':
        return __get_img_param_json(wave, st_time)
    else:
        raise ValueError("Invalid data_format. Please choose 'XML' or "
                         "'JSON' as the data_format.")


def get_img_param_range(data_format: Format,
                        wave: Wave,
                        st_time: Union[str, datetime],
                        en_time: Union[str, datetime],
                        limit: int = 100,
                        offset: int = 0,
                        step: int = 1) -> Union[elemTree.Element, list]:
    """
    retrieves XML or JSON parameter range of images depending on data_format.

    data_format, wave, st_time, and en_time are all required arguments.
    limit, offset, and step are optional arguments.

    :param data_format: the type of image to return. Allowed inputs are
    Format.X with X being 'JPEG', 'XML', or 'JSON'.

    :param wave: the wavelength channel of the image. Value is wavelength
    retrieved from constants.Wave class. Allowed inputs are Wave.WAVE_# with #
    being '94', '131', '171', '193', '211', '304', '355', '1600', or '1700'

    :param st_time: the start time corresponding to the image. Allowed input
    is of type string or datetime with 'YYYY-MM-DDThh:mm:ss' format

    :param en_time: optional. the end time corresponding to the image.
    Allowed input is of type string or datetime with 'YYYY-MM-DDThh:mm:ss'
    format

    :param limit: optional. the maximum number of images returned in one
    request (default is 100). Input is of type int

    :param offset: optional. the offset in number from the start of the list
    of results that meet the requirements passed into the method. Used to
    perform paging when used in conjunction with limit (default is 0). Input
    is of type int

    :param step: optional. determines the index of which image to return (
    default is 1). Input is of type int

    :return: an `xml.etree.ElementTree.Element` or a list of dictionaries
    """

    if data_format == 'XML':
        return __get_img_param_range_xml(wave, st_time, en_time, limit,
                                         offset, step)
    elif data_format == 'JSON':
        return __get_img_param_range_json(wave, st_time, en_time, limit,
                                          offset, step)
    else:
        raise ValueError("Invalid data_format. Please choose 'XML' or "
                         "'JSON' as the data_format.")


def get_img_header(data_format: Format,
                   wave: Wave,
                   st_time: Union[str, datetime]) \
        -> Union[elemTree.Element, list]:
    """
    retrieves image header information as XML or JSON depending on data_format.

    data_format, wave, and st_time, are all required arguments.

    :param data_format: the type of image to return. Allowed inputs are
    Format.X with X being 'XML' or 'JSON'.

    :param wave: the wavelength channel of the image. Value is wavelength
    retrieved from constants.Wave class. Allowed inputs are Wave.WAVE_# with #
    being '94', '131', '171', '193', '211', '304', '355', '1600', or '1700'

    :param st_time: the start time corresponding to the image. Allowed input
    is of type string or datetime with 'YYYY-MM-DDThh:mm:ss' format

    :return: an `xml.etree.ElementTree.Element` or a dictionary
    """

    if data_format == 'XML':
        return __get_img_header_xml(wave, st_time)
    elif data_format == 'JSON':
        return __get_img_header_json(wave, st_time)
    else:
        raise ValueError("Invalid data_format. Please choose 'XML' or "
                         "'JSON' as the data_format.")


# methods used for retrieving the image data

def __get_img_jpeg(size: Size,
                   wave: Wave,
                   st_time: (str, datetime)) -> PIL_Image:
    """
    queries the AIA image corresponding to the given start time, 
    wave channel, and size.

    :param size: the size of the image. Value is size retrieved
    from the constants.Size class. Allowed inputs are Size.SIZE_# with # being
    '2k', '512', '256'
    :param wave: the wavelength channel of the image. Value is wavelength
    retrieved from constants.Wave class. Allowed inputs are Wave.WAVE_# with #
    being '94', '131', '171', '193', '211', '304', '355', '1600', or '1700'
    :param st_time: the start time corresponding to the image. Allowed input
    is of type string or datetime with 'YYYY-MM-DDThh:mm:ss' format

    
    :return: the JPEG AIA image as a PIL.Image object
    """

    size = validate_size(size)
    wave = validate_wave(wave)
    st_time = format_time(st_time)

    url = Url.AIA_JPEG.format(size, wave, st_time)
    response = requests.get(url)
    img = PIL_Image.open(BytesIO(response.content))
    return img


def __get_img_param_jpeg(size: Size,
                         wave: Wave,
                         st_time: (str, datetime),
                         param: Param) -> PIL_Image:
    """
    queries the AIA image corresponding to the given start time, 
    wave channel, and SIZE.

    :param size: optional. the size of the image. Value is size retrieved
    from the constants.Size class. Allowed inputs are Size.SIZE_# with # being
    '2k', '512', '256'
    :param wave: the wavelength channel of the image. Value is wavelength
    retrieved from constants.Wave class. Allowed inputs are Wave.WAVE_# with #
    being '94', '131', '171', '193', '211', '304', '355', '1600', or '1700'
    :param st_time: the start time corresponding to the image. Allowed input
    is of type string or datetime with 'YYYY-MM-DDThh:mm:ss' format
    :param param: the image parameter. Value is parameter index
    retrieved from the constants.Param class. Allowed inputs are Param.X
    with X being 'ENTROPY', 'MEAN', 'ST_DEVIATION', 'FRACTAL_DIMENSION',
    'SKEWNESS', 'KURTOSIS', 'UNIFORMITY', 'RELATIVE_SMOOTHNESS',
    'TAMURA_CONTRAST', or 'TAMURA_DIRECTIONALITY'
    
    :return: the JPEG heatmap of the given image parameter as a PIL.Image object
    """

    size = validate_size(size)
    wave = validate_wave(wave)
    st_time = format_time(st_time)
    param = validate_param(param)

    url = Url.AIA_PARAM_JPEG.format(size, wave, st_time, param)
    response = requests.get(url)
    img = PIL_Image.open(BytesIO(response.content))
    return img


def __get_img_param_xml(wave: Wave,
                        st_time: (str, datetime)) -> elemTree:
    """
    queries the XML of 10 image parameters computed on the image corresponding
    to the given date and wavelength channel.

    Note: Use `convert_xml_to_ndarray` to convert the retrieved XML into a 
    `numpy.ndarray` object.

    :param wave: the wavelength channel of the image. Value is wavelength
    retrieved from constants.Wave class. Allowed inputs are Wave.WAVE_# with #
    being '94', '131', '171', '193', '211', '304', '355', '1600', or '1700'
    :param st_time: the start time corresponding to the image. Allowed input
    is of type string or datetime with 'YYYY-MM-DDThh:mm:ss' format
    
    :return: an `xml.etree.ElementTree.Element` instance, as the content of the
    retrieved XML.
    """

    wave = validate_wave(wave)
    st_time = format_time(st_time)

    url = Url.AIA_PARAM_XML.format(wave, st_time)
    response = requests.get(url)
    xml = elemTree.fromstring(response.content)
    return xml


def __get_img_param_json(wave: Wave,
                         st_time: (str, datetime)) -> list:
    """
    queries the JSON of 10 image parameters computed on the image corresponding
    to the given date and wavelength channel.

    :param wave: the wavelength channel of the image. Value is wavelength
    retrieved from constants.Wave class. Allowed inputs are Wave.WAVE_# with #
    being '94', '131', '171', '193', '211', '304', '355', '1600', or '1700'
    :param st_time: the start time corresponding to the image. Allowed input
    is of type string or datetime with 'YYYY-MM-DDThh:mm:ss' format
    
    :return: a list of dictionaries, as the content of the retrieved JSON file
    """
    wave = validate_wave(wave)
    st_time = format_time(st_time)

    url = Url.AIA_PARAM_JSON.format(wave, st_time)
    response = requests.get(url)
    js = response.json()
    return js


def __get_img_param_range_xml(wave: Wave,
                              st_time: (str, datetime),
                              en_time: (str, datetime),
                              limit: int = 100,
                              offset: int = 0,
                              step: int = 1) -> elemTree:
    """
    queries the XML of a range of image parameters computed on the image 
    corresponding to the given date and wavelength channel. optional 
    arguments include limit, offset, and step.

    :param wave: the wavelength channel of the image. Value is wavelength
    retrieved from constants.Wave class. Allowed inputs are Wave.WAVE_# with #
    being '94', '131', '171', '193', '211', '304', '355', '1600', or '1700'
    :param st_time: the start time corresponding to the image. Allowed input
    is of type string or datetime with 'YYYY-MM-DDThh:mm:ss' format
    :param en_time: optional. the end time corresponding to the image.
    Allowed input is of type string or datetime with 'YYYY-MM-DDThh:mm:ss'
    format
    :param limit: the maximum number of images returned in one request (
    default is 100)
    :param offset: the offset in number from the start of the list of results
    that meet the requirements passed into
    the method.
    Used to perform paging when used in conjunction with limit (default is 0)
    :param step: determines the index of which image to return (default is 1)
    :return: an `xml.etree.ElementTree.Element` instance, as the content of the
    retrieved XML.
    """
    wave = validate_wave(wave)
    st_time = format_time(st_time)
    en_time = format_time(en_time)

    if isinstance(limit, int) and isinstance(offset, int) and isinstance(
            step, int):
        url = Url.AIA_RANGE_XML.format(wave, st_time, en_time, limit, offset,
                                       step)
        response = requests.get(url)
        xml = elemTree.fromstring(response.content)
        return xml


def __get_img_param_range_json(wave: Wave,
                               st_time: (str, datetime),
                               en_time: (str, datetime),
                               limit: int = 100,
                               offset: int = 0,
                               step: int = 1) -> list:
    """
    queries the JSON of a range of image parameters computed on the image
    corresponding to the given date and wavelength channel. optional
    arguments include limit, offset, and step.

    :param wave: the wavelength channel of the image. Value is wavelength
    retrieved from constants.Wave class. Allowed inputs are Wave.WAVE_# with #
    being '94', '131', '171', '193', '211', '304', '355', '1600', or '1700'
    :param st_time: the start time corresponding to the image. Allowed input
    is of type string or datetime with 'YYYY-MM-DDThh:mm:ss' format
    :param en_time: optional. the end time corresponding to the image.
    Allowed input is of type string or datetime with 'YYYY-MM-DDThh:mm:ss'
    format
    :param limit: the maximum number of images returned in one request (
    default is 100)
    :param offset: the offset in number from the start of the list of results
    that meet the requirements passed into the method. Used to perform paging
    when used in conjunction with limit (default is 0)
    :param step: determines the index of which image to return (default is 1)
    :return: a list of dictionaries, as the content of the retrieved JSON file
    """
    wave = validate_wave(wave)
    st_time = format_time(st_time)
    en_time = format_time(en_time)

    if isinstance(limit, int) and isinstance(offset, int) and isinstance(
            step, int):
        url = Url.AIA_RANGE_JSON.format(wave, st_time, en_time, limit,
                                        offset, step)
        response = requests.get(url)
        js = response.json()
        return js


def __get_img_header_xml(wave: Wave,
                         st_time: (str, datetime)) -> elemTree:
    """
    queries the XML of the image header information corresponding to the given
    wavelength and start time

    :param wave: the wavelength channel of the image. Value is wavelength
    retrieved from constants.Wave class. Allowed inputs are Wave.WAVE_# with #
    being '94', '131', '171', '193', '211', '304', '355', '1600', or '1700'
    :param st_time: the start time corresponding to the image. Allowed input
    is of type string or datetime with 'YYYY-MM-DDThh:mm:ss' format

    :return: an `xml.etree.ElementTree.Element` instance, as the content of the
    retrieved XML.
    """

    wave = validate_wave(wave)
    st_time = format_time(st_time)

    url = Url.AIA_HEADER_XML.format(wave, st_time)
    response = requests.get(url)
    xml = elemTree.fromstring(response.content)
    return xml


def __get_img_header_json(wave: Wave,
                          st_time: (str, datetime)) -> list:
    """
    queries the JSON of the image header information corresponding to the given
    wavelength and start time

    :param wave: the wavelength channel of the image. Value is wavelength
    retrieved from constants.Wave class. Allowed inputs are Wave.WAVE_# with #
    being '94', '131', '171', '193', '211', '304', '355', '1600', or '1700'
    :param st_time: the start time corresponding to the image. Allowed input
    is of type string or datetime with 'YYYY-MM-DDThh:mm:ss' format

    :return: a dictionary with the content of the retrieved JSON file
    """
    wave = validate_wave(wave)
    st_time = format_time(st_time)

    url = Url.AIA_HEADER_JSON.format(wave, st_time)
    response = requests.get(url)
    js = response.json()
    return js
