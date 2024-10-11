import torch.nn as nn

# 定义一个简单的卷积神经网络
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(6, 64, kernel_size=5),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, stride=2),
            nn.Conv2d(64, 128, kernel_size=5),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, stride=2),
            nn.Flatten(),
            nn.Linear(128 * 9 * 9, 1024),  # 修改这里
            nn.ReLU(inplace=True),
            nn.Linear(1024, 1),  # 输出单个值表示相似度得分
        )

    def forward(self, x):
        return self.cnn(x)
