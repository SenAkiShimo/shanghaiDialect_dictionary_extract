import json
import cv2
import os
import numpy as np

IMG_DIR = "./fake_dictionary_dataset"
LABEL_PATH = "./fake_dictionary_dataset/labels.json" 
SAVE_DEBUG_PATH = "./debug_result.jpg"

def verify_labels():
    if not os.path.exists(LABEL_PATH):
        print(f"错误：找不到 JSON 文件 {LABEL_PATH}")
        return
    
    with open(LABEL_PATH, 'r', encoding='utf-8') as f:
        all_data = json.load(f)

    target_page = list(all_data.keys())[0]
    labels = all_data[target_page]
    img_name = f"{target_page}.jpg"
    img_path = os.path.join(IMG_DIR, img_name)

    if not os.path.exists(img_path):
        print(f"错误：找不到图片 {img_path}")
        return

    img = cv2.imread(img_path)
    if img is None:
        print("图片读取失败")
        return

    print(f"正在校验: {img_name}, 共有 {len(labels)} 个标注框")

    for item in labels:
        box = item["box"]
        cls = item["class"]

        p1 = (int(box[0]), int(box[1]))
        p2 = (int(box[2]), int(box[3]))

        color_map = {
        0: (0, 255, 0),
        1: (255, 0, 0),
        2: (255, 255, 0),
        3: (0, 165, 255)
        }

        color = color_map.get(cls, (255, 255, 255))

        cv2.rectangle(img, p1, p2, color, 2)
        

        cv2.putText(img, str(cls), (p1[0], p1[1]-5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)


    cv2.imwrite(SAVE_DEBUG_PATH, img)
    print(f"校验图片已生成至: {SAVE_DEBUG_PATH}")

    cv2.imshow("Debug", img)
    cv2.waitKey(0)

if __name__ == "__main__":
    verify_labels()
