import cv2
import time

from commons.hand_detector import HandDetector
from services.volume_control import VolumeControl
from services.volume_drawing import VolumeDrawing


def main():
    print(cv2.getBuildInformation())

    capture = cv2.VideoCapture()
    capture.open(0 + cv2.CAP_DSHOW)
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    capture.set(cv2.CAP_PROP_FOURCC, fourcc)
    capture.set(cv2.CAP_PROP_FPS, 30)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)

    detector = HandDetector(max_num_hands=1,
                            detection_confidence=0.7)
    volume = VolumeControl()
    drawing = VolumeDrawing()

    previous_time = 0

    while True:
        _, frame = capture.read()

        if frame is None:
            print("The frame is empty")
            break
        else:
            image_color = cv2.cvtColor(src=frame,
                                       code=cv2.COLOR_BGR2RGB)
            frame = detector.find_hands(frame=frame,
                                        image_color=image_color,
                                        draw=False)
            landmark_list = detector.find_position(frame=frame)

            if len(landmark_list) != 0:
                volume.define_level(landmark_list=landmark_list)
                drawing.fingers_line(frame=frame,
                                     first_point=landmark_list[4],
                                     second_point=landmark_list[8])
                drawing.bar_level(frame=frame,
                                  landmark_list=landmark_list)

        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time

        cv2.putText(frame, f'{(int(fps))}fps', (32, 56), cv2.FONT_HERSHEY_PLAIN, 2, (193, 115, 37), 2)

        cv2.imshow('Volume Hand Control', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
