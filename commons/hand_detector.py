import mediapipe as mp
import numpy as np


class HandDetector:
    def __init__(self,
                 static_image_mode: bool = False,
                 max_num_hands: int = 2,
                 detection_confidence: float = 0.5,
                 tracking_confidence: float = 0.5):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.static_image_mode,
            max_num_hands=self.max_num_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

        self.results = None

    def find_hands(self,
                   frame: np.ndarray,
                   image_color: np.ndarray,
                   draw: bool = True):
        self.results = self.hands.process(image_color)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(frame,
                                                hand_landmarks,
                                                self.mp_hands.HAND_CONNECTIONS)

        return frame

    def find_position(self,
                      frame: np.ndarray,
                      hand_num: int = 0):
        landmark_list = []

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_num]

            for point, landmark in enumerate(hand.landmark):
                height, width, center = frame.shape
                center_x, center_y = int(landmark.x * width), int(landmark.y * height)

                landmark_list.append([point, center_x, center_y])

        return landmark_list
