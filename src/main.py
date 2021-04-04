import cv2

from package import get_box_positions, display_results
from speech import play_text
from face import detect_faces, display_detection
from util import boxt, get_center_from_box

def main():

    video_capture = cv2.VideoCapture(0)

    last_box_stack = []

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        names, locations = detect_faces(frame)
        display_detection(frame, names, locations)

        boxes = get_box_positions(frame)
        # display_results(frame, boxes)

        for box in boxes:
            print("box", box, get_center_from_box(box))
        for loc in locations:
            print("face", loc, get_center_from_box(loc))

        # If packet was in picture + packet is moving up + face not recognized -> play Alarm
        if "THIEF" in names:  # TODO and packet was in picture and packet is moving up
            # TODO only play once
            # play_text("Hey! Stop this right now!")
            pass

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
