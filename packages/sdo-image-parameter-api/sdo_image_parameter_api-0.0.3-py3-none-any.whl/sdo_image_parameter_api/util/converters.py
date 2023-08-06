import numpy as np
from xml.etree import ElementTree as elemTree


def convert_xml_to_ndarray(xml_content: elemTree.Element) -> np.ndarray:
    """
    converts the content of a retrieved XML file into a `numpy.ndarray` type.
    The output dimension is 64 X 64 X 10 which is a data cube with 10 matrix
    for one image, each matrix for one image parameter.

    :param xml_content: the content of the xml file
    :return: a numpy array that is 64 x 64 x 10
    """
    mat = np.zeros((64, 64, 10))
    for cell in xml_content:
        x = int(cell[0].text)
        y = int(cell[1].text)
        z = 0
        for i in range(2, 12):
            mat[x][y][z] = float(cell[i].text)
            z = z + 1

    return mat


def convert_xml_range_to_ndarray(xml_content: elemTree.Element, length: int) \
        -> np.ndarray:
    """
    converts the content of a retrieved XML file into a `numpy.ndarray` type.
    The output dimension is length * 64 X 64 X 10 which is a data cube(?)
    with 10 matrix for one image, each matrix for one image parameter.

    :param xml_content: the content of the xml file
    :param length: the length of the xml_content file
    :return: a numpy array that is length x 64 x 64 x 10
    """

    mat = np.zeros((length, 64, 64, 10))

    for i in range(0, length):
        group = xml_content[i]
        for j in range(1, len(group)):
            cell = group[j]
            x = int(cell[0].text)
            y = int(cell[1].text)
            z = 0
            for k in range(2, 12):
                mat[i][x][y][z] = float(cell[k].text)
                z = z + 1
    return mat


def convert_xml_header_to_dict(xml_content: elemTree.Element) -> dict:
    """
    converts the content of a retrieved XML file into a `dict` type. The
    output is a dictionary with information types as keys, and information
    parameters as values.

    :param xml_content: the content of the xml file
    :return: a dictionary
    """
    d = {}
    for child in xml_content:
        d[child.tag] = np.double(child.text)
    return d
