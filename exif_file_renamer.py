# imports for reading filenames
from os.path import isfile, join

# import for file renaming
import os

# import for using arguments
import sys

# program's modules
import messages
import exif_reader

def is_any_value_empty(selected_data):
    for key in selected_data:
        if selected_data[key] == '':
            return True
    return False

def build_new_filename(selected_data):
    selected_data['EXIF DateTimeOriginal'] = selected_data['EXIF DateTimeOriginal'].replace(':', '')
    selected_data['EXIF DateTimeOriginal'] = selected_data['EXIF DateTimeOriginal'].replace(' ', '_')
    
    new_filename = '{timestamp}{subsec}_{focal_length}mm_{exposure_time}s_f{fnumber}_ISO-{iso}'.format(
        timestamp = selected_data['EXIF DateTimeOriginal'][2:],
        subsec = selected_data['EXIF SubSecTimeOriginal'],
        focal_length = selected_data['EXIF FocalLength'],
        exposure_time = selected_data['EXIF ExposureTime'].replace('/', '-'),
        fnumber = get_proper_fnumber(selected_data['EXIF FNumber']),
        iso = selected_data['EXIF ISOSpeedRatings']
    )

    return new_filename.replace('.0', '')

def get_proper_fnumber(exif_fnumber):
    proper_fnumber = exif_fnumber
    if '/' in exif_fnumber:
        split = exif_fnumber.split('/')
        proper_fnumber = float(split[0]) / float(split[1])
    return proper_fnumber

def handle_duplicate_filename(path):
    path_splitted = path.split('\\')
    filename = path_splitted[-1]
    filename_splitted = filename.split('_')
    last_filename_segment = filename_splitted[-1].split('.')[0]
    file_extension = filename_splitted[-1].split('.')[1]

    if filename_splitted[-1].startswith('ISO'):
        return path[:-4] + '_2.' + file_extension
    else: # last fragment must be a number
        last_filename_segment = str(int(last_filename_segment) + 1)
        filename_splitted[-1] = last_filename_segment + '.' + file_extension
        filename = '_'.join(filename_splitted)
        path_splitted[-1] = filename
        return '\\'.join(path_splitted)

def rename_file(original_file_path, new_file_path):
    try:
        os.rename(original_file_path, new_file_path)
    except FileExistsError:
        rename_file(original_file_path, handle_duplicate_filename(new_file_path))

def is_jpg_or_nef(f):
    return f.casefold().endswith('.jpg') or f.casefold().endswith('.nef')

def get_file_extension_suffix(f):
    file_extension_suffix = ''
    if f.endswith('.jpg'):
        file_extension_suffix = '.jpg'
    elif f.endswith('.nef'):
        file_extension_suffix = '.nef'
    return file_extension_suffix

def rename_files(path, files_count):
    try:
        scanned_jpg_files_count = 0
        scanned_raw_files_count = 0
        renamed_jpg_files_count = 0
        renamed_raw_files_count = 0
        scanned_files_count = 0
        attribute_errors = []
        print('Scanning...')
        for root, dirs, files in os.walk(path):
            for f in files:
                messages.show_file_renaming_progress(scanned_files_count, files_count, join(root, f))
                if isfile(join(root, f)) and is_jpg_or_nef(f):
                    try:
                        file_extension_suffix = get_file_extension_suffix(f.casefold())
                        if file_extension_suffix == '.jpg':
                            scanned_jpg_files_count = scanned_jpg_files_count + 1
                        elif file_extension_suffix == '.nef':
                            scanned_raw_files_count = scanned_raw_files_count + 1
                        original_file_path = root + '\\' + f
                        exif = exif_reader.get_exif(original_file_path)
                        selected_data = exif_reader.get_selected_exif(exif)
                        if not is_any_value_empty(selected_data):
                            # renaming file
                            new_filename = build_new_filename(selected_data)
                            new_file_path = root + '\\' + new_filename + file_extension_suffix
                            if original_file_path.lower() != new_file_path.lower():
                                rename_file(original_file_path, new_file_path)
                                if file_extension_suffix == '.jpg':
                                    renamed_jpg_files_count = renamed_jpg_files_count + 1
                                elif file_extension_suffix == '.nef':
                                    renamed_raw_files_count = renamed_raw_files_count + 1
                    except AttributeError:
                        attribute_errors.append(original_file_path)
                scanned_files_count = scanned_files_count + 1
        print()
        messages.print_attribute_error_logs(attribute_errors)
        messages.print_file_count_logs(
            scanned_jpg_files_count,
            scanned_raw_files_count,
            renamed_jpg_files_count,
            renamed_raw_files_count,
            scanned_files_count
        )

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
        print('The program is going to iterate through {} files.'.format(files_count))
        print('Are you sure? [y/n]')
        yes = {'yes', 'y'}
        choice = input().lower()
        if choice in yes:
            rename_files(path, files_count)
    else:
        print('No files found in the directory. Make sure you provided a correct path.')
except IndexError:
    print('Error: no argument provided. Please provide an absolute path to the directory containing files you want to rename.')