from face_recognition import face_encodings, load_image_file, compare_faces


def load_known_encodings():
    return [
        # face_encodings(load_image_file("biden.jpg"))[0],
        face_encodings(load_image_file("obama.jpg"))[0]
    ]

known_encodings = load_known_encodings()
unknown_encoding = face_encodings(load_image_file("biden.jpg"))[0]

results = compare_faces(known_encodings, unknown_encoding)
print(any(results))