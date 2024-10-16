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
WINDOW_TITLE = "23127PN0CC"

# the interval of game click (seconds)
CLEAN_INTERVAL = 0.3

WINDOW_BAR = 30

# the MARGIN_LEFT of game area to the game window
MARGIN_LEFT = 58
# the MARGIN_TOP of game area to the game window + title bar
MARGIN_TOP = 251 + WINDOW_BAR

# STOP & CONTINUE BUTTON
STOP_BUTTON = (45, 68 + WINDOW_BAR)
CONTINUE_BUTTON = (300, 560 + WINDOW_BAR)

# the number of the item in the horizontal direction
HORIZONTAL_NUM = 6
# the number of the item in the vertical direction
VERTICAL_NUM = 8

# the size of the item 
ITEM_WIDTH = 54
ITEM_HEIGHT = 54

# cut the image noise, (LT)left top to (RB)right bottom
bx, by = 5, 5
SUB_LT_X = 3
SUB_LT_Y = 3
SUB_RB_X = ITEM_WIDTH - 2
SUB_RB_Y = ITEM_HEIGHT - 2

# the final width and height of the item，the final item is 55-6=49x49
FINAL_WIDTH = ITEM_WIDTH - bx
FINAL_HEIGHT = ITEM_HEIGHT - by

# ignore following value
RUN_POSITION = (100, 100)
