import cv2
import math
import numpy as np


class VolumeDrawing:
    def __init__(self,
                 thumb_index: int = 4,
                 index_finger_index: int = 8):
        self.thumb_index = thumb_index
        self.index_finger_index = index_finger_index

    def bar_level(self,
                  frame: np.ndarray,
                  landmark_list: list):
        x1, y1 = landmark_list[self.thumb_index][1], landmark_list[self.thumb_index][2]
        x2, y2 = landmark_list[self.index_finger_index][1], landmark_list[self.index_finger_index][2]

        min_length = 20
        max_length = 220

        length = round(math.hypot((x2 - x1), (y2 - y1)))
        length = min_length if length < min_length else max_length if length > max_length else length

        min_bar = 940
        max_bar = 115

        level_bar = np.interp(length, [min_length, max_length], [min_bar, max_bar])

        min_percentage = 0
        max_percentage = 100

        level_percentage = np.interp(length, [min_length, max_length], [min_percentage, max_percentage])

        cv2.rectangle(frame,
                      (50, 115),
                      (100, 940),
                      (193, 115, 37),
                      3)
        cv2.rectangle(frame,
                      (50, int(level_bar)),
                      (100, 940),
                      (193, 115, 37),
                      cv2.FILLED)

        if int(level_percentage == 100):
            position = (32, 975)
        elif int(level_percentage > 9):
            position = (42, 975)
        else:
            position = (52, 975)

        cv2.putText(frame,
                    f'{int(level_percentage)}%',
                    position,
                    cv2.FONT_HERSHEY_PLAIN,
                    2,
                    (193, 115, 37),
                    3)

    @staticmethod
    def fingers_line(frame: np.ndarray,
                     first_point: np.ndarray,
                     second_point: np.ndarray):
        cv2.circle(frame,
                   (first_point[1], first_point[2]),
                   9,
                   (193, 115, 37),
                   cv2.FILLED)
        cv2.circle(frame,
                   (second_point[1], second_point[2]),
                   9,
                   (193, 115, 37),
                   cv2.FILLED)
        cv2.line(frame,
                 (first_point[1], first_point[2]),
                 (second_point[1], second_point[2]),
                 (193, 115, 37),
                 3)
