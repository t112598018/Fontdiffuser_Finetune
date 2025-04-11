import os
import json
import shutil
from tqdm import tqdm

def reset_directories():
    """
    重置 train 和 test 資料夾，若存在則先刪除再重新建立
    """
    for folder in ["train", "test"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)

def load_train_test_sets():
    """
    讀取 train.txt 和 test.txt，獲取訓練與測試的字元清單
    """
    if not os.path.exists("train.txt") or not os.path.exists("test.txt"):
        raise FileNotFoundError("找不到 train.txt 或 test.txt，請先準備這些文件")

    with open("train.txt", "r", encoding="utf-8") as f:
        train_characters = f.read().splitlines()

    with open("test.txt", "r", encoding="utf-8") as f:
        test_characters = f.read().splitlines()

    return train_characters, test_characters

def copy_images_based_on_labels(ContentImage, TargetImage, ID):
    """
    根據 train.txt 和 test.txt 指定的字元，將對應圖片從 ContentImage 和 TargetImage 複製到對應的資料夾中
    並檢查每張圖片是否存在，若缺漏則列出警告
    """
    train_characters, test_characters = load_train_test_sets()

    # 確保目標資料夾存在
    os.makedirs("train/ContentImage", exist_ok=True)
    os.makedirs("train/TargetImage", exist_ok=True)
    os.makedirs("test", exist_ok=True)
    os.makedirs(f"test/{ID}", exist_ok=True)
    os.makedirs(f"train/TargetImage/{ID}", exist_ok=True)

    # 處理訓練集
    print("保存訓練集圖片...")
    for char in tqdm(train_characters, desc="訓練集進度"):
        unicode_filename = f"U+{ord(char):04X}.jpg"

        # 複製 ContentImage
        for images_directory in ContentImage:
            image_path = os.path.join(images_directory, unicode_filename)
            destination_path = f"train/ContentImage/{char}.jpg"
            if os.path.exists(image_path):
                shutil.copy(image_path, destination_path)
            else:
                print(f"缺少 ContentImage：{image_path}")

        # 複製 TargetImage
        for images_directory in TargetImage:
            image_path = os.path.join(images_directory, unicode_filename)
            destination_path = f"train/TargetImage/{ID}/{ID}+{char}.jpg"
            if os.path.exists(image_path):
                shutil.copy(image_path, destination_path)
            else:
                print(f"缺少 TargetImage（訓練集）：{image_path}")

    # 處理測試集
    print("保存測試集圖片...")
    for char in tqdm(test_characters, desc="測試集進度"):
        unicode_filename = f"U+{ord(char):04X}.jpg"

        for images_directory in TargetImage:
            image_path = os.path.join(images_directory, unicode_filename)
            destination_path = f"test/{ID}/{ID}+{char}.jpg"
            if os.path.exists(image_path):
                shutil.copy(image_path, destination_path)
            else:
                print(f"缺少 TargetImage（測試集）：{image_path}")

    print(f"訓練集: {len(train_characters)} 個字元已保存到 train/")
    print(f"測試集: {len(test_characters)} 個字元已保存到 test/")

# -------------------- 主程式流程 --------------------

# 步驟一：重置 train/test 資料夾
reset_directories()

# 步驟二：指定圖片來源
characters_file = "CP950.json"  # 字元資料 JSON 檔
ContentImage = ["./Noto_Sans_TC_JPG"]  # ContentImage 資料夾路徑
ID = "112598018"  # 目標 ID 清單（從資料夾名稱取得）

# 從資料夾讀取所有風格子目錄作為 TargetImage
TargetImage = ["./112598018_JPG"]

# 步驟三：根據 train.txt/test.txt 複製對應圖片到資料夾
copy_images_based_on_labels(ContentImage, TargetImage, ID)
