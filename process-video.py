import argparse
import scenedetect
import os
import sys
import json
import cv2

from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
from scenedetect.frame_timecode import FrameTimecode
from scenedetect.stats_manager import StatsManager
from scenedetect.detectors import ContentDetector
# from scenedetect.video_splitter import VideoSplitter

def map_timecodes(timecode_item):
    return [timecode_item[0].get_timecode(), timecode_item[1].get_timecode()]

def get_images(video_path, nth, folder):
    print(folder)
    print(nth)

    os.mkdir(folder)

    # Opens the Video file
    cap = cv2.VideoCapture(video_path)

    i = 0
    k = 0

    while(cap.isOpened()):
        ret, frame = cap.read()
        
        if(ret == False): break
        if((i % nth) == 0):
            # Only parse every 5 frame (make this tuneable, obvs).
            cv2.imwrite(folder + 'tmp-img-' + str(k) + '.jpg', frame)
            k += 1
        
        i += 1

    cap.release()
    cv2.destroyAllWindows()    

def splice_video(video_path):
    video_manager = VideoManager([video_path])
    stats_manager = StatsManager()

    # Construct our SceneManager and pass it our StatsManager.
    scene_manager = SceneManager(stats_manager)

    # Add ContentDetector algorithm (each detector's constructor
    # takes detector options, e.g. threshold).
    scene_manager.add_detector(ContentDetector())
    base_timecode = video_manager.get_base_timecode()

    scene_list = []

    try:
        # Set downscale factor to improve processing speed.
        video_manager.set_downscale_factor()

        # Start video_manager.
        video_manager.start()

        # Perform scene detection on video_manager.
        scene_manager.detect_scenes(frame_source=video_manager)

        # Obtain list of detected scenes.
        scene_list = scene_manager.get_scene_list(base_timecode)
        # Each scene is a tuple of (start, end) FrameTimecodes.
        
        # Output the edited vids.
        scenedetect.video_splitter.split_video_mkvmerge([video_path], scene_list, "tmp", "tmp-movie", suppress_output=False)

        mapped_scene_list = map(map_timecodes, scene_list)
        json_scene_list = json.dumps(list(mapped_scene_list))

        print(json_scene_list)
    finally:
        video_manager.release()

    return scene_list

parser = argparse.ArgumentParser()

parser.add_argument("file", type=str, help="Video file to edit.")
parser.add_argument("--images", help="Extract images from video.")
parser.add_argument("--nth", help="Number of frames to skip, when extracting images.", nargs='?', const=5, type=int, default=5) # Test option.
parser.add_argument("--ifolder", help="Folder in which to place derived images.", nargs='?', const="./tmp/", type=str, default="./tmp/")
args = parser.parse_args()

if(args.file and args.images):
    get_images(args.file, args.nth, args.ifolder)
elif(not args.images):
    splice_video(args.file)
