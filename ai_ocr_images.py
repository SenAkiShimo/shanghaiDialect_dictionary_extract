import cv2
from ultralytics import YOLO
from paddleocr import PaddleOCR
import pandas as pd
import re

model = YOLO('runs/detect/shanghai_dict_v1/weights/best.pt')

ocr = PaddleOCR(use_angle_cls=True, lang='ch')

def smart_extract(img_path):
    img = cv2.imread(img_path)
    results = model.predict(img_path, conf=0.5)
    
    boxes = results[0].boxes.xyxy.cpu().numpy()
    boxes = sorted(boxes, key=lambda x: x[1])
    
    extracted_data = []
    
    for box in boxes:
        x1, y1, x2, y2 = map(int, box)
        crop = img[y1:y2, x1:x2]
        
        ocr_res = ocr.ocr(crop, cls=True)
        
        if ocr_res and ocr_res[0]:
            full_text = "".join([line[1][0] for line in ocr_res[0]])

            match = re.search(r'^([\u4e00-\u9fa5]+).*?([\u4e00-\u9fa5〈（[].*)$', full_text)
            if match:
                word = match.group(1)
                meaning = match.group(2)
                extracted_data.append([word, meaning])
            else:
                extracted_data.append([full_text, "待手动拆分"])
                
    return extracted_data

# 运行并保存
data = smart_extract('./picture/temp_page_8.png')
df = pd.DataFrame(data, columns=['上海话原词', '普通话释义'])
df.to_csv('final_dictionary_result.csv', index=False, encoding='utf-8-sig')
print("提取完成！")
