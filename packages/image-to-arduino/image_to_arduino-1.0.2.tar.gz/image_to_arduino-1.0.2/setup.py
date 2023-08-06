from setuptools import setup, find_packages

REQUIREMENTS = [i.strip() for i in open("/home/wiktor/Image_Converter_App/requirements.txt").readlines()]
LONG_DESCRIPTION = 'About Image converter GUI App to arduino oled display ssd1306 128x64'
setup(
   name='image_to_arduino',
   version='1.0.2',
   description='Image converter to arduino',
   license="MIT",
   author='WiktorK02',
   author_email='wiktor.kidon@hotmail.com',
   url="https://github.com/WiktorK02/Image_Converter_App.git",
   long_description_content_type="text/markdown",
   long_description=LONG_DESCRIPTION,
   packages=['src'],
   package_data={'src': ['data/*.dat']},
   install_requires=REQUIREMENTS, 

)
