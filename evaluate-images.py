import os
import argparse
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
from torchvision import transforms, models
from PIL import Image
from torch.autograd import Variable

# Initialize an instance of the frozen model
# --------------------------------------------------------------
# --------------------------------------------------------------

# This is prepping the image with PyTorch's image tools.
test_transforms = transforms.Compose(
    [
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225])                                
    ]
)

# Getting a prerolled ResNet50 instance out of PyTorch
model = models.resnet50()

# Hmm?... Adhoc input layer, possibly?
model.fc = nn.Sequential(
    nn.Linear(2048, 512),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(512, 10),
    nn.LogSoftmax(dim=1)
)

# Load the pretrained weights...
model.load_state_dict(torch.load('ResNet50_nsfw_model.pth', map_location=torch.device('cpu')))

# Start the chainsaw...
model.eval()

# --------------------------------------------------------------
# --------------------------------------------------------------

def predict_image(image):
    image_tensor = test_transforms(image).float()
    image_tensor = image_tensor.unsqueeze_(0)

    if torch.cuda.is_available():
        image_tensor.cuda()

    input = Variable(image_tensor)
    output = model(input)
    index = output.data.numpy().argmax()
    return index

def evaluate_images(folder):
    # Classes = [0 - 'drawings', 1 - 'hentai', 2 - 'neutral', 3 - 'porn', 4 - 'sexy']
    
    #load images
    entries = os.listdir(folder)

    i = 0
    is_flagged = "false"

    for entry in entries:
        i+=1
        image = Image.open(folder + entry)
        
        # Prediction...
        index = predict_image(image)
        
        # If the image is smut (based on the classes above)...
        if(index == 1 or index == 3 or index == 4):
            is_flagged = "true"
            break

    print(is_flagged)


parser = argparse.ArgumentParser()

parser.add_argument("folder", type=str, help="Folder of generated or extant images to test for smut.")
args = parser.parse_args()

evaluate_images(args.folder)    

