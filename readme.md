# Notes...

- Using PyInstaller to create .exe `pyinstaller --onefile index.py / whatever.py`
- `index.py` will split videos into scenes / shots, and also split a video into jpgs
- `evaluate-images.py` will take a collection of images, and examine them to see if they contain smut
- To split a video `python process-video.py --images file c:\movie-parser\public\tmp\tmp-001-1570532655600 --ifolder ./temporary/`