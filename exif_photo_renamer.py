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

def handle_duplicate_filename(path):
    path_splitted = path.split('\\')
    filename = path_splitted[-1]
    filename_splitted = filename.split('_')
    last_filename_segment = filename_splitted[-1].split('.')[0]
    file_extension = filename_splitted[-1].split('.')[1]

    if filename_splitted[-1].startswith('ISO'):
        # print(path[:-4] + '_2.' + file_extension)
        return path[:-4] + '_2.' + file_extension
    else: # last fragment must be a number
        last_filename_segment = str(int(last_filename_segment) + 1)
        filename_splitted[-1] = last_filename_segment + '.' + file_extension
        filename = '_'.join(filename_splitted)
        path_splitted[-1] = filename
        # print('\\'.join(path_splitted))
        return '\\'.join(path_splitted)

def rename_file(original_file_path, new_file_path):
    try:
        os.rename(original_file_path, new_file_path)
    except FileExistsError:
        rename_file(original_file_path, handle_duplicate_filename(new_file_path))

def print_attribute_error_logs(attribute_errors):
    if len(attribute_errors) == 1:
        print("Warning! AttributeError has occured. This file couldn't be renamed:")
        print(attribute_errors[0])
    elif len(attribute_errors) > 1:
        print("Warning! AttributeError has occured. The following files couldn't be renamed:")
        for f in attribute_errors:
            print(f)

def print_file_count_logs(jpg, raw):
    if jpg == 0:
        print("Didn't rename any files.")
    elif raw == 0:
        print('Done! Renamed '+\
            str(jpg)+\
            ' JPG files. ')
    else:
        print('Done! Renamed '+\
            str(jpg)+\
            ' JPG files and '+\
            str(raw)+\
            ' RAW files ('+\
            str(jpg + raw)+\
            ' files total).')

def rename_files(path, files_count):
    try:
        renamed_jpg_files_count = 0
        renamed_raw_files_count = 0
        scanned_files_count = 0
        attribute_errors = []
        print('Scanning...')
        for root, dirs, files in os.walk(path):
            for f in files:
                # print(join(root, f))
                progress_percentage = (scanned_files_count / files_count) * 100
                print('Progress: ' + "%.2f" % round(progress_percentage, 2) + '%. File: ' + join(root, f))
                if isfile(join(root, f)) and f.casefold().endswith('.jpg'):
                    try:
                        original_file_path = root + '\\' + f
                        exif = get_exif(original_file_path)
                        selected_data = get_selected_exif(exif)
                        if not check_for_empty_values(selected_data):
                            # renaming JPG file
                            new_filename = build_new_filename(selected_data)
                            new_file_path = root + '\\' + new_filename + '.jpg'
                            if original_file_path.lower() != new_file_path.lower():
                                rename_file(original_file_path, new_file_path)
                                renamed_jpg_files_count = renamed_jpg_files_count + 1
                            f_raw = check_for_raw_file(root, f)
                            if f_raw:
                                # renaming NEF file
                                original_file_path = root + '\\' + f_raw
                                new_file_path = root + '\\' + new_filename + '.nef'
                                if original_file_path.lower() != new_file_path.lower():
                                    rename_file(original_file_path, new_file_path)
                                    renamed_raw_files_count = renamed_raw_files_count + 1
                    except AttributeError:
                        attribute_errors.append(original_file_path)
                scanned_files_count = scanned_files_count + 1
        print()
        print_attribute_error_logs(attribute_errors)
        print_file_count_logs(renamed_jpg_files_count, renamed_raw_files_count)

    except FileNotFoundError:
        print('Error: file not found. Please make sure you provided correct path.')

def count_files(path):
    count = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            count = count + 1
    return count

try:
    path = sys.argv[1]
    print('Counting files...')
    files_count = count_files(path)
    if files_count > 0:
        print('The program is going to iterate through ' + str(files_count) + ' files.')
        print('Are you sure? [y/n]')
        yes = {'yes', 'y'}
        choice = input().lower()
        if choice in yes:
            rename_files(path, files_count)
    else:
        print('No files found in the directory.')
except IndexError:
    print('Error: no argument provided. Please provide an absolute path to the directory containing files you want to rename.')