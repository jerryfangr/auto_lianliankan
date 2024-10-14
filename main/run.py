import time

import numpy as np

from config import setting as SETTING
from tools.logger import log_print
from tools.screen import set_run_position, get_window_position, get_screen_image
from tools.image import split_items, unique_images, images_to_number_type
from tools.game import clean_items, stop_game
from ck_model.predict import load_model

if __name__ == '__main__':
    log_print('main auto_lianliankan start at ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    load_model()
    log_print('Input e or [Ctrl + C] to exit, Enter round [number] to start')
    set_run_position()

    round = 0
    while True:
        input_val = input('round(0-4): ')
        if input_val == 'e':
            break
        if input_val == 'a':
            round = -1
        else:
            round = int(input_val or round)
            round = 4 if round > 4 else round

        log_print('-----------> round {} start <-----------'.format(round))
        # get game window position
        game_position = get_window_position(SETTING.WINDOW_TITLE, SETTING.DEBUG_MODE)
        # get screen image
        screen_image = get_screen_image('screen_round_{}'.format(round))

        # stop game
        stop_game(game_position, True)

        # split items image from screen image
        game_item_images = split_items(screen_image, game_position, save_image=SETTING.DEBUG_MODE)
        # get unique type images
        type_images = unique_images(game_item_images, save_image=SETTING.DEBUG_MODE)

        # map item image to type number(by type images index) then transpose the matrix
        wrapper = SETTING.EMPTY_TYPE_NUMBER if SETTING.ALLOW_OUTSIDE_LINK else None
        type_matrix = np.transpose(images_to_number_type(game_item_images, type_images, wrapper))

        # continue game
        stop_game(game_position, False, 0.4)

        log_print('type_matrix: \n' + str(type_matrix))

        # dict to store round condition(0~4 / a)
        round_condition = [
            10, 11, 11, 14, 22,
            -1
        ]

        # * auto click items to clean
        clean_items(type_matrix, game_position, SETTING.DEBUG_MODE, max_clean_count=round_condition[round], min_clean_count=round_condition[round])
        round += 1

