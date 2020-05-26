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