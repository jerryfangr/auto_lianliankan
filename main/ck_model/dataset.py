import os
import cv2
import torch
import random
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms


class ImageDataset(Dataset):
    def __init__(self, data):
        self.data = data  # 数据格式: [(combined_img, label), ...]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]


PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 数据预处理
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((49, 49)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def read_img(img):
    # 如果img1类型为字符串，则读取图片
    if isinstance(img, str):
        img = cv2.imread(img)

    # 转换颜色通道顺序 (BGR to RGB)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 应用变换
    return transform(img)


def format_data(img1_path, img2_path):
    img1 = read_img(img1_path)
    img2 = read_img(img2_path)
    return torch.cat((img1, img2), dim=0).unsqueeze(0)

def load_images(dataset_path):
    img_list = []

    # 遍历dataset文件夹下的所有子文件夹
    for img_type in os.listdir(dataset_path):
        img_folder = os.path.join(dataset_path, img_type)

        # 检查是否为文件夹
        if os.path.isdir(img_folder):
            # 遍历子文件夹中的所有图片
            group = []
            for img_name in os.listdir(img_folder):
                img_path = os.path.join(img_folder, img_name)

                # 检查是否为图片文件
                if img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    group.append(read_img(img_path))

            img_list.append(group)

    return img_list

# 标准随机数据集
def generate_random_pairs1(num_pairs, img_group_list):
    pairs = []
    total_round = num_pairs
    same_round = int(total_round * 0.3)

    label0, label1 = torch.tensor(0, dtype=torch.long), torch.tensor(1, dtype=torch.long)

    # 生成相同类别对
    for _ in range(same_round):
        img_group = random.choice(img_group_list)
        img1, img2 = random.sample(img_group, 2)
        pairs.append((torch.cat((img1, img2), dim=0), label1))

    # 剩余为不同类别对
    for _ in range(total_round - same_round):
        while True:
            img_group1, img_group2 = random.sample(img_group_list, 2)
            if img_group1 is not img_group2:  # 确保两个组不相同
                break
        img1, img2 = random.choice(img_group1), random.choice(img_group2)
        pairs.append((torch.cat((img1, img2), dim=0), label0))

    random.shuffle(pairs)
    return pairs

# 标准随机数据集 - 同时加正反图片集
def generate_random_pairs2(num_pairs, img_group_list):
    pairs = []
    total_round = int(num_pairs / 2)
    same_round = int(total_round * 0.3)

    label0, label1 = torch.tensor(0, dtype=torch.long), torch.tensor(1, dtype=torch.long)

    # 生成相同类别对
    for _ in range(same_round):
        img_group = random.choice(img_group_list)
        img1, img2 = random.sample(img_group, 2)
        pairs.append((torch.cat((img1, img2), dim=0), label1))
        pairs.append((torch.cat((img2, img1), dim=0), label1))

    # 剩余为不同类别对
    for _ in range(total_round - same_round):
        while True:
            img_group1, img_group2 = random.sample(img_group_list, 2)
            if img_group1 is not img_group2:  # 确保两个组不相同
                break
        img1, img2 = random.choice(img_group1), random.choice(img_group2)
        pairs.append((torch.cat((img1, img2), dim=0), label0))
        pairs.append((torch.cat((img2, img1), dim=0), label0))

    random.shuffle(pairs)
    return pairs

# 单独挑选的数据集
def generate_random_pairs3(num_pairs, img_group_list):
    pairs = []
    label0, label1 = torch.tensor(0, dtype=torch.long), torch.tensor(1, dtype=torch.long)
    # print('img_group_list', img_group_list[0][1])
    # raise Exception('stop')
    # 特别针对数据集
    for _ in range(num_pairs):
        gp1 = img_group_list[18]
        gp2 = img_group_list[37]

        g1_img1, g1_img2 = random.sample(gp1, 2)
        g2_img1, g2_img2 = random.sample(gp2, 2)

        pairs.append((torch.cat((g1_img1, g1_img2), dim=0), label1))
        pairs.append((torch.cat((g2_img1, g2_img2), dim=0), label1))

        pairs.append((torch.cat((g1_img1, g2_img1), dim=0), label0))
        pairs.append((torch.cat((g1_img2, g2_img2), dim=0), label0))

    random.shuffle(pairs)
    return pairs


def create_dataset(num_pair=3200, batch_size=32, num_workers=4):
    img_dataset = load_images(os.path.join(PROJECT_PATH, 'ck_model/train-data'))

    # 创建数据集实例 训练集和测试集
    train_dataset = ImageDataset(generate_random_pairs2(num_pair, img_dataset))
    test_dataset = ImageDataset(generate_random_pairs1(6000, img_dataset))

    train_loader = DataLoader(train_dataset, batch_size, shuffle=True, num_workers=num_workers)
    test_loader = DataLoader(test_dataset, batch_size, shuffle=False, num_workers=num_workers)

    return train_loader, test_loader


