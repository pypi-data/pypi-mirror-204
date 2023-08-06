# HTI Thermal
## HTI Thermal Library to extract raw thermal datapoint from rjpeg
This is a library is used to extract rJpeg image captured using Hti-Xintai HT-19 Thermal Imager to raw thermal datapoints.

## Features
imagesToThermals
and image to np.array

## Installation
To install the library, use pip:
```
pip install htithermal
```

## Usage
Here is an example of how to use the library:

python
```
import htithermal as ht

# Extract thermal datapoint from images
themperature_array = ht.convertRjpegToTemperature('C:/Users/gsome/Desktop/Hti-Images/20230417-100642.jpg')

# Extract all thermal datapoint from images in given directory
ht.imagesToThermals(input_dir='C:\\Users\\gsome\\Desktop\\Hti-Images')

# Visualize thermal image
import matplotlib.pyplot as plt
import pandas as pd
plt.imshow(themperature_array)
plt.show()
```

## Contact Us
gupta.somex@gmail.com

## License
This library is licensed under the MIT License.