from exif import Image
from geopy.geocoders import Nominatim
import os

base_dir = 'TestFiles'

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

    if img.has_exif:
        try:
            coords = (decimal_coords(img.gps_latitude,
                      img.gps_latitude_ref),
                      decimal_coords(img.gps_longitude,
                      img.gps_longitude_ref))
        except AttributeError:
            print ('No Coordinates Available')
    else:
        print ('The Image has no EXIF information')
        
    return({"datetime":img.datetime_original, "latitude":coords[0],"longitude":coords[1]})

for file in os.listdir(base_dir):
    if file.endswith(".jpg"):

        #Analyze an image
        info = image_information(base_dir + "/" + file)
        location = geoloc.reverse(str(info["latitude"]) + "," + str(info["longitude"])).raw['address']

        country = location['country']
        county = "NA"

        if 'county' in location:
            county = location['county']

        place = "NA"
        if 'city' in location:
            place = location["city"]
        elif 'town' in location:
            place = location["town"]
        elif 'village' in location:
            place = location["village"]

        #print(location)
        print(file + ": " +place + ", " + county + ", " + country + "\n")
