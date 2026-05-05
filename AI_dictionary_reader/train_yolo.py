from ultralytics import YOLO

def train_dictionary_detector():

    model = YOLO('yolov8n.pt') 

    results = model.train(
        data='./dictionary_yolo/dataset.yaml', 
        epochs=150, 

        imgsz=960, 
        
        device='cpu', 

        batch=8,
        rect=True,
        overlap_mask=False,
        
        patience=30,
        mixup=0.1,
        project='shanghai_dict',
        name='v1_high_res'
    )

    metrics = model.val()
    print("训练完成！")

if __name__ == '__main__':
    train_dictionary_detector()