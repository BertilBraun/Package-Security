from __future__ import annotations
import cv2
import numpy as np
from face_recognition import face_encodings, face_locations, face_distance, load_image_file, compare_faces
from util import boxt


def _load_known():
    return [
        face_encodings(load_image_file("../assets/face_test/biden.jpg"))[0],
        face_encodings(load_image_file("../assets/face_test/obama.jpg"))[0]
    ], [
        "Biden",
        "Obama"
    ]


known_encodings, known_names = _load_known()


def detect_faces(img) -> tuple[list[str], list[boxt]]:
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)[:, :, ::-1]

    locations = face_locations(frame)
    encodings = face_encodings(frame, locations)

    names = []
    for encoding in encodings:
        # See if the face is a match for the known face(s)
        matches = compare_faces(known_encodings, encoding)

        # # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        distances = face_distance(known_encodings, encoding)
        best_match_index = np.argmin(distances)
        if matches[best_match_index]:
            names.append(known_names[best_match_index])
        else:
            names.append("THIEF")

    return names, [(x*4, y*4, w*4, h*4) for (x, y, w, h) in locations]


def display_detection(img, names: list[str], locations: list[boxt]):

    for name, (top, right, bottom, left) in zip(names, locations):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(img, (left, bottom - 35),
                      (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(img, name, (left + 6, bottom - 6),
                    font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Image', img)
