import math
import os

import win32api, win32gui, win32con, win32com.client
import cv2
from PIL import ImageGrab
from time import sleep

from config import setting as SETTING
from tools.logger import log_print

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def set_run_position():
    """
    Set the run position
    args:
        None
    return:
        None
    """

    SETTING.RUN_POSITION = win32gui.GetCursorPos()
    log_print('Save Run position: %s' % str(SETTING.RUN_POSITION))


def get_screen_image(name='screen', type: 'str|None'=None):
    """
    Get the screenshot
    args:
        None
    return:
        image(numpy array) - the screenshot of the screen 
    """

    screen_path = os.path.join(PROJECT_PATH, SETTING.TEMP_PATH, name + '.png')

    if type != 'read':
        scim = ImageGrab.grab() 
        scim.save(screen_path)

    return cv2.imread(screen_path)


def get_window_position(window_title='', debug=False):
    """
    Get the window position
    args:
        window_title(string) - the text of window title bar 
    return:
        (x, y) - the position of the window
    """

    config_path = os.path.join(PROJECT_PATH, SETTING.CONFIG_PATH, 'tmp.txt')

    if debug:
        # read the window position from the config file
        with open(config_path, 'r') as f:
            pos = eval(f.read())
        return pos

    # FindWindow(lpClassName=None, lpWindowName=None)
    window = win32gui.FindWindow(None, window_title)

    while not window:
        log_print('Failed to obtain window, try again in 3 seconds...', 'error')
        sleep(3)
        window = win32gui.FindWindow(None, window_title)

    # Unlock the focus from Python IDLE
    win32com.client.Dispatch("WScript.Shell").SendKeys('%')

    # set the window to the foreground
    win32gui.SetForegroundWindow(window)
    pos = win32gui.GetWindowRect(window)

    # write the window position to the config file
    with open(config_path, 'w') as f:
        f.write(str(pos))

    log_print('Window position: %s' % str(pos), 'info')
    return (pos[0], pos[1])


def click_screen(x: 'int', y: 'int', sleep_wait=0.1, count=2):
    """
    Click the screen
    args:
        x - the x coordinate of the click position 
        y - the y coordinate of the click position 
        wait - the time to wait after each click 
        count - the number of clicks 
    return:
        None
    """
    x, y = math.floor(x), math.floor(y)

    for i in range(count):
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        sleep(0.03)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        sleep(sleep_wait)
