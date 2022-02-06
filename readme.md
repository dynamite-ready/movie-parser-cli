# NSFW Movie Parser CLI

An pair of CLI apps written in Python. 

- `process-video.py` - Can split a video into small video files, based on the camera changes found in the movie upload. It can also take an individual movie file, capture it's frames, and save them as `.jpg`. Uses the PySceneDetect heavily - https://github.com/dynamite-ready/PySceneDetect.

- `evaluate-images.py` - Takes a folder of image files, and will determine which of them are NSFW. It's based on ResNet50NSFW - https://github.com/emiliantolo/pytorch_nsfw_model

## 1: Dependencies

First and foremost, this is a Python repo, so you will need to install it if you don't already have it. The program(s) should build on both Python 2 & 3, but I would recommend version 3 - https://www.python.org/downloads/

If you want to build the standalone CLI executables, you will also need to install PyInstaller separately. You can install it with:

```
`pip install pyinstaller`

```

To run the app in any form, the two following binary files will have to be present in the CWD (Current Working Directory):

- `mkvmerge.exe` - Is used read and generate MP4 files. It can be found here - https://www.videohelp.com/software/MKVToolNix)

- `ResNet50_nsfw_model.pth` - The trained weights for the ResNet50NSFW model. The file can be found here - https://github.com/emiliantolo/pytorch_nsfw_model)

## 2: Installation

A list of all dependent Python modules can be found in `requirements.txt`. 
To install the app, you should be able to use the following command:

```
`python -m pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html`

```

These modules are interdependent, so you need to be wary when they're updated. PyTorch moves particularly fast.

## Using the app

`process-video.py / process-video.exe`:

```
usage: process-video.py [-h] [--images] [--skip [SKIP]] [--ipath [IPATH]] file

positional arguments:
  file             A path to the video file you wish to split into smaller videos

optional arguments:
  -h, --help       show this help message and exit
  --images         When set the program will instead capture jpg images from video. Should be used with `--ipath` and `--skip`
  --skip [SKIP]    Number of frames to skip when extracting images
  --ipath [IPATH]  Folder in which to store jpgs when using the `--images` option
```

`evaluate-images.py / evaluate-images.exe`:

```
usage: evaluate-images.py [-h] [--model [MODEL]] folder

positional arguments:
  folder           A folder of images to test for NSFW content. Outputs a single floating point number (0.3+ is probably mucky)

optional arguments:
  -h, --help       show this help message and exit
  --model [MODEL]  `ResNet50_nsfw_model.pth` file location
```

## Build the standalone CLI

`build-exe.sh` or `build-exe.bat` can be used to create a standalone executable CLI app.
You will need to install PyInstaller to run it (see the `dependencies` section).

## Notes

- CUDA PyTorch would have been nice, but it's a bloated brick of code
- Take care with the size of the files and folders you want to process
- Is tightly coupled to my Movie Parser GUI project - https://github.com/dynamite-ready/movie-parser-cli