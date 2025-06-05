# visual_engine.py
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import os
from typing import List, Dict, Any
from ultralytics import YOLO
from skimage.metrics import structural_similarity as ssim


def _get_images_from_supported_file(file_path: str) -> List[np.ndarray]:
    """Extracts images from PDFs or image files (.png, .jpg, .jpeg)."""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    images = []

    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return images

    try:
        if ext == ".pdf":
            pdf_pages = convert_from_path(file_path)
            for page in pdf_pages:
                images.append(np.array(page.convert("RGB")))
            print(f"Info: Extracted {len(images)} page(s) from PDF '{os.path.basename(file_path)}'.")
        elif ext in [".png", ".jpg", ".jpeg"]:
            img = Image.open(file_path).convert("RGB")
            images.append(np.array(img))
            print(f"Info: Loaded image '{os.path.basename(file_path)}'.")
        else:
            print(f"Info: Visual processing skipped for file type '{ext}' in '{os.path.basename(file_path)}'.")
    except Exception as e:
        print(f"Error extracting images from '{os.path.basename(file_path)}': {e}")

    return images


def compare_page_ssim(img1: np.ndarray, img2: np.ndarray) -> float:
    """Computes SSIM between two RGB images (converted to grayscale)."""
    if img1 is None or img2 is None or img1.size == 0 or img2.size == 0:
        return 0.0

    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    if h1 != h2 or w1 != w2:
        img2 = cv2.resize(img2, (w1, h1))

    img1_gray = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY) if len(img1.shape) == 3 else img1
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY) if len(img2.shape) == 3 else img2

    score, _ = ssim(img1_gray, img2_gray, full=True, data_range=img1_gray.max() - img1_gray.min())
    return score


def compare_visual_elements(file1_path: str, file2_path: str, yolo_model_path: str = "signatureyolo.pt") -> Dict[str, Any]:
    """
    Compares visual elements of two documents.
    Performs YOLO detection and page-wise SSIM analysis.
    """
    results = {
        "yolo_detections_doc1": [],
        "yolo_detections_doc2": [],
        "page_ssim_scores": [],
        "average_ssim": None,
        "notes": []
    }

    try:
        images1 = _get_images_from_supported_file(file1_path)
        images2 = _get_images_from_supported_file(file2_path)

        if not images1 and not images2:
            results["notes"].append("No visual content could be extracted from either file.")
            return results

        if not images1:
            results["notes"].append(f"Visual analysis not performed or failed for Document 1: {os.path.basename(file1_path)}.")
        if not images2:
            results["notes"].append(f"Visual analysis not performed or failed for Document 2: {os.path.basename(file2_path)}.")

        # Load YOLO model once
        model = YOLO(yolo_model_path)

        # YOLO Detection for Document 1
        if images1:
            doc1_yolo_pages = []
            for idx, img_array in enumerate(images1):
                detections = model.predict(img_array, verbose=False)[0]
                boxes = detections.boxes
                detection_list = []
                for box in boxes:
                    coords = box.xyxy.cpu().numpy().tolist()[0]
                    conf = float(box.conf.cpu().numpy()[0])
                    cls = int(box.cls.cpu().numpy()[0])
                    detection_list.append({
                        "class_id": cls,
                        "confidence": round(conf, 4),
                        "bbox": [round(c, 2) for c in coords]
                    })
                doc1_yolo_pages.append({"page": idx + 1, "detections": detection_list})
                results["notes"].append(f"Detected {len(detection_list)} object(s) on page {idx + 1} of Document 1.")
            results["yolo_detections_doc1"] = doc1_yolo_pages

        # YOLO Detection for Document 2
        if images2:
            doc2_yolo_pages = []
            for idx, img_array in enumerate(images2):
                detections = model.predict(img_array, verbose=False)[0]
                boxes = detections.boxes
                detection_list = []
                for box in boxes:
                    coords = box.xyxy.cpu().numpy().tolist()[0]
                    conf = float(box.conf.cpu().numpy()[0])
                    cls = int(box.cls.cpu().numpy()[0])
                    detection_list.append({
                        "class_id": cls,
                        "confidence": round(conf, 4),
                        "bbox": [round(c, 2) for c in coords]
                    })
                doc2_yolo_pages.append({"page": idx + 1, "detections": detection_list})
                results["notes"].append(f"Detected {len(detection_list)} object(s) on page {idx + 1} of Document 2.")
            results["yolo_detections_doc2"] = doc2_yolo_pages

        # SSIM Page-by-Page
        if images1 and images2:
            num_pages1 = len(images1)
            num_pages2 = len(images2)
            common_pages = min(num_pages1, num_pages2)
            ssim_scores = []

            if num_pages1 != num_pages2:
                results["notes"].append(
                    f"Document 1 has {num_pages1} page(s), Document 2 has {num_pages2}. "
                    f"Comparing SSIM for first {common_pages} common page(s)."
                )

            for i in range(common_pages):
                score = compare_page_ssim(images1[i], images2[i])
                results["page_ssim_scores"].append({"page": i + 1, "ssim_score": round(score, 4)})
                ssim_scores.append(score)

            if ssim_scores:
                results["average_ssim"] = round(sum(ssim_scores) / len(ssim_scores), 4)
        elif (images1 or images2):
            results["notes"].append("SSIM comparison skipped due to one document missing image content.")

    except Exception as e:
        results["error"] = f"General error in compare_visual_elements: {str(e)}"
        print(f"Error in compare_visual_elements: {e}")

    return results
