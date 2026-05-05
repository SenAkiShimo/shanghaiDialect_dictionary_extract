import cv2
import os
import numpy as np
from ultralytics import YOLO
from paddleocr import PaddleOCR

MODEL_PATH = './runs/detect/shanghai_dict/v1_high_res/weights/best.pt'
IMAGE_PATH = './picture/temp_page_8.png'
DEBUG_OUTPUT = './ocr_debug_visual.png'

# 类别颜色定义 (BGR)
COLORS = {
    0: (255, 0, 0),
    1: (0, 0, 255),
    2: (255, 255, 0),
    3: (0, 165, 255)
}

def debug_extraction():
    model = YOLO(MODEL_PATH)
    ocr = PaddleOCR(use_textline_orientation=True, lang='ch')

    img = cv2.imread(IMAGE_PATH)
    if img is None: return
    canvas = img.copy()
    h, w, _ = img.shape

    results = model.predict(IMAGE_PATH, conf=0.4)
    boxes = results[0].boxes.xyxy.cpu().numpy()
    clss = results[0].boxes.cls.cpu().numpy()
    confs = results[0].boxes.conf.cpu().numpy()

    print(f"检测到 {len(boxes)} 个目标，正在进行可视化校验...")

    for i in range(len(boxes)):
        x1, y1, x2, y2 = map(int, boxes[i])
        cls_id = int(clss[i])
        conf = confs[i]
        color = COLORS.get(cls_id, (0, 255, 0))

        cv2.rectangle(canvas, (x1, y1), (x2, y2), color, 2)
  
        ocr_text = ""
        if cls_id != 2: 
            crop = img[max(0, y1-2):min(h, y2+2), max(0, x1-2):min(w, x2+2)]
            res = ocr.ocr(crop)

            if res and res[0]:
                ocr_text = "".join([line[1][0] for line in res[0]])

        display_msg = f"C{cls_id}: {ocr_text}" if ocr_text else f"C{cls_id}"
        cv2.putText(canvas, display_msg, (x1, y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    cv2.imwrite(DEBUG_OUTPUT, canvas)
    print(f"调试图已生成: {DEBUG_OUTPUT}")
    os.system(f"open {DEBUG_OUTPUT}")

if __name__ == '__main__':
    debug_extraction()
