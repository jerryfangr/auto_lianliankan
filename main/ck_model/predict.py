import os
import torch
from ck_model.network import SimpleCNN
from ck_model.dataset import format_data

# 检查是否有可用的GPU
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleCNN().to(device)
is_loaded = False


def load_model(model_epoch=0, force_reload=False, device='cuda'):
    global model, is_loaded
    if is_loaded and not force_reload:
        return model
    else:
        if force_reload:
            model = SimpleCNN().to(device)
        model_path = os.path.join(PROJECT_PATH, f'ck_model/checkpoints/ep_{model_epoch}.pth')
        print(f'Loading model from {model_path}')
        model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
        model.eval()
        is_loaded = True
        return model

# 预处理图像
def preprocess_image(img1, img2):
    return format_data(img1, img2).to(device)

# 使用模型进行预测
def predict_same2(img1, img2, model, debug_mode=False):
    # 前向传播
    with torch.no_grad():
        output1 = model(preprocess_image(img1, img2)).squeeze()
        predicted1 = torch.round(torch.sigmoid(output1))

    return output1.item() if debug_mode else int(predicted1.item())

# 使用模型进行预测
def predict_same(img1, img2, model, debug_mode=False):
    # 前向传播
    with torch.no_grad():
        output1 = model(preprocess_image(img1, img2)).squeeze()
        predicted1 = torch.round(torch.sigmoid(output1))
    
    if int(predicted1.item()) == 1:
        return output1.item() if debug_mode else 1

    with torch.no_grad():
        output2 = model(preprocess_image(img2, img1)).squeeze()
        predicted2 = torch.round(torch.sigmoid(output2))

    if debug_mode:
        return output1.item(), output2.item()
    
    return int(predicted2.item())

