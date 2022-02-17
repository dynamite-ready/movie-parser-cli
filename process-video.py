import argparse
import scenedetect
import os
import json
import cv2

from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
from scenedetect.frame_timecode import FrameTimecode
from scenedetect.stats_manager import StatsManager
from scenedetect.detectors import ContentDetector
from scenedetect import video_splitter

# This map function is a quick utility to transform the metadata output by SceneDetect
# into a format that's more readily convertible to JSON. The `scene_manager.get_scene_list`
# method outputs tuples, which are easy enough to work with in Python, but `Lists`
# are easier to convert to JSON.
def map_timecodes(timecode_item):
  return [timecode_item[0].get_timecode(), timecode_item[1].get_timecode()]

# Create a new folder without choking when it already exists.
def create_directory(path):
  if not os.path.exists(path):
    os.mkdir(path)

# This function doesn't actually use `SceneDetect`, but uses the OpenCV dependency
# that came with it. OpenCV is a well known open source project for the advanced manipulation
# of images. It contains a suite of algorithms for doing some very advanced things such as
# object detection. But here, I'm only using the `VideoCapture` method to take a snapshot
# of the frames in a video, and store them elsewhere for post processing later.
def get_images(video_path, output_path, nth_frame):
  # Create a folder to hold the images...
  create_directory(output_path)

  # Open the video file we want to process
  capture = cv2.VideoCapture(video_path)
  
  # We create an array of the images we have captured as a courtesy
  # It's not wholly necessary, but makes the files a little easier to find. :]
  image_file_list = []

  frame_counter = 0 # Count every frame in the video
  capture_counter = 0 # Count every nth_frame in the video
  
  # This `while` loop is used to step through every frame in the video
  while(capture.isOpened()):
    # Get the raw data of the current frame
    # I'm guessing each succesive call to `read` updates 
    # frame counter internal to Open CV. 
    # It's why I have to call it on every loop.
    # This function returns a Python tuple.
    # The first item tell you if the video is still open.
    # The second one gives you the frames content...
    (playing, frame) = capture.read()

    # If there's no data in frame variable (we've gone beyond the end of the video)
    # break the loop
    if(playing == False): break

    # Even small video files can contain thousands of images, and se a lot of memory.
    # What I want to do here, is only take a small sample of the images.
    # With the `nth_frame` variable/argument, if a video is 10 frames long, and
    # `nth_frame` is equal to `2`, I'm basically asking `get_images` to save
    # frames `2`, `4`, `6`, `8` and `10`. This should give me enough pictures
    # to check the content of a video, but also only take up half the space in memory
    if((frame_counter % nth_frame) == 0):
      image_file_name = output_path + 'tmp-img-' + str(capture_counter) + '.jpg' # Create a file name.
      cv2.imwrite(image_file_name, frame) # OpenCV method to write raw image data to a file name.
      image_file_list.append(image_file_name) # Add the file name to our `image_file_list`.
      capture_counter += 1 # Count the images we have currently stored.

    frame_counter += 1 # Also count how many frames of video we have read.

  capture.release() # When we have finished `watching` the video, close the capturing mechanism.
  cv2.destroyAllWindows() # Probably not necessary.

  # Take the list of captured images, and convert them to JSON.
  # Both humans and computers have very little trouble reading JSON...
  final_image_list = json.dumps(image_file_list)

  # At the end of processing, we show the user all files that have been save, with
  # the added bonus of printing a list that other computer programs can also consume.
  # Which will be useful a little later. 
  print(final_image_list)

# This function makes heavy use of SceneDetect to split a larger
# video into smaller ones, based on scene transitions and camera switches.
def split_video(video_path):
  # SceneDetect has a highly modular API. This hack uses version 0.5.*,
  # so there's a good chance that some of these comments won't
  # apply to version 0.6.*+. The VideoManager works a bit like `cv2.VideoCapture`.
  # It reads the video file, but can also split multiple videos
  # concurrently. For this program, we only need to split a single vid.
  video_manager = VideoManager([video_path])

  # Now we need a `SceneManager`... The SceneManager class/module contains methods
  # that do the actual scene detection.
  scene_manager = SceneManager()

  # Now we need to add a `Detector` to the `SceneManager`.
  # The `SceneManager.detectors` module contains two 'detectors'.
  # The `ContentDetector` is the fancy one.
  scene_manager.add_detector(ContentDetector())
  base_timecode = video_manager.get_base_timecode() # Start from 00:00:00

  # Just like the `get_images` function, I want to end the routine by printing out
  # a list to show what was done. Rather than file names in this case, I want to
  # display a list of where each camera transition starts and ends. Each of those
  # values correspond to each of the mini clips generated by `split_video`
  scene_list = []

  try:
    # Loads of getters and setters on these classes.
    # downscale_factor works like the `nth_frame` feature that I
    # use in `get_images`. You can give it an explicit value, but
    # if no argument is set, there's a fancy algorithm that automatically
    # manages frame skipping and optimisation.
    video_manager.set_downscale_factor()

    video_manager.start()

    # Here, we take the `video_manager`which we had constructed 
    # with the path to our `video_path`, and hand it to the `SceneManager` 
    # to actually detect scenes.
    scene_manager.detect_scenes(frame_source=video_manager)

    # This is nice. `scene_manager.get_scene_list` returns an array.
    # We don't need to play about with any loops.
    scene_list = scene_manager.get_scene_list(base_timecode)

    # This outputs a video for each detected scene. It uses the response from
    # `scene_manager.get_scene_list` to work out how to split the vid. There's a caveat here. 
    # `split_video_mkvmerge` relies on a third party program to split MP4 videos.
    # You can find the `mkvmerge.exe` in the MKVToolNix suite of video processing tools.
    # You'll then have to put this file in the same folder running the program. 
    # The split videos are also ouput to the CWD. There's no opportunity to move the files as yet.
    scenedetect.video_splitter.split_video_mkvmerge([video_path], scene_list, "tmp", "tmp-movie", suppress_output=True)

    # Make the scene list more JSON friendly (see - map_timecodes)
    mapped_scene_list = map(map_timecodes, scene_list)
    
    # Convert the `scene_list` to JSON.
    json_scene_list = json.dumps(list(mapped_scene_list))
     
    # Print out the JSON for consumption elsewhere...
    print(json_scene_list)
  finally:
    # Close the `VideoManager`... What about the other resources?
    video_manager.release()

# Initialise the argparser.
parser = argparse.ArgumentParser()
# `File` is a default argument. The CLI won't work without it.
# The program will either split a video file into smaller pieces, or
# take a video, and split it into images.
parser.add_argument("file", type=str, help="A path to the video file you wish to split into smaller videos")
# The next four arguments are optional. 
# When we call the program with `--images`, it will spilt a video into images.
# `action=store_true` creates an optional boolean argument that's always true.
parser.add_argument("--images", help="When set the program will instead capture jpg images from video. Should be used with `--ipath` and `--skip`", action='store_true')
parser.add_argument("--skip", help="Number of frames to skip when extracting images", nargs='?', type=int, const=5, default=5)
parser.add_argument("--ipath", help="Folder in which to store jpgs when using the `--images` option", nargs='?', type=str, const="./tmp-images/", default="./tmp-images/")

args = parser.parse_args()

if(args.file):
  if(args.images): get_images(args.file, args.ipath, args.skip)
  else: split_video(args.file)