from datetime import datetime
import os
import shutil

import ImageRecord
import ImageMetadata
from Config import *

def main():
    copied = 0

    files = os.listdir(image_dir)

    for i, file in enumerate(files):
        if file.endswith((".jpg", ".JPG", ".jpeg", ".JPEG")):
            print(f"[{i + 1}/{len(files)}] ", end='')

            # If the file isn't in the destination folder
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
                
                # Copy the image to the path generated with its metadata
                else:
                    print(f"Copying image {file} to {path}")
                    os.makedirs(os.path.dirname(path + '/'), exist_ok=True)
                    
                    shutil.copyfile(f"{image_dir}/{file}", f"{path}/{file}")

                    copied += 1
            else:
                print(f'- File {file} already in destination')
        
        # MP4 videos can't be properly classified, but copy them anyways
        elif file.endswith((".mp4", ".MP4")):
            print(f"[{i + 1}/{len(files)}] ", end='')

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