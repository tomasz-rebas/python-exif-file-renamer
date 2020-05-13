# Installation
 
Make sure you have Python installed. You can check it by running this command in terminal:

### `python`

You'll also need a pip package manager. Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) file and run:

### `python get-pip.py`

Alternatively you can run this command:

### `python -m pip install --upgrade pip`

Once pip is installed you need to install Pillow. It's a fork of Python Imaging Library used by python-exif-file-renamer for extracting EXIF data from images.

Run this command:

### `python -m pip install --upgrade Pillow`

And you're ready to go!

# Usage

Run `exif_photo_renamer.py` script and pass (as an argument) path to the folder containing photos you want to rename.

You can do this by navigating to the directory with the script and running the following command:

### `python.exe exif_photo_renamer.py MyFolder`

You need to specify an absolute path for the directory.