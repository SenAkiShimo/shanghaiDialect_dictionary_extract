import os
import re
import pandas as pd
from paddleocr import PaddleOCR
import logging

logging.getLogger("ppocr").setLevel(logging.ERROR)


ocr = PaddleOCR(use_angle_cls=True, lang='ch')

def extract_from_images(image_folder):
    all_data = []
    images = sorted([f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])
    
    for img_name in images:
        img_path = os.path.join(image_folder, img_name)
        print(f"正在识别: {img_name}...")
        
        result = ocr.ocr(img_path)
        if not result or result[0] is None:
            continue

        for line_info in result[0]:
            raw_text = line_info[1][0]
            
            clean_text = re.sub(r'[a-zA-Z0-9\s\.\[\]\(\)\/ʔø\?\'\"]+', '', raw_text)
            
            chinese_blocks = re.findall(r'[\u4e00-\u9fa5]+|~', clean_text)
            
            if len(chinese_blocks) >= 2:
                word = chinese_blocks[0]
                meaning = "".join(chinese_blocks[1:])
                all_data.append([word, meaning])
            elif len(chinese_blocks) == 1:
                all_data.append([chinese_blocks[0], ""])

    return all_data

folder_path = "./"
output_csv = "shanghai_dict_final.csv"

extracted_results = extract_from_images(folder_path)

if extracted_results:
    df = pd.DataFrame(extracted_results, columns=['上海话原词', '普通话释义'])
    
    for i in range(len(df)):
        if '~' in df.loc[i, '普通话释义']:
            df.loc[i, '普通话释义'] = df.loc[i, '普通话释义'].replace('~', df.loc[i, '上海话原词'])
            
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"\n提取完成！共得到 {len(df)} 条数据，已保存至: {output_csv}")
else:
    print("\n未能在图片中识别到有效内容，请检查图片路径或清晰度。")
