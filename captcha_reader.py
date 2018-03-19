import numpy as np
from scipy.ndimage import gaussian_filter
from skimage import io
from os import remove
from statistics import mean
from skimage import filters
from pytesseract import *
from PIL import Image


def has_2_number(input_string):
    """
    Check if the string is composed of two digits

       Args:
        input_string (str): The string to parse

        Returns:
        bool: The return value. True for success, False otherwise.
       
    """
    num = 0
    for char in input_string:
        if char.isdigit():
            num += 1

    if num == 2:
        return True
    else:
        return False


def remove_lines(gray_img):
    """
    Scan the image and remove the lines for a cleaner image

       Args:
        gray_img (ndarray): The image object

        Returns:
        ndarray: The input object without the lines

    """
    size = len(gray_img)
    gray_img = np.array(gray_img)
    mean_value = gray_img.mean()
    for i in range(0, size):
        if mean(gray_img[i, :]) < 0.7:  # TODO: Instead of a static value use something better
            gray_img[i, :] = [mean_value] * size
    for j in range(0, size):
        if mean(gray_img[:, j]) < 0.7:
            gray_img[:, j] = [mean_value] * size
    return gray_img


def turn_to_img(bool_img):
    """
    Convert matrix of True/False in matrix of 1/0

       Args:
        bool_img (ndarray): The image array composed of True/False values

        Returns:
        ndarray: The image array composed of 1/0 values

    """
    num_img = np.zeros((60, 60))
    for i in range(1, len(bool_img)):
        for j in range(1, len(bool_img)):
            if bool_img[i][j]:
                num_img[i, j] = 1
            else:
                num_img[i, j] = 0
    return num_img


def clean_image_and_save(img, name='temp_img_cr.bmp'):
    """
    Opens the image and cleans it, saving the result in a new file

       Args:
        img (str): The path of the image to clean
        name (str): The name of the cleaned image file

        Returns:
        None

    """
    image = io.imread(img, as_grey=True)
    image = remove_lines(image)
    image = gaussian_filter(image, 1.2)
    val = filters.threshold_li(image)
    mask = image < val
    image = turn_to_img(mask)
    io.imsave(name, image)


def retrieve_number_from_bmp(ims='temp_img_cr.bmp'):
    """
    Open the cleaned image and try to detect the text inside

       Args:
        ims (str): The path of the image to clean

        Returns:
        str: The value in the image if found, empty otherwise

    """

    im = Image.open(ims)
    text = image_to_string(im)  # TODO: Use a custom neural network to improve capabilities
    if not has_2_number(text):
        for angle in range(-30, 30, 1):
            text = image_to_string(im.rotate(angle))
            if has_2_number(text):
                break
            else:
                text = ''
    return text


def read_captcha(path):
    clean_image_and_save(path)
    print "The image " + path + " is: " + retrieve_number_from_bmp()
    remove("temp_img_cr.bmp")


if __name__ == "__main__":
    import sys
    read_captcha(sys.argv[1])