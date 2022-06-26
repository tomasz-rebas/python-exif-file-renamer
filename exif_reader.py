import exifread

def get_selected_exif(exif):
    selected_data = {
        'EXIF DateTimeOriginal': '',
        'EXIF FNumber': '',
        'EXIF FocalLength': '',
        'EXIF SubSecTimeOriginal': '',
        'EXIF ExposureTime': '',
        'EXIF ISOSpeedRatings': ''
    }

    for tag in exif.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            if tag in selected_data:
                selected_data[tag] = '%s' % (exif[tag])
    return selected_data

def get_exif(filename):
    # Open image file for reading (must be in binary mode)
    f = open(filename, 'rb')
    tags = exifread.process_file(f)
    return tags