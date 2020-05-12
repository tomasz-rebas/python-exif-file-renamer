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
    selected_data = {'DateTimeOriginal': '', 'MaxApertureValue': '', 'FocalLength': '', 'SubsecTimeOriginal': '', 'ExposureTime': '', 'ISOSpeedRatings': ''}
    for (key, val) in exif.items():
        if TAGS.get(key) in selected_data:
            selected_data[TAGS.get(key)] = val
    return selected_data

def check_for_empty_values(selected_data):
    for key in selected_data:
        if selected_data[key] == '':
            return True
    return False

def build_new_filename(selected_data):
    new_filename = ''
    selected_data['DateTimeOriginal'] = selected_data['DateTimeOriginal'].replace(':', '')
    selected_data['DateTimeOriginal'] = selected_data['DateTimeOriginal'].replace(' ', '_')
    new_filename += selected_data['DateTimeOriginal']
    new_filename += selected_data['SubsecTimeOriginal'] + '_'
    new_filename += str(int(selected_data['FocalLength'][0] / selected_data['FocalLength'][1])) + 'mm_'

    if selected_data['ExposureTime'][0] < selected_data['ExposureTime'][1]:
        new_filename += str(selected_data['ExposureTime'][0] / 10) + '-' + str(selected_data['ExposureTime'][1] / 10) + 's_'
    else:
        new_filename += str(selected_data['ExposureTime'][0] / 10) + 's_'

    new_filename += 'f' + str(selected_data['MaxApertureValue'][0] / selected_data['MaxApertureValue'][1]) + '_'
    new_filename += 'ISO-' + str(selected_data['ISOSpeedRatings'])
    
    return new_filename.replace('.0', '')

def check_for_raw_file(path, f):
    f_raw = f.casefold().replace('.jpg', '.nef')
    if os.path.isfile(path + '\\' + f_raw):
        return f_raw
    else:
        return False

def rename_files(path):
    try:
        for f in listdir(path):
            if isfile(join(path, f)) and f.casefold().endswith('.jpg'):
                original_file_path = path + '\\' + f
                exif = get_exif(original_file_path)
                selected_data = get_selected_exif(exif)
                if not check_for_empty_values(selected_data):
                    print('renaming JPG file...')
                    new_file_path = path + '\\' + build_new_filename(selected_data) + '.jpg'
                    # os.rename(original_file_path, new_file_path)
                    f_raw = check_for_raw_file(path, f)
                    if f_raw:
                        print('and renaming NEF file too...')
                print('new filename:')
                print(build_new_filename(selected_data))
                print(sys.argv[1])
    except FileNotFoundError:
        print('Error: file not found. Please make sure you provided correct path.')

# path = 'D:\python_test_photos'
# onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
# exif = get_exif(path + '\photo.jpg')
# selected_data = get_selected_exif(exif)

# os.rename(r'D:\python_test_photos\photo.jpg', r'D:\python_test_photos\photo_renamed.jpg')

#######################

try:
    path = sys.argv[1]
    rename_files(path)
except IndexError:
    print('Error: no argument provided. Please provide an absolute path to the directory containing files you want to rename.')


#######################

#print(onlyfiles)
