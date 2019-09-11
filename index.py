import argparse
import scenedetect
import os
import sys

from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
from scenedetect.frame_timecode import FrameTimecode
from scenedetect.stats_manager import StatsManager
from scenedetect.detectors import ContentDetector
# from scenedetect.video_splitter import VideoSplitter

# def splice_video(filepath, badgery):
#     print(filepath)

#     if(badgery):
#         print("||")
#         print(badgery)

def splice_video(video_path):
    print(video_path)
    # type: (str) -> List[Tuple[FrameTimecode, FrameTimecode]]
    video_manager = VideoManager([video_path])
    stats_manager = StatsManager()
    # Construct our SceneManager and pass it our StatsManager.
    scene_manager = SceneManager(stats_manager)

    # Add ContentDetector algorithm (each detector's constructor
    # takes detector options, e.g. threshold).
    scene_manager.add_detector(ContentDetector())
    base_timecode = video_manager.get_base_timecode()

    # We save our stats file to {VIDEO_PATH}.stats.csv.
    stats_file_path = '%s.stats.csv' % video_path

    scene_list = []

    try:
        # If stats file exists, load it.
        if os.path.exists(stats_file_path):
            # Read stats from CSV file opened in read mode:
            with open(stats_file_path, 'r') as stats_file:
                stats_manager.load_from_csv(stats_file, base_timecode)

        # Set downscale factor to improve processing speed.
        video_manager.set_downscale_factor()

        # Start video_manager.
        video_manager.start()

        # Perform scene detection on video_manager.
        scene_manager.detect_scenes(frame_source=video_manager)

        # Obtain list of detected scenes.
        scene_list = scene_manager.get_scene_list(base_timecode)
        # Each scene is a tuple of (start, end) FrameTimecodes.

        scenedetect.video_splitter.split_video_mkvmerge(str(video_path), scene_list, "badger", "tests", suppress_output=False)

        # print('List of scenes obtained:')
        # for i, scene in enumerate(scene_list):
        #     print(
        #         'Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
        #         i+1,
        #         scene[0].get_timecode(), scene[0].get_frames(),
        #         scene[1].get_timecode(), scene[1].get_frames(),))

        # # We only write to the stats file if a save is required:
        # if stats_manager.is_save_required():
        #     with open(stats_file_path, 'w') as stats_file:
        #         stats_manager.save_to_csv(stats_file, base_timecode)

    finally:
        video_manager.release()

    return scene_list

parser = argparse.ArgumentParser()

parser.add_argument("file", type=str, help="Video file to edit.")
parser.add_argument("--badgery", help="Extra badgery.", action="store_true")
args = parser.parse_args()

# Run the appropriate function (in this case showtop20 or listapps)
# if(args.file and args.badgery):
#     splice_video(args.file, "HELLO!")
# else:
#     splice_video(args.file, None)
    

splice_video(args.file)
