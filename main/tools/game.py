import copy
from time import sleep

from config import setting as SETTING
from tools.logger import log_print
from tools.screen import click_screen
from tools.match import check_can_link


def calculate_clean_position(type_matrix, game_x: 'int', game_y: 'int'):
    """
    calculate the position of the item witch can be linked
    """
    cx, cy = SETTING.FINAL_WIDTH/2, SETTING.FINAL_HEIGHT/2
    start = 1 if SETTING.ALLOW_OUTSIDE_LINK else 0
    endSub = 1 if SETTING.ALLOW_OUTSIDE_LINK else 0
    clean_position = []
    for i in range(start, len(type_matrix) - endSub):
        for j in range(start, len(type_matrix[i]) - endSub):
            if type_matrix[i][j] != 0:
                # find the same type item
                for m in range(0, len(type_matrix)):
                    for n in range(0, len(type_matrix[0])):
                        if type_matrix[m][n] != 0 and type_matrix[m][n] != SETTING.BLOCK_TYPE_NUMBER:
                            if check_can_link(i, j, m, n, type_matrix):
                                type_matrix[i][j] = 0
                                type_matrix[m][n] = 0
                                x1 = game_x + (j - start) * SETTING.ITEM_WIDTH
                                y1 = game_y + (i - start) * SETTING.ITEM_HEIGHT
                                x2 = game_x + (n - start) * SETTING.ITEM_WIDTH
                                y2 = game_y + (m - start) * SETTING.ITEM_HEIGHT
                                clean_position.append((x1 + cx, y1 + cy))
                                clean_position.append((x2 + cx, y2 + cy))
                                clean_position.append('({},{}) <-> ({},{})'.format(i+1-start, j+1-start, m+1-start, n+1-start))

                                return clean_position
    return clean_position


def calculate_position_list(type_matrix, game_x: 'int', game_y: 'int', max_clean_count: 'int'):
    count = 0
    clean_position = calculate_clean_position(type_matrix, game_x, game_y)
    clean_position_list = []
    # if there are clean item, append position
    while len(clean_position) > 0:
        clean_position_list.append(clean_position)
        count += 1

        # if got enough clean items, break the loop
        if max_clean_count > 0 and count >= max_clean_count:
            break

        clean_position = calculate_clean_position(type_matrix, game_x, game_y)
    
    return clean_position_list


def get_block_index_List(type_matrix, condition_fun):
    block_list = []

    start = 1 if SETTING.ALLOW_OUTSIDE_LINK else 0
    endSub = 1 if SETTING.ALLOW_OUTSIDE_LINK else 0
    for i in range(start, len(type_matrix) - endSub):
        for j in range(start, len(type_matrix[i]) - endSub):
            if condition_fun(type_matrix[i][j]):
                block_list.append((i, j))
    
    return block_list


def clean_items(type_matrix, game_position: 'tuple', fake_click: 'bool' = False, max_clean_count: 'int' = -1, min_clean_count: 'int' = -1):
    '''
    clean the item
    '''
    game_x = game_position[0] + SETTING.MARGIN_LEFT
    game_y = game_position[1] + SETTING.MARGIN_TOP

    clean_position_list = calculate_position_list(copy.deepcopy(type_matrix), game_x, game_y, max_clean_count)
    block_index_List = get_block_index_List(type_matrix, lambda x: x == SETTING.BLOCK_TYPE_NUMBER )
    log_print('Get all clean items: ' + str(len(clean_position_list)) + ' || Least need: ' + str(min_clean_count))

    # if there no enough clean item
    if len(clean_position_list) < min_clean_count:
        
        # check clean item, after delete block
        for block_index in block_index_List:
            col,cum = block_index

            origin_type = type_matrix[col][cum]

            type_matrix[col][cum] = SETTING.EMPTY_TYPE_NUMBER
            clean_position_list = calculate_position_list(copy.deepcopy(type_matrix), game_x, game_y, max_clean_count)
            
            # recover block
            type_matrix[col][cum] = origin_type

            if len(clean_position_list) >= min_clean_count:
                break
        
        if len(clean_position_list) >= min_clean_count:
            bias = 0 if SETTING.ALLOW_OUTSIDE_LINK else -1
            log_print('Clean item: you should delete block ({},{})'.format(cum+bias, col+bias))

        else:
            log_print('Clean item: Noway to clean, please retry')
    
    # start clean item
    else:
        for clean_position in clean_position_list:
            [item1_position, item2_position, description] = clean_position
            
            if fake_click is False:
                click_screen(item1_position[0], item1_position[1], 0.08)
                click_screen(item2_position[0], item2_position[1], 0.08)
            
            sleep(SETTING.CLEAN_INTERVAL)
            
            log_print('Clean item: ' + description + ' Done')

    # move cursor back to run position
    click_screen(SETTING.RUN_POSITION[0], SETTING.RUN_POSITION[1], 0.08)


