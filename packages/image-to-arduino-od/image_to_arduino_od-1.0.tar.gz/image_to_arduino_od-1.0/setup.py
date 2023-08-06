from setuptools import setup, find_packages

REQUIREMENTS = [i.strip() for i in open(r"C:\Users\Lenovo\Image_Converter_App\requirements.txt").readlines()]
DESCRIPTION = 'Image_Converter_App'
LONG_DESCRIPTION = 'About Image converter GUI App to arduino oled display ssd1306 128x64'
setup(
   name='image_to_arduino_od',
   version='1.0',
   license="MIT",
   author='WiktorK02',
   author_email='wiktor.kidon@hotmail.com',
   url="https://github.com/WiktorK02/Image_Converter_App.git",
   description=DESCRIPTION,
   long_description_content_type="text/markdown",
   long_description=LONG_DESCRIPTION,
   packages=find_packages('src', exclude=['image_to_arduino']),
   install_requires=REQUIREMENTS, 

)