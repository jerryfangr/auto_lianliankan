
# 自动连连看辅助

## 简介
- 基于opencv orb 图像相似度比较的连连看物理外挂

## 原理：
  1. PIL.ImageGrab.grab() 获取当前屏幕截图
  2. 裁剪出其中连连看的游戏消除块的区域，最终裁出每个消除块图片
  3. 根据图像相似度比较，获得所有类型的消除块图片，包括手动指定的消除后的空白块和障碍块图片
  4. 将图片更上一步的所有类型图片，相似度比较，生成数字类型矩阵
  5. 遍历数字类型矩阵，查看可以消除的方块坐标
  6. 模拟点击消除块

## 环境:
- python3.7+

## 安装:
```powershell
pip install -r requirements.txt
```

## 安装(Anconda):
```powershell
conda create -n game
conda activate game
pip install -r requirements.txt
```

## 使用

### 添加配置
> auto_lianliankan/config/setting.py

```python
# allow outside link
ALLOW_OUTSIDE_LINK = True

# image path of empty item
EMPTY_IMAGE_PATH = ["data/empty1.png"]
# image path of obstacles
BLOCK_IMAGE_PATH = ["data/block1.png"]

# game window title
WINDOW_TITLE = "MI 9 Transparent Edition"

# the interval of game click
LINK_INTERVAL = 0.1

# the MARGIN_LEFT of game area to the game window
MARGIN_LEFT = 56
# the MARGIN_HEIGHT of game area to the game window
MARGIN_HEIGHT = 244 + 28

# the number of the item in the horizontal direction
HORIZONTAL_NUM = 6
# the number of the item in the vertical direction
VERTICAL_NUM = 8

# the size of the item 
ITEM_WIDTH = ITEM_HEIGHT = 55

# cut the image noise, (LT)left top to (RB)right bottom
bx, by = 6, 6
```



## 开源协议:
- Apache Licence

