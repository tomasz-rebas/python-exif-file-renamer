# imports for EXIF data export
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

# not need to call this one
def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val
    return labeled

def get_selected_exif(exif):
    selected_data = {'DateTimeOriginal': '', 'MaxApertureValue': '', 'FocalLength': '', 'SubsecTimeOriginal': '', 'ExposureTime': '', 'ISOSpeedRatings': ''}
    for (key, val) in exif.items():
        if TAGS.get(key) in selected_data:
            selected_data[TAGS.get(key)] = val
    return selected_data