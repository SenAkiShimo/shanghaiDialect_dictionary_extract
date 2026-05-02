from ultralytics import YOLO

def train_dictionary_detector():
    model = YOLO('yolov8n.pt')

    results = model.train(
        data='./dictionary_yolo/dataset.yaml', 
        epochs=100,
        imgsz=640,
        batch=16,
        device='cpu',           
        name='shanghai_dict_v1', 
        patience=20,
        close_mosaic=10,
        optimizer='AdamW',
        lr0=0.01
    )
    
    # 3. 验证
    metrics = model.val()
    print(f"训练完成！模型位置: runs/detect/shanghai_dict_v1/weights/best.pt")

if __name__ == '__main__':
    train_dictionary_detector()