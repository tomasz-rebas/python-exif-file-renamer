# How does it work?

`exif_file_renamer.py` was designed to automate renaming photo files with an information useful for photographers e.g. date, exposure time and aperture. It extracts metadata from image files and uses it to rename them.

New filename follows this pattern:

### `DATE_TIME_FOCALLENGTH_EXPOSURE_APERTURE_ISO`

Example:

`180515_16025102_70mm_1-360s_f7.1_ISO-1600`

The script is looking for JPG files first, but it also checks for Nikon RAW (.nef) files of the same name and renames them as well if they're exist. 

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

Run `exif_file_renamer.py` script and pass (as an argument) path to the folder containing photos you want to rename.

You can do this by navigating to the directory with the script and running the following command:

### `python.exe exif_file_renamer.py MyFolder`

You need to specify an absolute path for the directory.