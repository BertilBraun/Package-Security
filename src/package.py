from __future__ import annotations
import cv2
import numpy as np
import glob
import random


# Load Yolo
net = cv2.dnn.readNet("../assets/yolov3_training_last.weights",
                      "../assets/yolov3_testing.cfg")

layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


def get_box_positions(img, threshhold: float = 0.3) -> list[tuple[int, int, int, int]]:
    height, width, channels = img.shape
    # Detecting objects
    blob = cv2.dnn.blobFromImage(
        img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            if scores[class_id] > threshhold:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])

    return boxes


def display_results(img, boxes: list[tuple[int, int, int, int]]) -> None:

    # hack -> confidences are not relevant atm
    confidences = [0.3] * len(boxes)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, "Package", (x, y + 30), font, 3, (255, 0, 0), 2)

    cv2.imshow("Image", img)
