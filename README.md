# Image-Compression
圖片壓縮器 (含HEIC)

可使用拖曳、直接運行的方式進行圖片處理壓縮，如若為 HEIC 則會轉檔為JPG在進行壓縮。

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
