from ultralytics import YOLO

def train_dictionary_detector():
    model = YOLO('yolov8n.pt')

    results = model.train(
        data='./dictionary_yolo/dataset.yaml',
        epochs=50,
        imgsz=640,
        batch=8,
        device='cpu',
        name='shanghai_dict_v1'
    )
    
    metrics = model.val()
    print(f"训练完成，模型保存在 runs/detect/shanghai_dict_v1/weights/best.pt")

if __name__ == '__main__':
    train_dictionary_detector()
