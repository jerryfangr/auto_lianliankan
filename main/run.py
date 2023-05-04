import time
import numpy as np
from tools.logger import log_print
from config import setting as SETTING
from tools.screen import set_run_position, get_window_position, get_screen_image
from tools.image import split_items, unique_images, images_to_number_type
from tools.game import clean_items

if __name__ == '__main__':
    log_print('main auto_lianliankan start at ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    log_print('[Ctrl + C] to exit, Enter any [number] to start')
    set_run_position()

    round = int(input('round(0-4): ') or 0)
    round = 4 if round >= 5 else round
    for i in range(round, 5):
        log_print('-----------> round {} start <-----------'.format(i))
        # get game window position
        game_position = get_window_position(SETTING.WINDOW_TITLE)

        # get screen image
        screen_image = get_screen_image('screen_round_{}'.format(i), 'read' if SETTING.DEBUG_MODE else None)

        # split items image from screen image
        game_item_images = split_items(screen_image, game_position, save_image=False)

        # get unique type images
        type_images = unique_images(game_item_images)

        # map item image to type number(by type images index) then transpose the matrix
        wrapper = 0 if SETTING.ALLOW_OUTSIDE_LINK else None
        type_matrix = np.transpose(images_to_number_type(game_item_images, type_images, wrapper))

        log_print('type_matrix: \n' + str(type_matrix))

        # * auto click items to clean || 10 11 11 14 all
        # round 0, 1, 2, 3 / 4(final)
        if i == 0:
            clean_items(type_matrix, game_position, SETTING.DEBUG_MODE, max_clean_count=11, min_clean_count=10)
        elif i == 1 or i == 2:
            clean_items(type_matrix, game_position, SETTING.DEBUG_MODE, 12, 11)
        elif i == 3:
            clean_items(type_matrix, game_position, SETTING.DEBUG_MODE, 14, 14)
        else:
            clean_items(type_matrix, game_position, SETTING.DEBUG_MODE, -1, 20)

        if i < 4:
            input('Press [Enter] to next round || [Ctrl + C] to exit')
