import time

import numpy as np

from config import setting as SETTING
from tools.logger import log_print
from tools.screen import set_run_position, get_window_position, get_screen_image
from tools.image import split_items, unique_images, images_to_number_type
from tools.game import clean_items
from ck_model.predict import load_model

if __name__ == '__main__':
    SETTING.DEBUG_MODE = True

    log_print('main auto_lianliankan start at ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    load_model()
    log_print('[Ctrl + C] to exit, Enter any [number] to start')
    set_run_position()

    round = 0
    while True:
        input_val = input('round(0-4): ')
        if input_val == 'e':
            break
        if input_val == 'a':
            round = 9
        else:
            round = int(input_val or round)
            round = 4 if round > 4 else round

        log_print('-----------> round {} start <-----------'.format(round))
        # get game window position
        game_position = get_window_position(SETTING.WINDOW_TITLE, SETTING.DEBUG_MODE)
        # get screen image
        screen_image = get_screen_image('screen_round_{}'.format(round), 'read' if SETTING.DEBUG_MODE else None)
        # split items image from screen image
        game_item_images = split_items(screen_image, game_position, save_image=SETTING.DEBUG_MODE)
        # get unique type images
        type_images = unique_images(game_item_images, save_image=SETTING.DEBUG_MODE)

        # map item image to type number(by type images index) then transpose the matrix
        wrapper = SETTING.EMPTY_TYPE_NUMBER if SETTING.ALLOW_OUTSIDE_LINK else None
        type_matrix = np.transpose(images_to_number_type(game_item_images, type_images, wrapper))

        log_print('type_matrix: \n' + str(type_matrix))

        # * auto click items to clean || 10 11 11 14 all
        # round 0, 1, 2, 3 / 4(final)
        if round == 0:
            clean_items(type_matrix, game_position, SETTING.DEBUG_MODE, max_clean_count=10, min_clean_count=10)
        elif round == 1 or round == 2:
            clean_items(type_matrix, game_position, SETTING.DEBUG_MODE, 11, 11)
        elif round == 3:
            clean_items(type_matrix, game_position, SETTING.DEBUG_MODE, 14, 14)
        elif round == 4:
            clean_items(type_matrix, game_position, SETTING.DEBUG_MODE, 20, 20)
        else:
            clean_items(type_matrix, game_position, SETTING.DEBUG_MODE, -1, -1)

        round += 1
