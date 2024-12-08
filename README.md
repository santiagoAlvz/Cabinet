# Cabinet

Cabinet is a Python script for automatically sorting a collection of pictures into categories using their date and location. When provided an origin and destination folder, Cabinet will read the metadata from all pictures in the folder, and copy the picture into the right subfolder in the destination, according to its year, country and the local place of taking.

![imagen](https://github.com/user-attachments/assets/477f3f9b-233d-4eb9-98d2-4d14816e5d1a)

## Usage
To use this script, the variables `image_dir` and `destination_dir` of the `Arguments` section must be assigned the route of the origin and destination folders, respectively. They must be enclosed in quotes as strings. Using absolute paths (i.e. starting at the root of the filesystem) is recommended.

Once these variables are assigned, the script must be run using Python.

Cabinet will iterate through all files in the origin folder with the appropiate file types (more info in the **Considerations** section), read their metadata, and copy them into the corresponding subfolder in the destination. Note that it won't iterate recursively through subfolders (it will only analyze and copy the files immediately in the origin folder).

There are 3 possible scenarios for classifying any given image, based on the information that Cabinet can recover from it.
1. Both original date and GPS coordinates of the image are available. Cabinet will then find the location country and local name using GeoPy's Nominatim geocoder, which relies on OpenStreetMap data. The image will be copied in the `[year]/[country]/[town/county/city]` subfolder.
2. Only original date is available. The image will be copied in the `[year]/Unknown` subfolder.
3. No metadata is recovered. The image will be copied in the `Unknown` subfolder.

As images are processed, their new path is printed. If there's any issue as it is also printed.

In the destination folder, the `CabinetHistory.txt` file is created and added a line with the execution datetime and the number of images copied. In subsequent runs to the same destination, new lines will be added to this file.

## Considerations
So far, only .jpg images and .mp4 videos are supported, as Cabinet relies on EXIF data. Note that not all mp4 files contain EXIF data. The whole script is built considering images taken with smartphones, which are mostly stored in these formats.

If an image destination path is already used by another image with the same name (something which may happen when performing multiple runs with the same destination folder), it will be skipped, since two images with the same name and classification are most likely the same image.

The local name used to classify an image may either be the city, town, village or county obtained when analyzing the image. This is because location information retrieved from GeoPy can be highly inconsistent between locations.
