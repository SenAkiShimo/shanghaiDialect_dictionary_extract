import os
import csv
import logging
from paddleocr import PaddleOCR

logging.getLogger("ppocr").setLevel(logging.ERROR)
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

def final_inspect(img_path, output_csv):
    print(f"正在扫描: {img_path}")
    result = ocr.ocr(img_path)
    
    if not result:
        print("错误：OCR 没返回任何结果。")
        return

    all_data = []

    if isinstance(result, list):
        for item in result:
            print(f"【原始数据片段】: {item}")
            
            text_content = ""
            if isinstance(item, dict):
                text_content = item.get('rec_text', str(item))
            else:
                text_content = str(item)
            
            if text_content:
                all_data.append([text_content])

    if all_data:
        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['OCR原始输出'])
            writer.writerows(all_data)
        print(f"\n--- 写入成功！共 {len(all_data)} 行 ---")
        print(f"请立刻打开文件夹里的 {output_csv}，看看里面有没有文字。")
    else:
        print("没提取到有效字符串。")

final_inspect("temp_page_10.png", "raw_check.csv")
