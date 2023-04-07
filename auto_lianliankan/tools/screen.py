import math
import os
import win32api
import win32gui
import win32con
import cv2
from PIL import ImageGrab
from time import sleep
from config import setting as SETTING
from tools.logger import log_print

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_screen_image(type=None):
    """
    Get the screenshot
    args:
        None
    return:
        image(numpy array) - the screenshot of the screen 
    """

    screen_path = os.path.join(PROJECT_PATH, SETTING.TEMP_PATH, 'screen.png')

    if type != 'read':
        scim = ImageGrab.grab() 
        scim.save(screen_path)

    return cv2.imread(screen_path)


def get_window_position(window_title=''):
    """
    Get the window position
    args:
        window_title(string) - the text of window title bar 
    return:
        (x, y) - the position of the window
    """

    # FindWindow(lpClassName=None, lpWindowName=None)
    window = win32gui.FindWindow(None, window_title)
    
    while not window:
        log_print('Failed to obtain window, try again in 3 seconds...', 'error')
        sleep(3)
        window = win32gui.FindWindow(None, window_title)

    # set the window to the foreground
    win32gui.SetForegroundWindow(window)
    pos = win32gui.GetWindowRect(window)

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
    win32api.SetCursorPos((x, y))
    sleep(0.05)

    for i in range(count):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        sleep(sleep_wait)
