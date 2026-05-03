import os
import json

def convert_to_yolo_format(json_data, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    W, H = 1200, 1600
    
    for page_name, labels in json_data.items():
        file_base_name = page_name.split('.')[0] 
        
        txt_path = os.path.join(output_dir, f"{file_base_name}.txt")
        
        with open(txt_path, "w") as f:
            for item in labels:
                cls_id = item.get("class", 0)
                box = item["box"]  # [x1, y1, x2, y2]

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
output_label_dir = "fake_dictionary_dataset/labels"

if os.path.exists(labels_json_path):
    with open(labels_json_path, "r", encoding='utf-8') as f:
        convert_to_yolo_format(json.load(f), output_label_dir)
    print(f"转换成功！YOLO 标签已存入: {output_label_dir}")
else:
    print(f"错误：找不到 {labels_json_path}")