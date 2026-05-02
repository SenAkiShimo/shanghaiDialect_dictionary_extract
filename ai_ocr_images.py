import cv2
from ultralytics import YOLO
from paddleocr import PaddleOCR
import pandas as pd
import re

model = YOLO('./runs/detect/shanghai_dict_v1-2/weights/best.pt')

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
        
        ocr_res = ocr.ocr(crop)
        
        if ocr_res:
            def get_texts(data):
                if isinstance(data, str): yield data
                elif isinstance(data, dict):
                    for v in data.values(): yield from get_texts(v)
                elif isinstance(data, (list, tuple)):
                    for item in data: yield from get_texts(item)

            raw_fragments = list(get_texts(ocr_res))
            full_text = "".join([t for t in raw_fragments if isinstance(t, str) and not t.replace('.','').isdigit()])

            if not full_text.strip():
                continue

            blocks = re.findall(r'[\u4e00-\u9fa5]+|~', full_text)
            
            if len(blocks) >= 2:
                word = blocks[0]
                meaning = "".join(blocks[1:])
                meaning = meaning.replace('~', word)
                extracted_data.append([word, meaning])
            elif len(blocks) == 1:
                extracted_data.append([blocks[0], full_text])
            else:
                extracted_data.append([full_text, "OCR未能分离汉字"])
                
    return extracted_data

image_to_process = './picture/temp_page_8.png'
data = smart_extract(image_to_process)

df = pd.DataFrame(data, columns=['上海话原词', '普通话释义'])
df.to_csv('final_dictionary_result.csv', index=False, encoding='utf-8-sig')
print(f"提取完成，共识别到 {len(data)} 条词目！")