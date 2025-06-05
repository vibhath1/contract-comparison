# yolo_detector.py
# (Your provided code for yolo_detector.py is correct for this requirement)
# Key function run_yolo_on_image(model_path, image) is used by visual_engine.
from ultralytics import YOLO
import cv2
# from pdf2image import convert_from_path # Not strictly needed if pdf_to_images is only for the PDF-specific func
import numpy as np

# This function is PDF-specific. visual_engine._get_images_from_supported_file handles PDF to image conversion.
# def pdf_to_images(pdf_path):
#     from pdf2image import convert_from_path # Moved import here
#     pages = convert_from_path(pdf_path)
#     return [np.array(page.convert("RGB")) for page in pages]

def run_yolo_on_image(model_path, image): # This is the core function used by visual_engine
    model = YOLO(model_path)
    results = model.predict(image, verbose=False) # Added verbose=False
    detections = []

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist()
            label = r.names[cls_id]
            detections.append({
                "label": label,
                "confidence": round(conf, 4),
                "box": [round(x) for x in xyxy]
            })
    return detections

# This function is PDF-specific due to pdf_to_images call.
# visual_engine now prepares images from various sources and calls run_yolo_on_image directly.
# So, this function might not be used in the main comparison_engine flow.
# def detect_visual_elements_yolo(pdf_path, model_path):
#     images = pdf_to_images(pdf_path)
#     all_detections = []
#     for idx, img in enumerate(images):
#         detections = run_yolo_on_image(model_path, img)
#         all_detections.append({
#             "page": idx + 1,
#             "detections": detections
#         })
#     return all_detections