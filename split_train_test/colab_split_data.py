import os
import shutil
import random

# 由使用者輸入來源資料夾參數（例如：112598018）
folder_param = input("請輸入來源資料夾參數 (例如 112598018): ").strip()

# 定義來源資料夾與目標資料夾
source_dir1 = folder_param
source_dir2 = "Noto_Sans_TC_JPG"
target_dir1 = os.path.join("train", "TargetImage", folder_param)
target_dir2 = os.path.join("train", "ContentImage")

# 若目標資料夾不存在，則建立目錄
os.makedirs(target_dir1, exist_ok=True)
os.makedirs(target_dir2, exist_ok=True)

def is_chinese(char):
    """
    檢查單一字元是否屬於中文範圍 (主要是 CJK 統一表意文字 U+4E00 ~ U+9FFF)
    """
    return '\u4e00' <= char <= '\u9fff'

def decode_filename(filename):
    """
    將符合格式 "U+XXXX" 的檔名轉換為對應的字元
    """
    base, _ = os.path.splitext(filename)
    if base.startswith("U+"):
        try:
            # 取得 "U+" 後面的16進位數字，並轉成整數，再轉成 Unicode 字元
            code = base[2:]
            char = chr(int(code, 16))
            return char
        except ValueError:
            return None
    return None

def get_chinese_images(directory):
    """
    掃描目錄中的圖片，返回符合檔名 (U+XXXX 表示中文漢字) 的一個字典
    結構為 {漢字: 檔案完整路徑}。
    若同一漢字有多個檔案，本範例只取第一個。
    """
    images = {}
    # 讀取目錄中所有檔案
    for file in os.listdir(directory):
        # 只處理 png, jpg, jpeg 等圖片
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            char = decode_filename(file)
            if char and is_chinese(char):
                # 假如該漢字已經出現過，就不再覆蓋
                if char not in images:
                    images[char] = os.path.join(directory, file)
    return images

# 取得兩個資料夾中符合條件的圖片字典
images1 = get_chinese_images(source_dir1)
images2 = get_chinese_images(source_dir2)

# 找出兩個資料夾中都存在的漢字檔案（交集）
common_chars = list(set(images1.keys()) & set(images2.keys()))
print("共同符合條件的中文檔案數量:", len(common_chars))

# 決定挑選 800 張，若不足 800 張則取現有數量
select_count = min(800, len(common_chars))
selected_chars = random.sample(common_chars, select_count)
print("隨機挑選的中文檔案:", selected_chars)

# 依據挑選結果進行檔案複製與重新命名
for char in selected_chars:
    # 處理來源目錄1，目標檔名格式: 輸入參數+漢字.jpg
    source_path1 = images1[char]
    new_name1 = f"{folder_param}+{char}.jpg"
    target_path1 = os.path.join(target_dir1, new_name1)
    shutil.copy2(source_path1, target_path1)
    
    # 處理來源目錄2，目標檔名格式: 漢字.jpg
    source_path2 = images2[char]
    new_name2 = f"{char}.jpg"
    target_path2 = os.path.join(target_dir2, new_name2)
    shutil.copy2(source_path2, target_path2)

print("檔案複製與重新命名完成！")
