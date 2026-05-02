import cv2
import os
from ultralytics import YOLO

MODEL_PATH = './runs/detect/shanghai_dict_v1/weights/best.pt'
IMAGE_PATH = './picture/temp_page_8.png'
DEBUG_OUTPUT = './debug_visual.png'

def debug_yolo_boxes():
    model = YOLO(MODEL_PATH)
    
    img = cv2.imread(IMAGE_PATH)
    if img is None:
        print(f"无法读取图片: {IMAGE_PATH}")
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

    print(f"AI 总共找到了 {len(sorted_boxes)} 个框")

    for i, box in enumerate(sorted_boxes):
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.putText(img, str(i+1), (x1 - 40, y1 + 25), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)


    cv2.line(img, (int(mid_x), 0), (int(mid_x), h), (255, 0, 0), 1)


    cv2.imwrite(DEBUG_OUTPUT, img)
    print(f"调试预览图已生成: {DEBUG_OUTPUT}")
    
    os.system(f"open {DEBUG_OUTPUT}")

if __name__ == '__main__':
    debug_yolo_boxes()
