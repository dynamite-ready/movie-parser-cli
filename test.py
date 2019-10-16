import os
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
from torchvision import transforms, models
from PIL import Image
from torch.autograd import Variable

#image directory
data_dir = 'test-folder/'

test_transforms = transforms.Compose(
    [
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225])                                
    ]
)

model = models.resnet50()
model.fc = nn.Sequential(
    nn.Linear(2048, 512),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(512, 10),
    nn.LogSoftmax(dim=1)

)
model.load_state_dict(torch.load('ResNet50_nsfw_model.pth', map_location=torch.device('cpu')))
model.eval()

def predict_image(image):
    image_tensor = test_transforms(image).float()
    image_tensor = image_tensor.unsqueeze_(0)

    if torch.cuda.is_available():
        image_tensor.cuda()

    input = Variable(image_tensor)
    output = model(input)
    index = output.data.numpy().argmax()
    return index

classes=['drawings', 'hentai', 'neutral', 'porn', 'sexy']

#load images
entries = os.listdir(data_dir)

i = 0

for entry in entries:
    i+=1
    image = Image.open(data_dir+entry)
    
    #prediction
    index = predict_image(image)

    print(classes[index])

