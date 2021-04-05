from __future__ import annotations
import cv2
from datetime import datetime

from package import get_box_positions, display_results
from speech import play_text
from face import detect_faces, display_detection
from util import boxt, get_center_from_box


# TODO issue: faces sometimes faces get detected as boxes..
# TODO issue: box detection is misserable for every frame to get the same bounding boxes..

def dist(a: tuple[int, int], b: tuple[int, int]) -> float:
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2) ** 0.5


def main():

    video_capture = cv2.VideoCapture(0)

    tracked_boxes = {}  # { init_pos: (curr_pos) }
    last_time_played = datetime.now()

    box_threshhold = 150
    alarm_threshhold = 200

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        names, locations = detect_faces(frame)
        display_detection(frame, names, locations)

        boxes = get_box_positions(frame)
        # display_results(frame, boxes)

        # prevent postman etc to trigger the alarm with new packages
        if len(boxes) > len(tracked_boxes):
            print("New box detected")
            last_time_played = datetime.now()

        # packet was in picture and packet is moving up
        package_picked_up = False

        alive_packages = []
        for box in boxes:
            cc = get_center_from_box(box)
            print("box", box, cc)
            for initial, lc in tracked_boxes.items():
                print(dist(cc, lc))
                if dist(cc, lc) < box_threshhold:
                    tracked_boxes[initial] = cc
                    alive_packages.append(initial)
                    if dist(cc, initial) > alarm_threshhold:
                        package_picked_up = True
                    break
            else:
                tracked_boxes[cc] = cc
                alive_packages.append(cc)

        # remove none existing boxes
        to_delete = [key for key in tracked_boxes if key not in alive_packages]
        for key in to_delete:
            del tracked_boxes[key]

        print("deleted", to_delete, alive_packages)
        print(tracked_boxes)

        for loc in locations:
            print("face", loc, get_center_from_box(loc))

        # If packet was in picture + packet is moving up + face not recognized -> play Alarm | only play once
        if "THIEF" in names \
                and (datetime.now() - last_time_played).total_seconds() > 30 \
                and package_picked_up:
            print("ALARM!")
            play_text("Hey! Stop this right now!")
            last_time_played = datetime.now()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
