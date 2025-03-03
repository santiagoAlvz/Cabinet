from datetime import datetime
import os
import shutil

import ImageRecord
import ImageMetadata
from Config import *

def main():
    copied = 0

    for file in os.listdir(image_dir):
        if file.endswith((".jpg", ".JPG", ".jpeg", ".JPEG")):
            if ImageRecord.verify(file):

                #Analyze an image and generate its path
                try:
                    info = ImageMetadata.image_information(image_dir + "/" + file)
                    path = ImageMetadata.make_path(info)

                # If there's no EXIF metadata available, copy it to the unknown subfolder
                except:

                    print(f"Image {file} couldn't be classified. Copying to {destination_dir}/Unknown/")
                    os.makedirs(os.path.dirname(f"{destination_dir}/Unknown/"), exist_ok=True)
                    shutil.copyfile(f"{image_dir}/{file}", f"{destination_dir}/Unknown/{file}")

                    copied += 1
                
                # If an image with the same name or identical hash exists in the destination, skip
                else:
                    print(f"Copying image {file} to {path}")
                    os.makedirs(os.path.dirname(path + '/'), exist_ok=True)
                    shutil.copyfile(f"{image_dir}/{file}", f"{path}/{file}")

                    copied += 1
            else:
                print(f'- File {file} already in destination')
        
        elif file.endswith((".mp4", ".MP4")):
            if ImageRecord.verify(file):
                print(f"Copying file {file} to {destination_dir}/Unknown/")
                os.makedirs(os.path.dirname(f"{destination_dir}/Unknown/"), exist_ok=True)
                shutil.copyfile(f"{image_dir}/{file}", f"{destination_dir}/Unknown/{file}")
                
                copied += 1
            else:
                print(f'- File {file} already in destination')
        
    ImageRecord.close()

    print(f"\nCopied {copied} files succesfully to the destination directory")

if __name__ == '__main__':
    main()