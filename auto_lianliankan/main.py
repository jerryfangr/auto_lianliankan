import time
import numpy as np
from tools.logger import log_print
from config import setting as SETTING
from tools.screen import get_window_position, get_screen_image
from tools.image import split_items, unique_images, images_to_number_type
from tools.game import clean_items

if __name__ == '__main__':
    log_print('main auto_lianliankan start at ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    screen_image = get_screen_image()
    game_position = get_window_position(SETTING.WINDOW_TITLE)

    game_item_images = split_items(screen_image, game_position, save_image=False)

    type_images = unique_images(game_item_images)

    # transpose the matrix
    wrapper = 0 if SETTING.ALLOW_OUTSIDE_LINK else None
    type_matrix = np.transpose(images_to_number_type(game_item_images, type_images, wrapper))

    log_print('type_matrix: \n' + str(type_matrix))

    clean_items(type_matrix, game_position)
