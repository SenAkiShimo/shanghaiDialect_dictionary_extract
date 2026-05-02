import os
import re
import cv2
import csv
import logging
from paddleocr import PaddleOCR


logging.getLogger("ppocr").setLevel(logging.ERROR)
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

def extract_entry(text):
    text = re.sub(r'^[0-9\.\s]+', '', text)
    blocks = re.findall(r'[\u4e00-\u9fa5]+|~|[①②③④⑤]|\<名\>|\<动\>|\(气\)', text)
    
    if len(blocks) >= 2:
        word = blocks[0]
        meaning = "".join(blocks[1:])

        return [word, meaning]
    
    elif len(blocks) == 1:
        return [blocks[0], "（仅词条）"]
        
    return None

def process_dictionary_page(img_path):
    img = cv2.imread(img_path)
    if img is None: return []
    h, w, _ = img.shape
    
    parts = [img[:, :w//2], img[:, w//2:]]
    page_data = []

    for i, part in enumerate(parts):
        part_path = f"temp_part_{i}.png"
        cv2.imwrite(part_path, part)
        

        raw_result = ocr.ocr(part_path)
        if not raw_result: continue

        lines_dict = {}
        for item in raw_result:
            if not isinstance(item, dict) or 'dt_polygons' not in item:
                continue
                
            text = item.get('rec_text', '')
            poly = item['dt_polygons']
            y_center = (poly[0][1] + poly[2][1]) / 2
            x_start = poly[0][0]

            found_line = False
            for existing_y in lines_dict.keys():
                if abs(existing_y - y_center) < 20:
                    lines_dict[existing_y].append((x_start, text))
                    found_line = True
                    break
            if not found_line:
                lines_dict[y_center] = [(x_start, text)]

        for y in sorted(lines_dict.keys()):
            row_items = sorted(lines_dict[y], key=lambda x: x[0])
            full_row_text = "".join([it[1] for it in row_items])
            
            entry = extract_entry(full_row_text)
            if entry:
                page_data.append(entry)
                
    return page_data

img_input = "temp_page_10.png" 
output_csv = "shanghai_v7_final.csv"

if os.path.exists(img_input):
    results = process_dictionary_page(img_input)
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['上海话原词', '普通话释义'])
        for row in results:
            word, meaning = row
            if '~' in meaning:
                meaning = meaning.replace('~', word)
            writer.writerow([word, meaning])
    print(f"处理完成，提取了 {len(results)} 条。")
else:
    print(f"错误：找不到图片 {img_input}")
