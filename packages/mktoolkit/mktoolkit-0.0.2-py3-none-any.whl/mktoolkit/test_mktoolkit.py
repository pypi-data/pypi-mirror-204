import unittest
import pydicom
import numpy as np
from torchvision import transforms
from mktoolkit import image_tensor
from PIL import Image


class ImageTensor(unittest.TestCase):

################################################################
################ Tensor function testing #######################
################################################################
    def test_image_tesor(self):
        #####################
        ### Input 1 for test
        # arrange
        self.image = Image.open('test_images/EE0B064D.jpg').convert('RGB')
        torch_tensor = transforms.Compose([transforms.ToTensor(), transforms.Resize((256, 256))])
        self.image_tens = torch_tensor(self.image)
        self.image_tens = self.image_tens.unsqueeze(0)
        # action
        img = image_tensor(self.image)
        #Assert
        self.assertEqual(self.image_tens.shape, img.shape)
        
        
        #####################
        ### Input 2 for test
        # arrange
        self.image2 = 'test_images/EE0B3880'
        self.ds = pydicom.dcmread(self.image2)
        self.pixel_array  = self.ds.pixel_array
        self.pil_image = Image.fromarray(self.pixel_array)
        self.img = self.pil_image.convert('RGB')
        self.img = np.max(self.img) - self.img
        torch_tensor = transforms.Compose([transforms.ToTensor(), transforms.Resize((256, 256))])
        self.image_tens = torch_tensor(self.img)
        self.image_tens = self.image_tens.unsqueeze(0)
        # action
        img = image_tensor(self.img)
        #Assert
        self.assertEqual(self.image_tens.shape, img.shape)


    def test_types(self):
        self.image2 = 'mtoolkit/test_images/EE0B3880'
        self.assertRaises(TypeError, image_tensor, 'abcd')
        self.assertRaises(TypeError, image_tensor, 2584)
        self.assertRaises(TypeError, image_tensor, 0.258)
        self.assertRaises(TypeError, image_tensor, self.image2)



if __name__ =='__main__':
    unittest.main()