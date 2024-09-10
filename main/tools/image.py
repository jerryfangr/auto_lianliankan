import os

import cv2
import numpy as np

from config import setting as SETTING
from tools.logger import log_print

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def is_pure_color_image(image: str, threshold=5) -> bool:
    """
    Determine whether an image is considered as a pure color or gradient color image.
    A pure or gradient color image has very little variation in pixel values.

    Args:
        image - the input image as a numpy array
        threshold - the standard deviation threshold to determine if it's a pure/gradient color image

    Returns:
        True if the image is considered a pure or gradient color image, False otherwise
    """
    # Compute the standard deviation of the pixel values
    std_devs = np.std(image, axis=(0, 1))

    # If the standard deviation of any channel is below the threshold, it's considered a pure/gradient color image
    return np.all(std_devs < threshold)


def ORB_img_similarity(img1: 'np.uint8|str', img2: 'np.uint8|str', img_type='data'):
    """
    Calculate the similarity of two images using ORB algorithm
    args:
        img1 - the first image
        img2 - the second image
        img_type - the type of img1 and img2, 'data' or 'path'
    return:
        (float) - the similarity of two images 0 - 1
    """

    # read image path to np.uint8
    if img_type == 'path':
        # img1 = cv2.imread(img1, cv2.IMREAD_GRAYSCALE)
        img1 = cv2.imread(img1)
        img2 = cv2.imread(img2)

    # if all pixels are 0, means two images are same.
    if not np.any(np.subtract(img1, img2)):
        return 1
    
    is_img1_pure = is_pure_color_image(img1)
    is_img2_pure = is_pure_color_image(img2)

    if is_img1_pure and is_img2_pure:
        return 1

    if (is_img1_pure and not is_img2_pure) or (not is_img1_pure and is_img2_pure):
        return 0

    # initialize ORB detector
    orb = cv2.ORB_create(fastThreshold=1, edgeThreshold=0)
    # find the key points and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    if des1 is None and des2 is None:
        return 1

    if (des1 is None and des2 is not None) or (des1 is not None and des2 is None):
        return 0

    # extract and compute the feature points
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    # knn filter result
    matches = bf.knnMatch(des1, trainDescriptors=des2, k=2)

    if len(matches) == 0 or len(matches[0]) <= 1:
        return 0

    # ratio test as per Lowe's paper
    good = [m for (m, n) in matches if m.distance < 0.75 * n.distance]
    similarly = len(good) / len(matches)

    return similarly


def split_items(screen_image: 'np.uint8', game_pos: 'tuple', save_image=False):
    """
    Split the items from screen image
    args:
        screen_image - the screenshot of the screen
        game_pos - the position of the game area
    return:
        items - the list of the items (numpy array)
    """

    log_print('Splitting the item from screen image...', 'info')
    
    # get the position of the game area
    game_x = game_pos[0] + SETTING.MARGIN_LEFT
    game_y = game_pos[1] + SETTING.MARGIN_TOP

    # split the number of the horizontal and vertical items
    items = []
    for x in range(0, SETTING.HORIZONTAL_NUM):
        for y in range(0, SETTING.VERTICAL_NUM):
            # split the item
            item = screen_image[
                (game_y + y * SETTING.ITEM_HEIGHT) : (game_y + (y+1) * SETTING.ITEM_HEIGHT), 
                (game_x + x * SETTING.ITEM_WIDTH)  : (game_x + (x+1) * SETTING.ITEM_WIDTH)
            ]
            items.append(item)

    # cut the noise area
    cut_items = [item[SETTING.SUB_LT_Y:SETTING.SUB_RB_Y, SETTING.SUB_LT_X:SETTING.SUB_RB_X] for item in items]
    if save_image:
        for i, item in enumerate(cut_items):
            cv2.imwrite(os.path.join(PROJECT_PATH, 'temp', 'item_{}.png'.format(i)), item)
    return cut_items


BLOCK_IMGS, EMPTY_IMGS = [], []

for img_path in SETTING.BLOCK_IMAGE_PATH:
    BLOCK_IMGS.append(cv2.imread(os.path.join(PROJECT_PATH, img_path)))

for img_path in SETTING.EMPTY_IMAGE_PATH:
    EMPTY_IMGS.append(cv2.imread(os.path.join(PROJECT_PATH, img_path)))


def has_image_data(img, img_list):
    """
    Check if the image is exist in the list
    args:
        img - the image to be checked
        img_list - the list of the images
    return:
        (bool) - True if the image is exist in the list
    """
    for i in img_list:
        if np.array_equal(i, img):
            return True
    return False


def is_image_exist(img: 'np.uint8', img_list: 'list'):
    """
    Check if the similarity of the image is exist in the list
    args:
        img - the image to be checked
        img_list - the list of the images
    return:
        (bool) - True if the image is exist in the list
    """
    for exist_img in img_list:
        sm = ORB_img_similarity(img, exist_img)
        if sm > 0.35:
            return True
        else:
            continue
    return False


def unique_images(images: 'list', save_image=False):
    """
    Calculate the unique images from the list
    args:
        images - the list of the images
    return:
        uq_imgs - the list of the unique images
    """

    log_print("Calculate unique images", "info")
    uq_imgs = []

    # add empty images
    for empty_img in EMPTY_IMGS:
        uq_imgs.append(empty_img)

    for block_img in BLOCK_IMGS:
        uq_imgs.append(block_img)

    for img in images:
        if not is_image_exist(img, uq_imgs):
            uq_imgs.append(img)

    if save_image:
        for i, item in enumerate(uq_imgs):
            cv2.imwrite(os.path.join(PROJECT_PATH, 'temp', 'type_{}.png'.format(i)), item)

    return uq_imgs


def images_to_number_type(image_list: 'list', type_images: 'list', wrapper=None):
    """
    Calculate the number type of the images
    args:
        image_list - the list of the images
        unique_images - the list of the unique images of the image_list
        wrapper - wrap the image_number_type with the wrapper
    return:
        image_number_type - the list of the number type of the images
    """

    image_number_type = []
    line = [wrapper] if wrapper is not None else []
    if wrapper is not None:
        image_number_type.append([wrapper for i in range(SETTING.VERTICAL_NUM + 2)])

    # calculate the number type of the images(the number type is the index of the unique images)
    for item_index, item_img in enumerate(image_list):
        for type_index, type_img in enumerate(type_images):
            sm = ORB_img_similarity(type_img, item_img)
            # print(item_index,  '-m->', type_index, '=', sm)
            if sm >= 0.35:
                if type_index < len(EMPTY_IMGS):
                    line.append(SETTING.EMPTY_TYPE_NUMBER)
                elif type_index >= len(EMPTY_IMGS) and type_index < (len(EMPTY_IMGS)+len(BLOCK_IMGS)):
                    line.append(SETTING.BLOCK_TYPE_NUMBER)
                else:
                    line.append(type_index)
                break

        if (wrapper is not None and len(line) == SETTING.VERTICAL_NUM + 1) or (wrapper is None and len(line) == SETTING.VERTICAL_NUM):
            if wrapper is not None:
                line.append(wrapper)
            image_number_type.append(line)
            line = [wrapper] if wrapper is not None else []

    if wrapper is not None:
        image_number_type.append([wrapper for i in range(SETTING.VERTICAL_NUM + 2)])

    return image_number_type
