import cv2
from pytesseract import image_to_string


def ocr_core(filename: str) -> str:
    """Optical Character Recognition"""
    image = cv2.imread(filename)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Удаление шума и улучшение контраста
    image_filtered = cv2.GaussianBlur(image_gray, (3, 3), 0)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    image_clahe = clahe.apply(image_filtered)

    # Построение гистограммы яркости
    hist = cv2.calcHist([image_clahe], [0], None, [256], [0, 256])

    # Если черных пикселей больше, инвертируем цвета
    thresh_binary = cv2.THRESH_BINARY_INV if hist[:128].sum() > hist[128:].sum() else cv2.THRESH_BINARY
    _, img_bin = cv2.threshold(image_clahe, 0, 255, thresh_binary | cv2.THRESH_OTSU)

    cv2.imwrite(filename, img_bin)

    text = image_to_string(img_bin, lang='eng+rus', config='--oem 3 --psm 6')
    return text.strip()
