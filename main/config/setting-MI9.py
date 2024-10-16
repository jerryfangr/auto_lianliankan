# -*- coding:utf-8 -*-
LOG_LEVEL = 1
DEBUG_MODE = False
TEMP_PATH = "temp"
CONFIG_PATH = "config"

# allow outside link
ALLOW_OUTSIDE_LINK = True

# image path of empty item
EMPTY_IMAGE_PATH = ["data/empty1.png"]
# image path of obstacles
BLOCK_IMAGE_PATH = ["data/block1.png"]

# the type number of block(>90)
BLOCK_TYPE_NUMBER = 90
EMPTY_TYPE_NUMBER = 0

# game window title
WINDOW_TITLE = "MI 9 Transparent Edition"

# the interval of game click (seconds)
CLEAN_INTERVAL = 0.3

WINDOW_BAR = 28

# the MARGIN_LEFT of game area to the game window
MARGIN_LEFT = 56
# the MARGIN_TOP of game area to the game window + title bar
MARGIN_TOP = 244 + WINDOW_BAR

# STOP & CONTINUE BUTTON
STOP_BUTTON = (45, 68 + WINDOW_BAR)
CONTINUE_BUTTON = (MARGIN_LEFT + 5, MARGIN_TOP + 5)

# the number of the item in the horizontal direction
HORIZONTAL_NUM = 6
# the number of the item in the vertical direction
VERTICAL_NUM = 8

# the size of the item 
ITEM_WIDTH = ITEM_HEIGHT = 55

# cut the image noise, (LT)left top to (RB)right bottom
bx, by = 6, 6
SUB_LT_X = bx
SUB_LT_Y = by
SUB_RB_X = ITEM_WIDTH + bx
SUB_RB_Y = ITEM_HEIGHT + by

# the final width and height of the item，the final item is 55-6=49x49
FINAL_WIDTH = ITEM_WIDTH - bx
FINAL_HEIGHT = ITEM_HEIGHT - by

# ignore following value
RUN_POSITION = (100, 100)
