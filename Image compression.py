from PIL import Image
from pillow_heif import register_heif_opener
import os
import sys

# 獲取執行文件所在的文件夾路徑
executable_dir = os.path.dirname(sys.executable)

def convert_heic_to_jpg(input_folder, output_folder):
    register_heif_opener()

    # 檢查輸出資料夾是否存在，如果不存在則建立
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 取得來源資料夾中的所有檔案
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".heic"):  # 確認檔案是 HEIC 格式
                heic_file_path = os.path.join(root, file)
                output_jpg_path = os.path.join(output_folder, os.path.splitext(file)[0] + ".jpg")

                # 使用 Pillow 的 HEIF 插件讀取 HEIC 檔案
                heic_image = Image.open(heic_file_path)

                # 儲存為 JPEG 格式
                heic_image.save(output_jpg_path, format="JPEG")

                # 取得檔案名稱
                heic_file_name = os.path.basename(heic_file_path)
                output_jpg_name = os.path.basename(output_jpg_path)

                print(f"成功將 {heic_file_name} 轉換為 {output_jpg_name}")

                # 壓縮 JPEG 檔案
                compress_image(output_jpg_path, output_folder)

    return True

def compress_image(image_path, output_folder, quality=85):
    # 檢查並創建輸出檔案夾
    current_path = os.path.dirname(os.path.abspath(__file__))
    output_folder_path = os.path.join(current_path, output_folder)
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # 獲取檔案信息
    file_name, extension = os.path.splitext(os.path.basename(image_path))

    # 確保是圖片檔案
    if extension.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        output_path = os.path.join(output_folder_path, f"{file_name}{extension}")
        image = Image.open(image_path)

        original_size = int(os.path.getsize(image_path)) // 1024
        compressed_size = original_size  # 初始壓縮大小等於原始大小

        # 叠代進行壓縮，直到壓縮後大小小於原始大小或品質低於25
        while compressed_size >= original_size and quality >= 25:
            # 在每次壓縮前更新壓縮後檔案的大小
            image.save(output_path, optimize=True, quality=quality)
            compressed_size = int(os.path.getsize(output_path)) // 1024

            if compressed_size >= original_size:  # 檢查壓縮後大小是否大於原始大小
                if quality > 45:
                    quality -= 20
                else:
                    quality -= 10

                # 在每次壓縮後重新獲取壓縮後檔案的大小
                compressed_size = int(os.path.getsize(output_path)) // 1024

        saved_size = original_size - compressed_size
        saved_percentage = round((saved_size / original_size) * 100, 1)

        # 顯示壓縮結果
        print(f"圖片名稱: {file_name}{extension}")
        print(f"圖片大小: {original_size:.1f} KB >> {compressed_size:.1f} KB")
        print(f"縮減容量: {saved_size:.1f} KB")
        print(f"縮減比例: {saved_percentage}%")
        print("---------------------------------------------------------------")

        return original_size, compressed_size
    
    elif extension.lower() == '.heic':  # 檢查是否為 HEIC 格式
        print(f"檢測到 {file_name}.HEIC 格式圖片，請將其移動到 input 資料夾並直接運行本程序。")
        print("---------------------------------------------------------------")
        return 0, 0  # 直接返回，避免繼續程式流程

    else:
        # 非圖片檔案的提示
        print(f"{file_name}{extension} 不是圖片檔案，已跳過壓縮動作。")
        print("---------------------------------------------------------------")
        return 0, 0

def compress_images_in_folder(input_folder, output_folder, quality=85):
    # 處理 HEIC 檔案轉換為 JPEG
    if not convert_heic_to_jpg(input_folder, output_folder):
        print("未能完成 HEIC 檔案轉換，請檢查程式及檔案路徑。")
        print("---------------------------------------------------------------")
        return

    current_path = os.path.dirname(os.path.abspath(__file__))
    input_folder_path = os.path.join(current_path, input_folder)
    output_folder_path = os.path.join(current_path, output_folder)

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    total_original_size_kb = 0
    total_compressed_size_kb = 0

    image_files = [f for f in os.listdir(input_folder_path) if os.path.isfile(os.path.join(input_folder_path, f))]

    for image_file in image_files:
        input_path = os.path.join(input_folder_path, image_file)

        # 取得副檔名判斷
        file_name, file_extension = os.path.splitext(input_path)
        file_extension = file_extension.lower()

        try:
            image = Image.open(input_path)
        except (IOError, OSError, Image.UnidentifiedImageError):
            print(f"{image_file} 不是圖片檔案，已跳過壓縮動作。")
            print("---------------------------------------------------------------")
            continue

        if image.format.lower() in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
            output_path = os.path.join(output_folder_path, f"{image_file}")

            # 壓縮單個圖片
            original, compressed = compress_image(input_path, output_folder, quality)

            total_original_size_kb += original
            total_compressed_size_kb += compressed

        else:
            # 如果是 heic 則不給予反饋 因為已經處裡完成
            if file_extension != '.heic':
                print(f"{image_file} 不是圖片檔案，已跳過壓縮動作。")
                print("---------------------------------------------------------------")

    # 顯示整個資料夾的壓縮結果
    total_saved_mb = (total_original_size_kb - total_compressed_size_kb) / 1024
    total_saved_percentage = round((total_saved_mb / (total_original_size_kb / 1024)) * 100, 1)

    print(">>> .HEIC 容量不列入計算內 <<<")
    print("")
    print("\n原始總容量:", round(total_original_size_kb / 1024, 1), "MB")
    print("壓縮總容量:", round(total_compressed_size_kb / 1024, 1), "MB")
    print("總計縮減量:", round(total_saved_mb, 1), "MB")
    print("總壓縮比例:", total_saved_percentage, "%")


try:
    if len(sys.argv) > 1:
        output_folder_name = 'output'
        total_original_drag = 0
        total_compressed_drag = 0

        for image_path in sys.argv[1:]:
            if os.path.isfile(image_path):
                original, compressed = compress_image(image_path, output_folder_name, quality=85)
                total_original_drag += original
                total_compressed_drag += compressed
            else:
                print(f"檔案 {image_path} 不存在，已跳過壓縮動作。")

        if total_original_drag > 0:
            total_saved_drag = total_original_drag - total_compressed_drag
            total_saved_percentage_drag = round((total_saved_drag / total_original_drag) * 100, 1)
            print("\n總原始容量:", round(total_original_drag / 1024, 1), "MB")
            print("總壓縮容量:", round(total_compressed_drag / 1024, 1), "MB")
            print("總計縮減量:", round(total_saved_drag / 1024, 1), "MB")
            print("總壓縮比例:", total_saved_percentage_drag, "%")
    else:
        # 確定目錄路徑(EXE版本)
        input_folder_name = os.path.join(executable_dir, 'input')
        output_folder_name = os.path.join(executable_dir, 'output')

        # 確定目錄路徑(純py版本)
        # input_folder_name = 'input'  # 設置輸入資料夾名稱
        # output_folder_name = 'output'  # 設置輸出資料夾名稱
        
        compress_images_in_folder(input_folder_name, output_folder_name, quality=85)

except Exception as e:
    if str(e) != 'float division by zero':
        if str(e)[:24] == "[WinError 3] 系統找不到指定的路徑。":
            print('請確認 input 資料夾是否正確存在。')
        else:
            print(f"程式出現錯誤：{e}")
        
print("")
os.system('pause')
