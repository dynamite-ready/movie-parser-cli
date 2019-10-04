import glob
import argparse
import json

from nsfw_detector import NSFWDetector

def evaluate_image_batch(folder):
    image_list = glob.glob("./" + folder + "/*.jpg")

    detector_mobilenet = NSFWDetector('./nsfw_mobilenet2.224x224.h5')
    # Predict single image

    prediction = detector_mobilenet.predict(image_list, image_size=(224,224))

    print(prediction)

    return prediction

parser = argparse.ArgumentParser()

parser.add_argument("folder", type=str, help="Folder of generated or extant images to test for smut.")
args = parser.parse_args()

evaluate_image_batch(args.folder)