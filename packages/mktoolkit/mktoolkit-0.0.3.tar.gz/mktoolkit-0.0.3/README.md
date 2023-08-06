#### Purpose
+ The purpose of the package is to provide a unified solution for the assessment of the density estimation of mammogram

### Features
+ Initial verison contain the feature to calculate the Tensor and the Density Estimation.

### Getting Started
+ This package can be found on the pypi which can installed using pip.

### Installation Guide
```bash 
pip install mktoolkit
``` 
### Usage
+ It can be used very easily by importing the functoins
```python
from mktoolkit import image_tensor
img = load_image(path)
img_tensor = image_tensor(img)
```
```python
from mktoolkit import breast_density_2d
img, prediction1, prediction2, density = breast_density_2d(image)
```
### Contribution
Contributions are Welcome
Notice a bug let us know

### Author
+ Main Contributor: UEF Cancer Group
