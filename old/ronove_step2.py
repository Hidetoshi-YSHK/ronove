import glob
import os
import re
import csv
from PIL import Image, ImageFilter

INPUT_FILE = "intermediate.csv"
INPUT_FILE_ENCODING = "utf_8"
OUTPUT_FILE = "output.csv"
OUTPUT_FILE_ENCODING = "utf_8"
# 画像ファイルディレクトリ
IMAGE_FILE_DIR = "target1900_image"
# 処理済み画像ファイルにつけられる接頭辞
IMAGE_FILE_PREFIX = "target1900"
# 画像サイズ指定
IMAGE_RESIZE_TO = (200, 200)

def main():
    files = glob.glob(IMAGE_FILE_DIR + "/*")
    file_name_dict = {}
    for file in files:
        print(file)
        basename = os.path.basename(file)
        splitext = os.path.splitext(basename)

        # 処理済みの画像はリサイズしない
        m = re.match(r"^" + re.escape(IMAGE_FILE_PREFIX) + r"_(.+)", splitext[0])
        if m:
            # キー：単語　値：処理済みファイル名
            word = m.group(1)
            file_name_dict[word] = basename
            continue

        # 画像をリサイズして接頭辞をつけてJPEGで保存
        image = Image.open(file)
        image.thumbnail(IMAGE_RESIZE_TO)
        image = image.convert('RGB')
        dest_file_name = IMAGE_FILE_PREFIX + "_" + splitext[0] + ".jpg"
        image.save(IMAGE_FILE_DIR + "/" + dest_file_name, quality=50)
        # 元画像を削除
        os.remove(file)

        # キー：単語　値：処理済みファイル名
        word = splitext[0]
        file_name_dict[word] = dest_file_name
    
    csv_data = []
    with open(INPUT_FILE, encoding=INPUT_FILE_ENCODING) as f:
        reader = csv.reader(f)
        for row in reader:
            word = row[0]
            if word in file_name_dict:
                row[4] = "<img src='{}'>".format(file_name_dict[word])
            csv_data.append(row)

    with open(OUTPUT_FILE, 'w', encoding=OUTPUT_FILE_ENCODING, newline="") as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

main()
