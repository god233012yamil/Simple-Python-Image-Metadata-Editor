# Image Metadata Editor

## Overview

Image Metadata Editor is a Python application designed to facilitate the viewing and editing of metadata embedded in digital images. Utilizing PyQt5 for its graphical user interface and PIL (Pillow) alongside `piexif` for metadata handling, this tool provides a user-friendly environment for photographers, digital artists, and developers to manage image metadata.

## Features

- **Open and view images**: Load images directly through the interface.
- **Display metadata**: Show all EXIF metadata contained in the image in a readable format.
- **Edit metadata**: Modify the values of metadata tags and save the changes back to the image.
- **Save functionality**: Save the modified image as a new file to preserve the original image.

## Prerequisites

Before you can run the Image Metadata Editor, you need to ensure your system has the following software installed:

- Python 3.x
- PyQt5
- PIL (Pillow)
- piexif

You can install the necessary Python libraries using pip:

pip install PyQt5 Pillow piexif

## Installation
Clone this repository to your local machine using: 

git clone https://github.com/yourusername/image-metadata-editor.git

## Usage
To start the application, run the following command in your terminal:

python app.py

Once the application is running, you can:

Click on "Open Image" to load an image into the application.

View the metadata in the display area. 

Select a metadata tag from the dropdown menu to edit. 

Enter the new value for the selected tag in the text field. 

Click "Save Changes" to apply the modifications and save them to a new image file.
