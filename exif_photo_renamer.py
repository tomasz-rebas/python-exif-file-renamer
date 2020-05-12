# imports for EXIF data export
from PIL import Image
from PIL.ExifTags import TAGS

# imports for reading filenames
from os import listdir
from os.path import isfile, join

# import for file renaming
import os

# import for using arguments
import sys

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
    selected = {'DateTimeOriginal': '', 'MaxApertureValue': '', 'FocalLength': '', 'SubsecTimeOriginal': '', 'ExposureTime': '', 'ISOSpeedRatings': ''}
    for (key, val) in exif.items():
        if TAGS.get(key) in selected:
            selected[TAGS.get(key)] = val
    return selected

def check_for_empty_values(selected):
    for key in selected:
        if selected[key] == '':
            return True
    return False

def build_new_filename(selected):
    new_filename = ''
    selected['DateTimeOriginal'] = selected['DateTimeOriginal'].replace(':', '')
    selected['DateTimeOriginal'] = selected['DateTimeOriginal'].replace(' ', '_')
    new_filename += selected['DateTimeOriginal']
    new_filename += selected['SubsecTimeOriginal'] + '_'
    new_filename += str(int(selected['FocalLength'][0] / selected['FocalLength'][1])) + 'mm_'

    if selected['ExposureTime'][0] < selected['ExposureTime'][1]:
        new_filename += str(selected['ExposureTime'][0] / 10) + '-' + str(selected['ExposureTime'][1] / 10) + 's_'
    else:
        new_filename += str(selected['ExposureTime'][0] / 10) + 's_'

    new_filename += 'f' + str(selected['MaxApertureValue'][0] / selected['MaxApertureValue'][1]) + '_'
    new_filename += 'ISO-' + str(selected['ISOSpeedRatings'])
    
    return new_filename.replace('.0', '')

def check_for_raw_file(path, f):
    f_raw = f.casefold().replace('.jpg', '.nef')
    if os.path.isfile(path + '\\' + f_raw):
        return f_raw
    else:
        return False

def rename_files(path):
    for f in listdir(path):
        if isfile(join(path, f)) and f.casefold().endswith('.jpg'):
            exif = get_exif(path + '\\' + f)
            selected = get_selected_exif(exif)
            if not check_for_empty_values(selected):
                print('renaming JPG file...')
                # os.rename(path + '\\' + f, path + '\\' + build_new_filename(selected) + '.jpg')
                f_raw = check_for_raw_file(path, f)
                if f_raw:
                    print('and renaming NEF file too...')
    print('new filename:')
    print(selected)
    print(build_new_filename(selected))
    print(sys.argv[1])

# path = 'D:\python_test_photos'
# onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
# exif = get_exif(path + '\photo.jpg')
# selected = get_selected_exif(exif)

# os.rename(r'D:\python_test_photos\photo.jpg', r'D:\python_test_photos\photo_renamed.jpg')

#######################

try:
    path = 'D:\python_test_photos'
    rename_files(path)
except IndexError:
    print('Error: no argument provided. Please provide an absolute path to the directory containing files you want to rename.')


#######################

#print(onlyfiles)
