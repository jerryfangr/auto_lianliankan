import os
import cv2
import numpy as np
from ck_model.predict import load_model, predict_same


if __name__ == '__main__':
    PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def pi(file_num):
        return os.path.join(PROJECT_PATH, 'main/temp', 'item_{}.png'.format(file_num))

    def pt(file_num):
        return os.path.join(PROJECT_PATH, 'main/temp', 'type_{}.png'.format(file_num))

    # print('1 --', cal_img_similarity(pi(19), pi(26), 'path'))
    # print('0 --', cal_img_similarity(pi(17), pi(22), 'path'))

    DEBUG_MODE = True
    check_data = [
        (pi(42), pi(43), 0),
        (pi(42), pt(5), 0),
        (pi(43), pt(5), 1),
    ]

    for cd in check_data:
        c_r = predict_same(cd[0], cd[1], load_model(), DEBUG_MODE)
        print(c_r, ' pass -->', c_r == cd[2])

    # c_r = predict_same(pi(0), pt(0), load_model()),
    # print('0 --', c_r, c_r == 0)
    # c_r = predict_same(pi(0), pt(1), load_model()),
    # print('0 --', c_r, c_r == 0)
    # c_r = predict_same(pi(4), pt(1), load_model()),
    # print('0 --', c_r, c_r == 0)
    # c_r = predict_same(pi(9), pi(15), load_model()),
    # print('1 --', c_r, c_r == 1)
    # c_r = predict_same(pt(1), pt(0), load_model()),
    # print('0 --', c_r, c_r == 0)
