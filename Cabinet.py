from exif import Image
from geopy.geocoders import Nominatim
from datetime import datetime
import os
import shutil
from unidecode import unidecode

import ImageRecord

# Arguments
image_dir = '/home/santiago/Proyectos/Cabinet/TestFiles'
destination_dir = '/home/santiago/Proyectos/Cabinet/SortedFiles'

geoloc = Nominatim(user_agent="GetLoc")

#Converts the coordinates to decimal
def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref =='W' :
        decimal_degrees = -decimal_degrees
    return decimal_degrees

#Gets the relevant image information from its metadata
def image_information(image_path):

    with open(image_path, 'rb') as src:
        img = Image(src)

    if img.has_exif and img.datetime_original is not None:
        try:
            coords = (decimal_coords(img.gps_latitude,
                      img.gps_latitude_ref),
                      decimal_coords(img.gps_longitude,
                      img.gps_longitude_ref))
        except AttributeError:

            # There is EXIF date Information, but no coordinates
            return({"coordinates":False, "year":img.datetime_original.split(":")[0]})
    else:
        raise Exception("The Image has no EXIF information")
        
    return({"coordinates":True, "year":img.datetime_original.split(":")[0], "latitude":coords[0],"longitude":coords[1]})

# Makes the path to which copy the image based on its metadata
def make_path(info):
    if info["coordinates"]:
        location = geoloc.reverse(f"{str(info['latitude'])},{str(info['longitude'])}", language="en").raw["address"]

        country = location['country']

        #Get the county of the location
        county = None

        if 'county' in location:
            county = location['county']

        #Get the town of the location
        town = None
        if 'city' in location:
            town = location["city"]
        elif 'town' in location:
            town = location["town"]
        elif 'village' in location:
            town = location["village"]

        #print(location)

        if county is not None:
            #print(file + ": " + county + ", " + country + " (" + info["year"] + ")")
            path = "/".join([destination_dir, info["year"], country, county])
        else:
            #print(file + ": " + town + ", " + country + " (" + info["year"] + ")")
            path = "/".join([destination_dir, info["year"], country, town])
        
        path = unidecode(path)
    else:
        path = "/".join([destination_dir, info["year"], "Unknown"])

    return path

def main():
    copied = 0

    for file in os.listdir(image_dir):
        if file.endswith((".jpg", ".JPG", ".mp4")):
            hash = ImageRecord.get_hash(image_dir + "/" + file)

            print(file + ': ' + hash)
            '''
            #Analyze an image and generate its path
            try:
                info = image_information(image_dir + "/" + file)
                path = make_path(info)

            # If there's no EXIF metadata available, copy it to the unknown subfolder
            except:

                #Verify if an image with the same name exists
                if(os.path.isfile(f"{destination_dir}/Unknown/")):
                    print(f"Image {file} is already in destination directory. Skipping")
                else:
                    print(f"Error. Image {file} couldn't be classified. Moving to {destination_dir}/Unknown/")
                    os.makedirs(os.path.dirname(f"{destination_dir}/Unknown/"), exist_ok=True)
                    shutil.copyfile(f"{image_dir}/{file}", f"{destination_dir}/Unknown/{file}")

                    copied += 1
            
            # If there was metadata, copy the image to the generated path, first verify if an image with the same name exists
            # Which are the odds of two different images having the exact same name and location? Skip image if so
            else:
                if(os.path.isfile(f"{path}/{file}")):
                    print(f"Image {file} is already in destination directory. Skipping")
                else:
                    print(path)
                    os.makedirs(os.path.dirname(path + '/'), exist_ok=True)
                    shutil.copyfile(f"{image_dir}/{file}", f"{path}/{file}")

                    copied += 1

    # Write the copying date into the record, for reference purpose when making future copyings
    file = open(f"{destination_dir}/CabinetHistory.txt", "a")
    record = f"\n{datetime.now()}, {copied} images copied"
    file.write(record)
    file.close()'''

if __name__ == '__main__':
    main()