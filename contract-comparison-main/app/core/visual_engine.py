import cv2
import numpy as np
from pdf2image import convert_from_path
from typing import List

def pdf_to_image(path: str) -> List[np.ndarray]:
    """Convert PDF pages to image arrays"""
    pages = convert_from_path(path)
    return [np.array(p.convert("RGB")) for p in pages]

def compare_images(img1: np.ndarray, img2: np.ndarray) -> float:
    """Return structural similarity index (SSIM) between two images"""
    from skimage.metrics import structural_similarity as ssim

    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    score, _ = ssim(img1_gray, img2_gray, full=True)
    return score

def compare_visual_elements(file1: str, file2: str) -> dict:
    """Compare the first pages of two PDFs/images and return a similarity score"""
    try:
        img1 = pdf_to_image(file1)[0]
        img2 = pdf_to_image(file2)[0]
    except Exception as e:
        return {"error": str(e)}

    similarity = compare_images(img1, img2)
    return {"visual_similarity_score": round(similarity, 4)}
