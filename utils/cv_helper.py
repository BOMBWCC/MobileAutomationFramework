import cv2
import numpy as np
import os
from typing import Optional, Tuple, List
from utils.logger import logger

class CVHelper:
    """
    Image Processing & Computer Vision Tool.
    Dependencies: opencv-python, numpy
    """

    @staticmethod
    def bytes_to_cv2(image_bytes: bytes) -> np.ndarray:
        """[Format Conversion]"""
        nparr = np.frombuffer(image_bytes, np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    @staticmethod
    def find_image_center(target_img_path: str, source_img_content: bytes = None, threshold: float = 0.8) -> Optional[Tuple[int, int]]:
        """
        [Core Positioning]
        Finds the center coordinates of target_img within source_img.
        :param target_img_path: Path to the template image.
        :param source_img_content: Bytes of the screenshot.
        :return: (x, y) or None
        """
        if not os.path.exists(target_img_path):
            logger.error(f"Template image not found: {target_img_path}")
            return None

        # Load images
        target = cv2.imread(target_img_path)
        source = CVHelper.bytes_to_cv2(source_img_content)

        # Template Matching
        result = cv2.matchTemplate(source, target, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            h, w = target.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            logger.debug(f"Image found at ({center_x}, {center_y}) with confidence {max_val:.2f}")
            return (center_x, center_y)
        
        logger.debug(f"Image not found. Max confidence: {max_val:.2f}")
        return None

    @staticmethod
    def is_image_exist(target_img_path: str, source_img_content: bytes, threshold: float = 0.8) -> bool:
        """[Boolean Check]"""
        return CVHelper.find_image_center(target_img_path, source_img_content, threshold) is not None

    @staticmethod
    def calculate_ssim(img1_path: str, img2_path: str) -> float:
        """
        [Structural Similarity] - Simplified implementation using Histogram if skimage is missing,
        or basic pixel diff. For robust SSIM, 'scikit-image' is needed.
        Here we use a basic Histogram comparison (Correlation) as a fallback/simpler version standard in OpenCV.
        Returns 0.0 to 1.0 (1.0 = identical).
        """
        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)

        if img1 is None or img2 is None:
            logger.error("One of the images for comparison could not be loaded.")
            return 0.0

        # Resize to match
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

        # Convert to HSV
        hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

        # Calculate Histograms
        hist1 = cv2.calcHist([hsv1], [0, 1], None, [180, 256], [0, 180, 0, 256])
        hist2 = cv2.calcHist([hsv2], [0, 1], None, [180, 256], [0, 180, 0, 256])

        cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

        # Compare (Correlation)
        similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        return similarity

    @staticmethod
    def crop_image(image_path: str, rect: Tuple[int, int, int, int]) -> str:
        """
        [Crop]
        Crops image and saves it as temporary file.
        rect: (x, y, w, h)
        """
        img = cv2.imread(image_path)
        x, y, w, h = rect
        crop = img[y:y+h, x:x+w]
        
        # Save to temp
        dir_name = os.path.dirname(image_path)
        base_name = os.path.basename(image_path)
        new_path = os.path.join(dir_name, f"crop_{base_name}")
        cv2.imwrite(new_path, crop)
        return new_path
