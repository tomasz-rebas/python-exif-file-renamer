def print_attribute_error_logs(attribute_errors):
    if len(attribute_errors) == 1:
        print("Warning! AttributeError has occured. This file couldn't be renamed:")
        print(attribute_errors[0])
    elif len(attribute_errors) > 1:
        print("Warning! AttributeError has occured. The following files couldn't be renamed:")
        for f in attribute_errors:
            print(f)

def print_file_count_logs(scanned_jpg, scanned_raw, renamed_jpg, renamed_raw, all):
    if renamed_jpg > 0 or renamed_raw > 0:
        if renamed_jpg > 0 and renamed_raw > 0:
            print('Done! Renamed {} JPG files and {} RAW files ({} files total).'.format(
                renamed_jpg,
                renamed_raw,
                renamed_jpg + renamed_raw
            ))
        elif renamed_jpg > 0 and renamed_raw == 0:
            print('Done! Renamed {} JPG files. '.format(renamed_jpg))
        elif renamed_jpg == 0 and renamed_raw > 0:
            print('Done! Renamed {} RAW files. '.format(renamed_raw))

        not_renamed_jpg = scanned_jpg - renamed_jpg
        not_renamed_raw = scanned_raw - renamed_raw

        if not_renamed_jpg > 0 and not_renamed_raw == 0:
            print("{} JPG files were already renamed or couldn't be renamed.".format(not_renamed_jpg))
        elif not_renamed_jpg == 0 and not_renamed_raw > 0:
            print("{} RAW files were already renamed or couldn't be renamed.".format(not_renamed_raw))
        elif not_renamed_jpg > 0 and not_renamed_raw > 0:
            print("{} JPG files and {} RAW files were already renamed or couldn't be renamed.".format(
                not_renamed_jpg,
                not_renamed_raw
            ))

        other = all - scanned_jpg - scanned_raw
        if other > 0:
            print("The other {} files are of different formats and weren't renamed.".format(other))
        
    else:
        print("Didn't find any JPG/RAW files that required renaming.")
        print("Didn't rename any files.")

def show_file_renaming_progress(scanned_files_count, files_count, filepath):
    progress_percentage = (scanned_files_count / files_count) * 100
    print('Progress: ' + "%.2f" % round(progress_percentage, 2) + '%. File: ' + filepath)