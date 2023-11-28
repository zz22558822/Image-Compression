# Image-Compression
圖片壓縮器 (含HEIC)

拖曳尚未增加HEIC的轉檔，請放置在input資料夾當中直接運行 Image compression.py。

## 使用前需安裝的庫
```安裝前的庫
python -m pip install --upgrade pip
pip install Pillow
pip install pillow-heif
```

## 打包的指令
```打包的指令
pyinstaller -i LOGO.ico '.\Image compression.py' -n "Image compression" --onefile
```
