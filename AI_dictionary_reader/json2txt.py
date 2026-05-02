import os

def convert_to_yolo_format(json_data, output_dir):
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    
    W, H = 1200, 1600
    
    for page_name, entries in json_data.items():
        with open(f"{output_dir}/{page_name}.txt", "w") as f:
            for entry in entries:
                box = entry["box"]
                x_center = (box[0] + box[2]) / 2 / W
                y_center = (box[1] + box[3]) / 2 / H
                width = (box[2] - box[0]) / W
                height = (box[3] - box[1]) / H
                
                f.write(f"0 {x_center} {y_center} {width} {height}\n")

import json
with open("fake_dictionary_dataset/labels.json", "r") as f:
    convert_to_yolo_format(json.load(f), "fake_dictionary_dataset/labels")
