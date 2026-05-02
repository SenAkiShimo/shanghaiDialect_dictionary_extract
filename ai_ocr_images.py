import cv2
import re
import os
import csv
import pandas as pd
from ultralytics import YOLO
from paddleocr import PaddleOCR
import logging

MODEL_PATH = './runs/detect/shanghai_dict_v1-2/weights/best.pt'
IMAGE_PATH = './picture/temp_page_8.png'
OUTPUT_CSV = 'shanghai_final_clean.csv'

logging.getLogger("ppocr").setLevel(logging.ERROR)


model = YOLO(MODEL_PATH)
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

def get_texts_recursive(data):
    if isinstance(data, str):
        yield data
    elif isinstance(data, dict):
        for v in data.values():
            yield from get_texts_recursive(v)
    elif isinstance(data, (list, tuple)):
        for item in data:
            yield from get_texts_recursive(item)

def clean_and_split_v3(raw_text):
    clean_text = re.sub(r'[a-zA-Z0-9\s\.ʔøãẽĩõũəɛɔ\[\]\|\/\\t]+', '', str(raw_text))
    tags = r'(名|动|形|副|代|量|叹|见|连|助|拟|〈名〉|〈动〉|〈形〉|〈副〉|①|②|③|④|~)'
    match = re.search(f'^([\u4e00-\u9fa5]+)({tags})(.*)$', clean_text)
    
    if match:
        return match.group(1), f"{match.group(2)}{match.group(3)}"
    
    blocks = re.findall(r'[\u4e00-\u9fa5]+|~', clean_text)
    if len(blocks) >= 2:
        return blocks[0], "".join(blocks[1:])
    elif len(blocks) == 1:
        return blocks[0], clean_text
    return None, None

def run_extraction():
    img = cv2.imread(IMAGE_PATH)
    if img is None:
        print(f"找不到图片: {IMAGE_PATH}")
        return

    results = model.predict(IMAGE_PATH, conf=0.4)
    boxes = results[0].boxes.xyxy.cpu().numpy()
    
    h, w, _ = img.shape
    mid_x = w / 2
    left_column = [b for b in boxes if (b[0] + b[2]) / 2 < mid_x]
    right_column = [b for b in boxes if (b[0] + b[2]) / 2 >= mid_x]
    
    left_column = sorted(left_column, key=lambda b: b[1])
    right_column = sorted(right_column, key=lambda b: b[1])
    sorted_boxes = left_column + right_column

    final_data = []
    print(f"AI 发现了 {len(sorted_boxes)} 个条目，正在识别...")

    for box in sorted_boxes:
        x1, y1, x2, y2 = map(int, box)
        crop = img[max(0, y1-2):min(h, y2+2), max(0, x1-2):min(w, x2+2)]
        
        ocr_res = ocr.ocr(crop)
        if not ocr_res or not ocr_res[0]: continue
        
        raw_fragments = list(get_texts_recursive(ocr_res))
        full_line = "".join([str(t) for t in raw_fragments if not isinstance(t, (float, int))])
        
        word, meaning = clean_and_split_v3(full_line)
        if word:
            if isinstance(meaning, str):
                meaning = meaning.replace('~', word)
            final_data.append([word, meaning])

    if final_data:
        df = pd.DataFrame(final_data, columns=['上海话原词', '普通话释义'])
        df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
        print(f"提取完成！共 {len(final_data)} 条，保存至 {OUTPUT_CSV}")

if __name__ == '__main__':
    run_extraction()
