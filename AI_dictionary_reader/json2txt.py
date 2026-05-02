import os
import json

def convert_to_yolo_format(json_data, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    W, H = 1200, 1600
    
    for page_name, entries in json_data.items():
        file_base_name = page_name.replace(".png", "")
        with open(f"{output_dir}/{file_base_name}.txt", "w") as f:
            for entry in entries:
                cls_id = entry.get("class", 0) 
                
                box = entry["box"]
                x_center = (box[0] + box[2]) / 2 / W
                y_center = (box[1] + box[3]) / 2 / H
                width = (box[2] - box[0]) / W
                height = (box[3] - box[1]) / H
                
                x_center = max(0, min(1, x_center))
                y_center = max(0, min(1, y_center))
                width = max(0, min(1, width))
                height = max(0, min(1, height))

                f.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

labels_json_path = "fake_dictionary_dataset/labels.json"
if os.path.exists(labels_json_path):
    with open(labels_json_path, "r", encoding='utf-8') as f:
        convert_to_yolo_format(json.load(f), "fake_dictionary_dataset/labels")
    print("JSON 已成功转换为 YOLO txt 格式。")
else:
    print(f"错误：找不到 {labels_json_path}")