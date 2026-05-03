import cv2
import os
from ultralytics import YOLO

MODEL_PATH = './runs/detect/shanghai_dict/v1_high_res/weights/best.pt'
IMAGE_PATH = './picture/temp_page_8.png'
DEBUG_OUTPUT = './debug_visual.png'

def debug_yolo_boxes():
    model = YOLO(MODEL_PATH)
    img = cv2.imread(IMAGE_PATH)
    results = model.predict(IMAGE_PATH, conf=0.4)[0]

    boxes = results.boxes.xyxy.cpu().numpy()
    clss = results.boxes.cls.cpu().numpy()
    
    h, w, _ = img.shape
    mid_x = w / 2

    colors = {
        0: (0, 255, 0),
        1: (255, 0, 0),
        2: (0, 0, 255),
        3: (255, 255, 0)
    }

    data = []
    for box, cls in zip(boxes, clss):
        if int(cls) == 2: continue 
        
        center_x = (box[0] + box[2]) / 2
        col_idx = 0 if center_x < mid_x else 1
        data.append({'box': box, 'cls': int(cls), 'col': col_idx})

    sorted_data = sorted(data, key=lambda x: (x['col'], x['box'][1]))

    for i, item in enumerate(sorted_data):
        x1, y1, x2, y2 = map(int, item['box'])
        cls = item['cls']
        color = colors.get(cls, (128, 128, 128))
        
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        label = f"{i+1} (C{cls})"
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.line(img, (int(mid_x), 0), (int(mid_x), h), (255, 100, 0), 2, cv2.LINE_AA)
    
    cv2.imwrite(DEBUG_OUTPUT, img)
    print(f"调试预览图已生成: {DEBUG_OUTPUT}")
    
    os.system(f"open {DEBUG_OUTPUT}")

if __name__ == '__main__':
    debug_yolo_boxes()
