# The optional `--onefile` flag tells PyInstaller to package your
# entire Python program, and all of it's dependencies into one file.
# This option worked for my `process-video.py`, but not the `evaluate-images.py`
# file. The main difference between the two programs, is the use of Pytorch
# When packaging `evalaute-images.py` without the `--onefile` flag, it works
# but the executable file will be accompanied by a huge folder of dependent Python
# modules. I would guess there are settings to fix this issue, but was unable to
# find a perscription online. ¯\_(ツ)_/¯

python -m PyInstaller --onefile process-video.py
python -m PyInstaller evaluate-images.py