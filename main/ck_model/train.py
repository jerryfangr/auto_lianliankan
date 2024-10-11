import os
import shutil
import torch
import torch.nn as nn
import torch.optim as optim
from ck_model.dataset import create_dataset
from ck_model.network import SimpleCNN

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model = None

def train(epochs=5, save_interval=1, load_model=0, train_data_size=3800, learn_rate=0.001, device='cuda'):
    global model

    # 创建数据集 DataLoader
    train_loader, test_loader = create_dataset(train_data_size, batch_size=32, num_workers=2)

    # 模型保存路径
    model_save_dir = os.path.join(PROJECT_PATH, 'ck_model/checkpoints')
    os.makedirs(model_save_dir, exist_ok=True)

    # 初始化载入模型
    if model == None:
        # 检查是使用的计算设备
        device = 'cpu' if device == 'cpu' or not torch.cuda.is_available() else 'cuda'

        model = SimpleCNN().to(device)
        # 加载最后保存的模型
        if os.path.exists(os.path.join(model_save_dir, f'ep_{load_model}.pth')):
            print(f'Init load model: ep_{load_model}')
            model.load_state_dict(torch.load(os.path.join(model_save_dir, f'ep_{load_model}.pth'), map_location=device, weights_only=True))

    # 初始化损失函数和优化器
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=learn_rate)

    # 训练循环
    last_save_epoch = 0
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device).float()
            optimizer.zero_grad()
            outputs = model(inputs).squeeze()
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
        
        final_loss = running_loss / len(train_loader)
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {final_loss:.5f}')

        # 每50轮保存一次模型
        if (epoch + 1) % save_interval == 0:
            last_epoch = epoch + 1
            model_path = os.path.join(model_save_dir, f'ep_{last_epoch}.pth')
            torch.save(model.state_dict(), model_path)
        
        if final_loss < 0.0001:
            print(f'Loss < 0.0001, end training')
            break

    model.eval()  # 设置模型为评估模式
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images).squeeze()
            # 应用sigmoid并四舍五入到最接近的整数(0或1)
            predictions = torch.round(torch.sigmoid(outputs))
            total += labels.size(0)
            correct += (predictions == labels).sum().item()  # 计算正确预测的数量

    return last_epoch, 100 * correct / total


def save_best_model(epochs=5, target=0):
    model_dir = os.path.join(PROJECT_PATH, 'ck_model/checkpoints')

    good_model_path = os.path.join(model_dir, f'ep_{epochs}.pth')
    saved_model_path = os.path.join(model_dir, f'ep_{target}.pth')

    shutil.copy(good_model_path, saved_model_path)
