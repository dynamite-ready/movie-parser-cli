# Movie Parser CLI

A command line application which takes a video filepath as an input, and determines which frames in the video file are NSFW.
It's based on this Pytorch model - https://github.com/emiliantolo/pytorch_nsfw_model and also uses the PySceneDetect project 
heavily - https://github.com/dynamite-ready/PySceneDetect.

It's actually a suite of two CLI programs. 

- `process-video.py`: Splits a video in to smaller ones, based on scene transitions, and turn vids into a folder of images.
- `evaluate-images.py`: Can take a folder of images and tell you if it contains porn.

Some of the results of the smut evaluation process can be particularly funny. 
Hilary Hahn in concert will trigger it...

It's used as a component of the Movie Parser project - https://github.com/dynamite-ready/movie-parser

## Notes

- Using PyInstaller `pip install pyinstaller` to create .exe `pyinstaller --onefile index.py / whatever.py`
- `build-exe.sh` or `build-exe.bat` can also be used perform the step above.
- `index.py` will split videos into scenes / shots, and also split a video into jpgs
- `evaluate-images.py` will take a folder of images, and examine them to see if they contain smut
- To split a video `python process-video.py --images file c:\movie-parser\public\tmp\tmp-001-1570532655600 --ipath ./temporary/`
- install with `python -m pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html`
- CUDA PyTorch would have been nice, but it's a bloated brick of code.