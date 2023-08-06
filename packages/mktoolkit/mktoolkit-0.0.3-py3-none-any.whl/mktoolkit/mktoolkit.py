import numpy as np
import requests
from pathlib import Path
from skimage import feature
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

##################################
######### Paths File #############
##################################
model_path = "weights.pth"
path = Path(model_path)
if path.is_file():
    pass
else:
    url = "https://www.dropbox.com/s/37rtedwwdslz9w6/all_datasets.pth?dl=1"
    response = requests.get(url)
    open("weights.pth", "wb").write(response.content)


##################################
#########  #############
##################################
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


def image_tensor(img):
    """
    Params:
    -----
    img: type- PIL image, nd_array

    Retruns
    -----
    torch_tensor: shape(batch_size, channels, width, heigth)

    Example:
    -----
    import mktools.image_tensor
    img = load_image(path)
    img_tensor = image_tensor(img)

    """
    if type(img) not in [np.ndarray, Image.Image]:
        raise TypeError("Input must be np.ndarray or PIL.Image")

    torch_tensor = transforms.Compose(
        [transforms.Resize((256, 256)), transforms.ToTensor()]
    )
    if type(img) == Image.Image:
        image = torch_tensor(img)
        image = image.unsqueeze(0)
        print("tensor", type(image))
        return image
    elif type(img) == np.ndarray:
        pil_image = Image.fromarray(img).convert("RGB")
        image = torch_tensor(pil_image)
        image = image.unsqueeze(0)
        print("tensor", type(image))
        return image
    else:
        raise TypeError("Input must be np.ndarray or PIL.Image")


def breast_density_2d(image):
    """
    Params:
    -----
    image:
        type:
            torch.Tensor
        dtype:
            torch.float32
        shape:
            ([1, 3, 256, 256]) (batch_size, channels, width, heigth)

    Retruns
    -----
    image:
        type:
            np.ndarray
        dtype:
            float32
        shape:
            (256, 256)
    pred1:
        type:
            np.ndarray
        dtype:
            float32
        shape:
            (256, 256)
    pred2:
        type:
            np.ndarray
        dtype:
            float32
        shape:
            (256, 256)
    density:
        type:
            np.ndarray
        dtype:
            float64
        shape:
            ()

    Example:
    -----
    import mktools.breast_density_2d

    img, prediction1, prediction2, density = breast_density_2d(image)

    """
    if type(image) != torch.Tensor:
        raise TypeError("Input type must be torch.Tensor")
    else:
        model = torch.load(model_path, map_location=torch.device("cpu"))
        model = nn.DataParallel(model.module)

        pred1, pred2 = model.module.predict(image)

        image = image[0].cpu().numpy().transpose(1, 2, 0)
        image = image[:, :, 0]

        pred1 = pred1[0].cpu().numpy().transpose(1, 2, 0)
        pred1 = pred1[:, :, 0]

        pred2 = pred2[0].cpu().numpy().transpose(1, 2, 0)
        pred2 = pred2[:, :, 0]

        breast_area = np.sum(np.array(pred1) == 1)
        dense_area = np.sum(np.array(pred2) == 1)
        density = (dense_area / breast_area) * 100
        return image, pred1, pred2, density


def canny_edges(image_array):
    """
    Params:
    -----
    img_array:
        type:
            np.ndarray
        dtype:
            float32
        shape:
            (256, 256)

    Retruns
    -----
    img_array:
        type:
            np.ndarray
        dtype:
            bool
        shape:
            (256, 256)

    Example:
    -----
    import mktools.canny_edges

    img_array = canny_edges(img_array)

    """
    if (type(image_array) != np.ndarray) and (image_array.shape != (256, 256)):
        raise TypeError("Input must be np.ndarray and shape must be (256, 256)")
    else:
        edges = feature.canny(image_array, sigma=3)
        return edges


"""def run_analysis(img):
    img = image_tensor(img)
    img, pred1, pred2, density = breast_density_2d(img)
    edges = canny_edges(pred1)
    fig, axes = plt.subplots(1,2, figsize = (15,10),squeeze=False)
    axes[0, 0].set_title('Image', fontsize=16)
    axes[0, 1].set_title("Breast and dense tissue segmentation", fontsize=20)
    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_axis_off()
    axes[0, 1].imshow(img, cmap='gray')
    axes[0, 1].imshow(mask_to_rgba(edges, color='red'), cmap='gray')
    axes[0, 1].imshow(mask_to_rgba(pred2, color='green'), cmap='gray', alpha=0.7)
    axes[0, 1].set_axis_off()
    print("inside run_analysis", type(fig))"""

