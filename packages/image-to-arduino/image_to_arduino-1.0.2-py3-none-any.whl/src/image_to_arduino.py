#!/usr/bin/env python3
import tkinter as tk
import customtkinter 
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageOps
import os

# To check extenxion
import imghdr

file_path = ''
image_tk = ''
switch_state = False

def open_file():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        # If file name len is greater than 15: return ... + extension
        file_label.configure(text="File: " + (os.path.basename(file_path) if len(os.path.basename(file_path)) < 15 else "..." + imghdr.what(file_path)))
    else:
        file_label.configure(text="No file selected")

def generate_text():
    global image_tk, switch_var
    if not file_path == '':    
        try:
            # To check extenxion
            extension = imghdr.what(file_path)

            if  extension == "jpeg" or extension == "png":
                # Load image
                image = cv2.imread(file_path, cv2.IMREAD_COLOR)
                
                # Resize the image to 128x64
                image = cv2.resize(image, (128, 64))
                
                # Convert RGB image to grayscale
                grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                
                # Convert the image to a PIL Image object
                image_pre = Image.fromarray(cv2.threshold(grayscale_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1])

                if switch_state == True:
                    # Reverse the colors of the image
                    image_pre = ImageOps.invert(image_pre)
                
                # Convert the PIL Image to a PhotoImage object
                image_pre = ImageTk.PhotoImage(image_pre)
                
                # Update the label's image
                image_preview_label.config(image=image_pre)
                image_preview_label.image = image_pre
            
                _, thresholded_image = cv2.threshold(grayscale_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                if switch_state == True:
                    # Convert the thresholded image to a binary array (0s and 1s)
                    binary_array = np.where(thresholded_image > 0, 0, 1)
                else:
                    # Convert the thresholded image to a binary array (0s and 1s)
                    binary_array = np.where(thresholded_image > 0, 1, 0)

            # Convert the binary array to a 1D array
            one_d_array = binary_array.flatten()

            # Split the binary alpha values into 8-byte arrays
            byte_arrays = np.packbits(one_d_array)

            # Convert byte arrays to hexadecimal format
            hex_byte_arrays = ['0x' + format(byte, '02x') for byte in byte_arrays]

            cpp_array = ', '.join(hex_byte_arrays)
            # Insert newline after every 10 hexadecimal numbers
            cpp_array = [cpp_array[i:i+2] for i in range(0, len(cpp_array), 2)]  # Split into pairs of hexadecimal numbers
            cpp_array = [''.join(cpp_array[i:i+30]) for i in range(0, len(cpp_array), 30)]  # Join pairs with space, and group every 10 pairs
            cpp_array = '\n'.join(cpp_array)  # Join groups with newline character

            # Generate C++ array
            cpp_array = 'unsigned char my_array[] = {\n' + cpp_array + '\n};'

            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, cpp_array)
        
        # In case of error or invalid extension 
        except:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "Error generating text")
    else: 
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Select any file")

def copy_all():
    global file_path
    if not file_path:
        copied_all_label.configure(text="No text to copy")
        return

    root.clipboard_clear()
    root.clipboard_append(output_text.get(1.0, tk.END))
    copied_all_label.configure(text="✓ Copied")

def toggle_switch():
    global switch_state
    switch_state = not switch_state

def clear_all():
    # Clear output text and image preview
    output_text.delete(1.0, tk.END)
    image_preview_label.config(image="")

customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("dark-blue")  

# Create customtkinter window
root = customtkinter.CTk() 
root.title("Image Converter v1.0")

# Set window size
root.geometry("320x530") # Set width and height as desired

# Label for displaying selected file path
file_label =  customtkinter.CTkLabel(root, text="No file selected")
file_label.grid(row=0, column=0, padx=10, columnspan=1, sticky="nsew", pady=5)

# "Open File" button
open_file_button = customtkinter.CTkButton(root, text="Open Image File", command=open_file)
open_file_button.grid(row=0, column=1, padx=10, pady=5, columnspan=1, sticky="nsew")

# "Generate" button
generate_button = customtkinter.CTkButton(root, text="Generate Code", command=generate_text)
generate_button.grid(row=2, column=0, padx=10, pady=5, columnspan=1, sticky="nsew")

# "Copy All" button
copy_all_button = customtkinter.CTkButton(root, text="Copy All", command=copy_all)
copy_all_button.grid(row=2, column=1, padx=10, pady=5, columnspan=1, sticky="nsew")  

# Output text 
output_text = customtkinter.CTkTextbox(root, height = 280, width = 300 )   # 25 50
output_text.grid(row=3, column=0, padx=10, pady=5, columnspan=3, sticky="nsew")

# Label for displaying "Copied All" text
copied_all_label =  customtkinter.CTkLabel(root, text="")
copied_all_label.grid(row=4, column=1, pady=5,columnspan=3, sticky="nsew")

# Preview text lael
preview_text_label = customtkinter.CTkLabel(root, text="Preview")
preview_text_label.grid(row=5, column=0, pady=5, padx=10)

# Label to display the image
image_preview_label = tk.Label(root, bg='#1c1c1c')
image_preview_label.grid(row=6, column=0, columnspan=1, padx=10)

# Switch label
switch = customtkinter.CTkSwitch(root, text="Reverse colors", command=toggle_switch)
switch.grid(row=1, column=0, padx=10, sticky="nsew")
# Switch label right
switch_right = customtkinter.CTkSwitch(root, text="Full arduino code", command=toggle_switch)
switch_right.grid(row=1, column=1, padx=10, sticky="nsew")

# "Clear all" button 
clear_all_button = customtkinter.CTkButton(root, text="Clear All", command=clear_all)
clear_all_button.grid(row=4, column=0, pady=5, padx=10, columnspan=1, sticky="nsew")  

# Configure the window to not be resizable
root.resizable(False, False)

root.mainloop()
