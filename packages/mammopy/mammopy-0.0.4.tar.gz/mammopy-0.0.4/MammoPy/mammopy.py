
import os
import numpy as np
import requests
from pathlib import Path
from skimage import feature
import torch
import matplotlib.pyplot as plt
import torch.nn as nn
import os, io, pydicom
import time
from torchvision import transforms
from PIL import Image

MASK_COLORS = ["red", "green", "blue", "yellow", "magenta", "cyan"]


def mask_to_rgba(mask, color="red"):
    """
    Converts binary segmentation mask from white to red color.
    Also adds alpha channel to make black background transparent.
    Args:
        mask (numpy.ndarray): [description]
        color (str, optional): Check `MASK_COLORS` for available colors. Defaults to "red".
    Returns:
        numpy.ndarray: [description]
    """
    assert color in MASK_COLORS
    assert mask.ndim == 3 or mask.ndim == 2

    h = mask.shape[0]
    w = mask.shape[1]
    zeros = np.zeros((h, w))
    ones = mask.reshape(h, w)
    if color == "red":
        return np.stack((ones, zeros, zeros, ones), axis=-1)
    elif color == "green":
        return np.stack((zeros, ones, zeros, ones), axis=-1)
    elif color == "blue":
        return np.stack((zeros, zeros, ones, ones), axis=-1)
    elif color == "yellow":
        return np.stack((ones, ones, zeros, ones), axis=-1)
    elif color == "magenta":
        return np.stack((ones, zeros, ones, ones), axis=-1)
    elif color == "cyan":
        return np.stack((zeros, ones, ones, ones), axis=-1)



def load_model(model_path):
    """
    Loads a pre-trained model from a given path.
    Args:
    - model_path: str, the path to the pre-trained model. 
                  If model_path = 'base', then the default pre-trained model will be loaded.
    
    Returns:
    - model: torch.nn.Module, the pre-trained model loaded from the specified path.
    Raises:
    - TypeError: if the input model_path is not 'base'.
    """
    
    if model_path == 'base':
        # Define the path to the default pre-trained model weights
        model_weights_path = "weights.pth"
        path = Path(model_weights_path)

        # If the model weights file does not exist, download it from Dropbox
        if not path.is_file():
            url = "https://www.dropbox.com/s/37rtedwwdslz9w6/all_datasets.pth?dl=1"
            response = requests.get(url)
            open("weights.pth", "wb").write(response.content)
        
        # Load the pre-trained model and set the device to CPU
        model = torch.load(model_weights_path, map_location=torch.device("cpu"))
        # Convert the model to be compatible with multiple GPUs, if available
        model = nn.DataParallel(model.module)
        
        return model
    else:
        raise TypeError("Model not implemented")

        

def image_tensor(img):
    """
    Converts a PIL Image or NumPy array to a PyTorch tensor.
    Args:
    - img: PIL.Image or np.ndarray, the image to be converted to a PyTorch tensor.
    Returns:
    - image: torch.Tensor, the converted PyTorch tensor.
    Raises:
    - TypeError: if the input image is not a PIL.Image or np.ndarray.
    """
    
    if type(img) not in [np.ndarray, Image.Image]:
        raise TypeError("Input must be np.ndarray or PIL.Image")

    # Define a PyTorch tensor transformer pipeline
    torch_tensor = transforms.Compose(
        [transforms.Resize((256, 256)), transforms.ToTensor()]
    )

    if type(img) == Image.Image:
        # Convert PIL image to PyTorch tensor
        image = torch_tensor(img)
        image = image.unsqueeze(0)
        print("tensor", type(image))
        return image
    elif type(img) == np.ndarray:
        # Convert NumPy array to RGB PIL image and then to PyTorch tensor
        pil_image = Image.fromarray(img).convert("RGB")
        image = torch_tensor(pil_image)
        image = image.unsqueeze(0)
        print("tensor", type(image))
        return image
    else:
        raise TypeError("Input must be np.ndarray or PIL.Image")



