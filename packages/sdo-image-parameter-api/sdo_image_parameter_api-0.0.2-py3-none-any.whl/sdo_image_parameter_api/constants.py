# Constant arguments

def get_const(name) -> list:
    """
    This method retrieves the values for a given constant group in a list form

    :param name: the class name of constant group to return. Value can be
    Format, Size, InfoType, Wave, Url, Param, or Const

    :return: list of values for each variable in a constant group
    """

    variables = vars(name)
    return [variables[key] for key in variables.keys() if key[0:2] != '__']


class Format:
    """
    This class defines the formats which information can be returned in.
    """

    JPEG = 'JPEG'
    XML = 'XML'
    JSON = 'JSON'


class InfoType:
    """
    This class defines the types of information that can be retrieved.
    """

    AIA = 'aia'
    PARAM = 'param'
    RANGE = 'range'
    HEADER = 'header'


class Wave:
    """
    This class defines the allowed wavelengths for each image
    """

    WAVE_94 = '94'
    WAVE_131 = '131'
    WAVE_171 = '171'
    WAVE_193 = '193'
    WAVE_211 = '211'
    WAVE_304 = '304'
    WAVE_355 = '355'
    WAVE_1600 = '1600'
    WAVE_1700 = '1700'


class Size:
    """
    This class defines the allowed sizes for each image.
    """
    SIZE_2K = '2k'
    SIZE_512 = '512'
    SIZE_256 = '256'


class Url:
    """
    This class defines the URL templates for retrieving image information.
    """

    AIA_JPEG = 'http://dmlab.cs.gsu.edu/dmlabapi/images/SDO/AIA/{}/?wave={' \
               '}&starttime={}'
    AIA_PARAM_JPEG = 'http://dmlab.cs.gsu.edu/dmlabapi/images/SDO/AIA/param' \
                     '/64/{}/?wave={}&starttime={}&param={}'
    AIA_PARAM_XML = 'http://dmlab.cs.gsu.edu/dmlabapi/params/SDO/AIA/64/full' \
                    '/?wave={}&starttime={}'
    AIA_PARAM_JSON = 'http://dmlab.cs.gsu.edu/dmlabapi/params/SDO/AIA/json/64' \
                     '/full/?wave={}&starttime={}'
    AIA_RANGE_XML = 'http://dmlab.cs.gsu.edu/dmlabapi/params/SDO/AIA/64/full' \
                    '/range/?wave={}&starttime={}&endtime={}&limit={' \
                    '}&offset={}&step={}'
    AIA_RANGE_JSON = 'http://dmlab.cs.gsu.edu/dmlabapi/params/SDO/AIA/json/64' \
                     '/full/range/?wave={}&starttime={}&endtime={}&limit={' \
                     '}&offset={}&step={}'
    AIA_HEADER_XML = 'http://dmlab.cs.gsu.edu/dmlabapi/header/SDO/AIA/xml' \
                     '/?wave={}&starttime={}'
    AIA_HEADER_JSON = 'http://dmlab.cs.gsu.edu/dmlabapi/header/SDO/AIA/json' \
                      '/?wave={}&starttime={}'


class Param:
    """
    This class defines the IDs of the ten image parameters computed over each
    image.
    """

    ENTROPY = 1
    MEAN = 2
    ST_DEVIATION = 3
    FRACTAL_DIMENSION = 4
    SKEWNESS = 5
    KURTOSIS = 6
    UNIFORMITY = 7
    RELATIVE_SMOOTHNESS = 8
    TAMURA_CONTRAST = 9
    TAMURA_DIRECTIONALITY = 10


class Const:
    """
    This class defines constant variables.
    """

    DATE_TIME = '%Y-%m-%dT%H:%M:%S'
