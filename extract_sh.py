import os
import re
import cv2
import fitz
import pandas as pd
from paddleocr import PaddleOCR
import logging

logging.getLogger("ppocr").setLevel(logging.ERROR)

ocr = PaddleOCR(use_angle_cls=True, lang='ch')

def process_dictionary(pdf_path, start_page=3):
    doc = fitz.open(pdf_path)
    all_data = []

    for page_index in range(start_page-1, len(doc)):
        print(f"正在处理第 {page_index + 1} 页...")
        page = doc[page_index]
        
        pix = page.get_pixmap(dpi=300)
        img_path = f"temp_page_{page_index}.png"
        pix.save(img_path)

        img = cv2.imread(img_path)
        h, w, _ = img.shape
        left_part = img[:, :w//2]
        right_part = img[:, w//2:]

        for i, part in enumerate([left_part, right_part]):
            part_path = f"temp_part_{i}.png"
            cv2.imwrite(part_path, part)
            
            result = ocr.ocr(part_path)
            
            if not result or result[0] is None:
                continue

            for line_info in result[0]:
                raw_text = line_info[1][0]
                
                match = re.search(r'([\u4e00-\u9fa5]{1,5})', raw_text)
                if match:
                    word = match.group(1)
                    meaning = raw_text.replace(word, "")
                    meaning = re.sub(r'[a-zA-Z0-9\s\.\?\[\]\(\)\/]+', '', meaning)
                    
                    if len(meaning) > 0:
                        all_data.append([word, meaning])

    for f in [img_path, "temp_part_0.png", "temp_part_1.png"]:
        if os.path.exists(f): os.remove(f)

    return all_data

pdf_file = "dic.pdf" 
extracted_data = process_dictionary(pdf_file, start_page=8) 

df = pd.DataFrame(extracted_data, columns=['上海话原词', '普通话释义'])

for i in range(1, len(df)):
    if '~' in df.loc[i, '普通话释义']:
        df.loc[i, '普通话释义'] = df.loc[i, '普通话释义'].replace('~', df.loc[i, '上海话原词'])

df.to_csv("shanghai_result.csv", index=False, encoding='utf-8-sig')
print("全部处理完成！")