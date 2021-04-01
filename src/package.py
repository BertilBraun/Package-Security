from imageai.Detection import ObjectDetection

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath("../assets/resnet50_coco_best_v2.1.0.h5")
detector.loadModel()

detections = detector.detectObjectsFromImage(input_image="../assets/image.jpg", output_image_path="imagenew.jpg")

for eachObject in detections:
    print(eachObject["name"], " : " , eachObject["percentage_probability"])