import time
import numpy as np
from tools.logger import log_print
from config import setting as SETTING
from tools.screen import get_window_position, get_screen_image
from tools.image import split_items, unique_images, images_to_number_type
from tools.game import clean_items

if __name__ == '__main__':
    log_print('main auto_lianliankan start at ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    # get game window position
    game_position = get_window_position(SETTING.WINDOW_TITLE)

    # get screen image
    screen_image = get_screen_image()

    # split items image from screen image
    game_item_images = split_items(screen_image, game_position, save_image=False)

    # get unique type images
    type_images = unique_images(game_item_images)

    # map item image to type number(by type images index) then transpose the matrix
    wrapper = 0 if SETTING.ALLOW_OUTSIDE_LINK else None
    type_matrix = np.transpose(images_to_number_type(game_item_images, type_images, wrapper))

    log_print('type_matrix: \n' + str(type_matrix))

    # auto click items to clean items 11 11 14 all
    # round 1, 2, 3
    # clean_items(type_matrix, game_position, False, max_clean_count=14)

    # round 4(final)
    clean_items(type_matrix, game_position, False)