def percentage_density(model, image_path):
    """
    Computes the percentage of mammogram density in an input image.
    Args:
        model (str): The name of the pre-trained model to use.
        image_path (str): The path to the input image file.
    Returns:
        dict: A dictionary containing the results of the computation. The dictionary
        has the following keys:
            - non_dense_area: The total number of pixels in the input image that corresponse 
            to non-dense tissue. (i.e., non-fibroglandular)
            - dense_area: The total number of pixels in the input image that corresponse
            to dense tissue. (i.e., fibroglandular)
            - percentage_density: The percentage of mammogram density in the input image.
    Raises:
        TypeError: If `model` is not a string or `image_path` is not a string.
        ValueError: If `model` is not a valid pre-trained model name or `image_path`
        does not point to a valid image file.
    """

    # Load the pre-trained model weights
    #model = load_model(model)

    # Load the input image and convert it to a PyTorch tensor
    image = Image.open(image_path).convert('RGB')
    img = image_tensor(image)

    # Compute the mammogram density
    result = {}
    pred1, pred2 = model.module.predict(img)
    
    pred1 = pred1[0].cpu().numpy().transpose(1, 2, 0)
    pred1 = pred1[:, :, 0]

    pred2 = pred2[0].cpu().numpy().transpose(1, 2, 0)
    pred2 = pred2[:, :, 0]

    breast_area = np.sum(np.array(pred1) == 1)
    dense_area = np.sum(np.array(pred2) == 1)
    density = (dense_area / breast_area) * 100
    
    # Populate the result dictionary with the computed values
    result["non_dense_area"] = breast_area
    result["dense_area"] = dense_area
    result["percentage_density"] = density
    
    return result

def canny_edges(image_array):
    """
    Detect edges using the Canny algorithm.
    
    Parameters:
    image_array (numpy.ndarray): The input image array
    
    Returns:
    edges (numpy.ndarray): A binary edge map with detected edges marked with 1.
    
    Raises:
    TypeError: If the input image is not a numpy array.
    """
    if not isinstance(image_array, np.ndarray):
        raise TypeError("Input image must be a numpy array.")
    
    # Detect edges using Canny algorithm with sigma value of 3.
    edges = feature.canny(image_array, sigma=3)
    
    return edges

    
def visualize(model, image_path,breast_segmentation=True, dense_segmentation=True):
    """
    This function is used to visualize the segmentation results of mammography images using a deep learning model.
    Args:
    - model: PyTorch model used for segmentation.
    - image_path: Path to the mammography image.
    - breast_segmentation: Boolean indicating whether to display the breast area contour or not.
    - dense_segmentation: Boolean indicating whether to display the dense tissue segmentation or not.
    Returns:
    - None
    Raises:
    - TypeError: If model is not a PyTorch model or if image_path is not a string.
    - ValueError: If breast_segmentation and dense_segmentation are both False.
    """
    
    if not isinstance(model, torch.nn.Module):
        raise TypeError("Model must be a PyTorch model.")
    if not isinstance(image_path, str):
        raise TypeError("Image path must be a string.")
    if not breast_segmentation and not dense_segmentation:
        raise ValueError("At least one of breast_segmentation and dense_segmentation must be True.")

    # Load and preprocess the image
    image = Image.open(image_path).convert('RGB')
    img = image_tensor(image)

    # Make predictions using the model
    pred1, pred2 = model.module.predict(img)

    # Convert predictions to numpy arrays
    img = img[0].cpu().numpy().transpose(1, 2, 0)
    img = img[:, :, 0]

    pred1 = pred1[0].cpu().numpy().transpose(1, 2, 0)
    pred1 = pred1[:, :, 0]

    pred2 = pred2[0].cpu().numpy().transpose(1, 2, 0)
    pred2 = pred2[:, :, 0]

    # Generate breast area contour using Canny edge detection
    breast_contour = canny_edges(pred1)

    # Display the segmentation results
    if breast_segmentation and not dense_segmentation:
        plt.title('Breast area contour')
        plt.imshow(img, cmap='gray')
        plt.imshow(mask_to_rgba(breast_contour, color='red'), cmap='gray')
        plt.axis('off')
        plt.show()

    if dense_segmentation and not breast_segmentation:
        plt.title('Dense tissues')
        plt.imshow(img, cmap='gray')
        plt.imshow(mask_to_rgba(pred2, color='green'), cmap='gray')
        plt.axis('off')
        plt.show()

    if breast_segmentation and dense_segmentation:
        fig, axes = plt.subplots(1, 2, figsize=(20, 15), squeeze=False)
    
        axes[0, 0].set_title('Image', fontsize=25)
        axes[0, 1].set_title("Breast and dense tissue segmentation", fontsize=25)
      
        axes[0, 0].imshow(img, cmap='gray')
        axes[0, 0].set_axis_off()

        axes[0, 1].imshow(img, cmap='gray')
        axes[0, 1].imshow(mask_to_rgba(breast_contour, color='green'), cmap='gray')
        axes[0, 1].imshow(mask_to_rgba(pred2, color='red'), cmap='gray', alpha=0.5)
        axes[0, 1].set_axis_off()

        plt.show()