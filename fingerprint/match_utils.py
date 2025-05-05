import cv2
import numpy as np
from skimage.morphology import skeletonize
from scipy.spatial import distance

def preprocess_fingerprint(img):
    """Convert grayscale image to binary skeleton."""
    eq = cv2.equalizeHist(img)
    blur = cv2.GaussianBlur(eq, (5, 5), 0)
    _, threshed = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    inverted = 255 - threshed
    skeleton = skeletonize(inverted // 255).astype(np.uint8)
    return skeleton

def extract_minutiae(skeleton):
    """Detect ridge endings and bifurcations in 3x3 windows."""
    minutiae = []
    rows, cols = skeleton.shape
    for y in range(1, rows - 1):
        for x in range(1, cols - 1):
            if skeleton[y, x] == 1:
                neighbors = skeleton[y-1:y+2, x-1:x+2].flatten()
                count = np.sum(neighbors) - 1
                if count == 1:
                    minutiae.append((x, y, "ending"))
                elif count == 3:
                    minutiae.append((x, y, "bifurcation"))
    return minutiae

def compare_minutiae(template1, template2, dist_thresh=10):
    matches = 0
    matched_indices = set()
    for x1, y1, type1 in template1:
        for i, (x2, y2, type2) in enumerate(template2):
            if i in matched_indices:
                continue
            if type1 == type2:
                dist = distance.euclidean((x1, y1), (x2, y2))
                if dist < dist_thresh:
                    matched_indices.add(i)
                    matches += 1
                    break
    return matches, len(template1), len(template2)
