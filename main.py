# -*- coding: utf-8 -*-
__author__ = 'dontsov'

import os
import argparse
from PIL import Image
import exifread
import tempfile


def rotate_dir(path):

    out_dir = os.path.join(path, 'edit')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for root, dirs, files in os.walk(path):
        for file in files:
            try:
                if file.lower().endswith(".jpg"):
                    file_path = os.path.join(root, file)

                    with open(file_path, 'r') as f:
                        tags = exifread.process_file(f)

                    img = Image.open(file_path)

                    if 'Image Orientation' in tags.keys():
                        direction = tags['Image Orientation'].values[0]
                        if direction == 3:  # из описания EXIF
                            img = img.transpose(Image.ROTATE_180)
                        if direction == 6:
                            img = img.transpose(Image.ROTATE_270)  # (Image.ROTATE_90)
                        elif direction == 8:
                            img = img.transpose(Image.ROTATE_90)

                    img = img.convert("RGB")  #  error if png
                    img.save(os.path.join(out_dir, file), 'JPEG', quality=95)
                    print 'Save: %s' % file
            except Exception, err:
                print 'Error: %s' % str(err)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Fotool')
    parser.add_argument('-d', '--dir', default='', help='directory')

    args = parser.parse_args()

    if args.dir:
        rotate_dir(args.dir)