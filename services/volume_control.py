import math
import numpy as np

from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class VolumeControl:
    def __init__(self,
                 thumb_index: int = 4,
                 index_finger_index: int = 8):
        self.thumb_index = thumb_index
        self.index_finger_index = index_finger_index

    def define_level(self,
                     landmark_list: list):
        x1, y1 = landmark_list[self.thumb_index][1], landmark_list[self.thumb_index][2]
        x2, y2 = landmark_list[self.index_finger_index][1], landmark_list[self.index_finger_index][2]

        min_length = 20
        max_length = 220

        length = round(math.hypot((x2 - x1), (y2 - y1)))
        length = min_length if length < min_length else max_length if length > max_length else length

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume_range = volume.GetVolumeRange()
        min_volume = volume_range[0]
        max_volume = volume_range[1]

        level = np.interp(length, [min_length, max_length], [min_volume, max_volume])

        volume.SetMasterVolumeLevel(level, None)
