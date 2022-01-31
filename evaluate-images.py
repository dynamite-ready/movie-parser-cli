import os
import argparse
import torch

from torch import nn
from torchvision import transforms, models
from PIL import Image
from torch.autograd import Variable

def initialise_model():
  # This is preps the input image with PyTorch's image tools.
  # will resize the input image, crop it, and convert it to a normalized
  # tensor (I'm assuming each pixel is represented by a vector of 3 floats).
  input_layer = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225])                                
  ])

  # It looks like PyTorch has a built in Model Zoo, which I guess is
  # a big reason for why it's so popular. In this case, ResNet50 is
  # a CNN network architecture that has been proven to work with image recognition.
  # The `ResNet50_nsfw_model` model is based on what is mostly the same architecture... 
  model = models.resnet50()

  # ...Except for the few layers where it's different.
  # One of the more practical features provided by PyTorch is a fairly flexible API
  # to allow developes/scientist/engineers/bums to tack pieces on to ready made networks.
  # I think this `Sequential` grouping of 5 layers represents a custom output stack for 
  # the `ResNet50_nsfw_model`
  model.fc = nn.Sequential(
    nn.Linear(2048, 512),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(512, 10),
    nn.LogSoftmax(dim=1)
  )

  # Load the pretrained weights. As you can see here, the second argument
  # of `torch.load` request a `torch_device`. If I was using CUDA, I would guess I'd
  # have to point that out here. I Hav CUDA installed on my machine, but the version
  # of Pytorch built to interface with CUDA is a whopping 3.5GB. That's infeasible
  # if I wish to make this portable. Until that changes, this program relies on the CPU version.
  model.load_state_dict(torch.load(args.model, map_location=torch.device('cpu')))

  # Start the chainsaw...
  model.eval()

  # Return these key constants as a tuple...
  return (input_layer, model)

def predict_image(image, input_layer, model):
  image_tensor = input_layer(image).float() # Input the image.
  # This next line tranforms the input tensor, to fit the default Resnet50 input shape.
  input = image_tensor.unsqueeze_(0)
  # Collect the output. It's a single value that represents m 
  output = model(input)
  index = output.data.numpy().argmax()

  return [index, output.data[0][index].item()]

def evaluate_images(folder):
  # The `ResNet50_nsfw_model` Pytorch model can detect the following:
  # 0 - '2D Art', 
  # 1 - 'Hentai', 
  # 2 - 'Neutral', 
  # 3 - 'Porn', 
  # 4 - 'Sexy'

  # Initialise the Pytorch NSFW model. The `initialise_model`` function returns 
  # the initialised model itself, and a function to prepare the input image for processing.
  (input_layer, model) = initialise_model()
  
  # Load the images from your chosen image folder.
  # `os.listdir` returns a list / array.
  images = os.listdir(folder)

  # Perform a running count of the images that have been checked.
  image_counter = 0

  # By default, lets assume that the image folder contains no filth... 
  magnitude = -1

  for image in images:
    image_counter += 1 # Count the number of images processed
    image = Image.open(folder + "/" +  image) # Open each given image in the folder 
    
    # Now we make the prediction itself.
    index = predict_image(image, input_layer, model)
    
    # Only flag the images as dirty, if it's determined to fit a suspect class. 
    if((index[0] == 1 or index[0] == 3 or index[0] == 4) and index[1] > magnitude):
        magnitude = index[1]

  # Finally, we print out how mucky the AI model
  # considers this collection of images to be.
  print(magnitude)

parser = argparse.ArgumentParser()
parser.add_argument("folder", type=str, help="A folder of images to test for NSFW content. Outputs a single floating point number (0.3+ is probably mucky)")
parser.add_argument("--model", type=str, help="`ResNet50_nsfw_model.pth` file location", nargs='?', default=os.getcwd() + '/ResNet50_nsfw_model.pth')
args = parser.parse_args()

evaluate_images(args.folder)    

