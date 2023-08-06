# Image Converter GUI APP for Arduino oled display ssd1306 128x64
## About Project
Application has been created in order to easy convert image into your <strong>Arduino</strong> project with <strong>oled displays</strong>
### How does it work:
While you open .png and .jpg (others extensions in the future) image in app, the algorithm convert it to hexdeicmal array. Then it             returns full     code, ready to copy and put into the Arduino IDE. You can also preview how image will you like on your dislplay
## Demo
 <p align="center">
<img src="https://user-images.githubusercontent.com/123249470/232137289-ff2707a7-a4bf-4e55-88a5-a469f54c3c3d.gif" width="350" height="560">
</p>

## How to install
#### First of all download python and pip and check version
```
pip3 --version 
python --version
```

### Windows:
Type into CMD:
```
pip3 install image-to-arduino
```
```
pip3 install tk
```
### Linux: 
```
$ pip3 install image-to-arduino
```
```
$ sudo apt-get install python3-tk
```
### Mac OS:
```
~ % pip3 install image-to-arduino
```
```
~ % pip3 install tk 
```
## How to run
```
$ pip3 show image-to-arduino
```
copy location path and add ```/src``` to the end
```
$ cd <copyied path/src>
```
### For example:
```
$ pip3 show image-to-arduino
Location: /home/usr/Image_Converter_App
$ cd /home/usr/Image_Converter_App/src
```
### Windows:
#### Run the script:
```
python image_to_arduino.py
```
### Linux/Mac OS:
#### Mark the file as an executable:
```
$ chmod +x image_to_arduino.py 
```
#### Run the script:
```
$ python3 image_to_arduino.py 
```
## How to connect display to Arduino

<p align="center">
      <img src="https://user-images.githubusercontent.com/123249470/233432819-97b593ab-d380-4945-85ab-543dbb49921b.png" width="620" height="480">
</p>

IMPORTANT: If you have Arduino board with inputs SCK and SDA, use them instead of A4 and A5 inputs

## How to Contribute
1. Fork the Project
2. Clone repo with your GitHub username instead of ```YOUR-USERNAME```:<br>
```
$ git clone https://github.com/YOUR-USERNAME/Image_Converter_App 
```
3. Create new branch:<br>
```
$ git branch BRANCH-NAME 
$ git checkout BRANCH-NAME
```
4. Make changes and test<br>
5. Submit Pull Request with comprehensive description of change

## Task list
* <del> upgrade graphics and style </del><br>
* <del> add more functions </del><br>
* add more than one display size<br>
* make icon of the app<br>
* <del> show preview of an image </del> <br>
* make app as .exe <br>
* <del> reverse color of image </del><br>
* create function which generate full arduino code(not only arduino array) and connect it to switch button
## What I have learned
*	tkinter library skills 
*	basics of UX and GUI
*	image processing 
## Used libraries
* tkinter 
* customtkinter
* openCV
* numpy
## Version
Version 1.0.3.1
## License 
[MIT license](LICENSE)
