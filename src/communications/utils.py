import cv2
from pytesseract import image_to_string


def ocr_core(img_path: str) -> str:
    """Optical Character Recognition"""
    cv_img = cv2.imread(img_path)
    gray_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
    thresh_binary = cv2.THRESH_BINARY_INV if hist[:128].sum() > hist[128:].sum() else cv2.THRESH_BINARY
    _, binarized_img = cv2.threshold(gray_img, 0, 255, thresh_binary | cv2.THRESH_OTSU)

    # denoised_img = cv2.GaussianBlur(binarized_img, (3, 3), cv2.BORDER_DEFAULT)
    rgb_img = cv2.cvtColor(binarized_img, cv2.COLOR_GRAY2RGB)
    cv2.imwrite(img_path, rgb_img)

    text = image_to_string(rgb_img, lang='eng+rus', config='--oem 3 --psm 6')
    # удалить пустые строчки
    text = '\n'.join(s.rstrip() for s in text.split('\n') if s.rstrip())
    return text