"""
###########################
#########################
############################

file = 'C:/Users/mhanan/Downloads/Hanan/mtoolkit/mtoolkit/test_images/IM094_ID101_R0.png'

img = Image.open(file, mode="r").convert('RGB')
tensored_img = image_tensor(img)
print("Tensor output:", type(tensored_img))
print("Tensor output:", tensored_img.shape)
print("Tensor output:", tensored_img.dtype)
img , p1, p2, d = breast_density_2d(image=tensored_img)
print("1 Brest function, Image:", type(img))
print("2 Brest function, Pred1:", type(p1))
print("3 Brest function, Pred2:", type(p2))
print("4 Brest function, Density:", type(d))
print("1 Brest function, Image:", img.shape)
print("2 Brest function, Pred1:", p1.shape)
print("3 Brest function, Pred2:", p2.shape)
print("4 Brest function, Density:", d.shape)
print("1 Brest function, Image:", img.dtype)
print("2 Brest function, Pred1:", p1.dtype)
print("3 Brest function, Pred2:", p2.dtype)
print("4 Brest function, Density:", d.dtype)
cany = canny_edges(p1)
print("Canny out:", type(cany))
print("Canny out:", cany.shape)
print("Canny out:", cany.dtype)



################################################################
################# Single file Analysis #########################
################################################################
def single_file_analysis(file):
    file_ext = file.name.split(".")[-1]
    if file_ext in ['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG']:
        img = Image.open(file).convert('RGB')
        print("JPG Code Running", type(img))
        run_analysis(img)
    elif file_ext == 'tiff' or file_ext == 'tif':
        pil_image = Image.open(io.BytesIO(file.read()))
        img = pil_image.convert('RGB')                
        print("Tiff Code Running", type(img))
        run_analysis(img)
    elif file_ext == 'dcm' or file_ext == 'DCM':
        dicom_file = pydicom.dcmread(file)
        pil_image = Image.fromarray(dicom_file.pixel_array)
        img = pil_image.convert('RGB')
        print("DCM Code Running", type(img))
        run_analysis(img)
    else:
        try:
            ds = pydicom.dcmread(file)
            pixel_array  = ds.pixel_array
            if ds.PhotometricInterpretation == 'MONOCHROME1':
                pixel_array = (pixel_array * 255.0 / np.max(pixel_array)).astype(np.uint8)
                pil_image = Image.fromarray(pixel_array)
                img = pil_image.convert('RGB')
                img = np.max(img) - img
                np_to_PILimg = Image.fromarray(img)
                print("DICOM Code Running", type(img))
                run_analysis(np_to_PILimg)
            else:
                print("inside if Error Message is going to display")
        except pydicom.errors.InvalidDicomError:
            print("exception Error Message is going to display")


################################################################
################# Multiple file Analysis #######################
################################################################

def multi_file_gen(result_file_name, img_name, img):
    with open(os.path.join('results', result_file_name), 'a') as result:
        img = image_tensor(img)
        img, pred1, pred2, density = breast_density_2d(_image=img, model_path=model_path)
        time.sleep(0.15)
        print(img_name, str(np.round(density,2)), file=result)

def multiple_file_analysis(file, result_file_name):    
    file_ext = file.name.split(".")[-1]
    img_name = file.name
    counter = 0
    if file_ext in ['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG']:
        img = Image.open(file).convert('RGB')
        multi_file_gen(result_file_name, img_name, img)
        counter += 1
    elif file_ext == 'tiff' or file_ext == 'tif':
        pil_image = Image.open(io.BytesIO(file.read()))
        img = pil_image.convert('RGB')
        multi_file_gen(result_file_name, img_name, img)
        counter += 1
    elif file_ext == 'dcm' or file_ext == 'DCM':
        dicom_file = pydicom.dcmread(file)
        pil_image = Image.fromarray(dicom_file.pixel_array)
        img = pil_image.convert('RGB')
        multi_file_gen(result_file_name, img_name, img)
        counter += 1
    else:
        try:
            ds = pydicom.dcmread(file)
            pixel_array  = ds.pixel_array
            if ds.PhotometricInterpretation == 'MONOCHROME1':
                pixel_array = (pixel_array * 255.0 / np.max(pixel_array)).astype(np.uint8)
                pil_image = Image.fromarray(pixel_array)
                img = pil_image.convert('RGB')
                img = np.max(img) - img
                np_to_PILimg = Image.fromarray(img)
                multi_file_gen(result_file_name, img_name, np_to_PILimg)
                counter += 1
            else:
                print("Wrong File format, We accept only JPG, PNG, TIFF or DICOM")                            
        except pydicom.errors.InvalidDicomError:
                print("Wrong File format, We accept only JPG, PNG, TIFF or DICOM")
    return counter

"""
