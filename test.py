import pyheif
import piexif
import pprint

def extract_geotag_data(image_path):
    # Open the HEIC image using pyheif
    heif_file = pyheif.read(image_path)

    # Extract the metadata from the image
    metadata = heif_file.metadata
    exif_data_bytes = metadata[0]['data']
    exif_dict = piexif.load(exif_data_bytes)
    # pprint.pprint(exif_dict)

    # EXIF reference:
    # https://exiv2.org/tags.html
    dt = exif_dict['0th'][306].decode('utf-8')
    lat_long = decode_gps(exif_dict['GPS'])
    print(dt, lat_long)

# takes the 'GPS' tag of EXIF data and returns it as a simple
# decimal lat/long list
def decode_gps(gps_tag):
    lat_ref = gps_tag[1]
    lat = gps_tag[2]
    long_ref = gps_tag[3]
    long = gps_tag[4]

    if lat_ref == b'N':
        lat_factor = 1
    else:
        lat_factor = -1

    if long_ref == b'W':
        long_factor = -1
    else:
        long_factor = 1

    # example: ((42, 1), (16, 1), (4573, 100))
    lat_dec = lat_factor * exif_dms_to_dec(lat)
    long_dec = long_factor * exif_dms_to_dec(long)
    return [lat_dec, long_dec]

# helper function that transforms an EXIF deg/min/sec to a simple decimal number
def exif_dms_to_dec(dms):
    return (dms[0][0] / dms[0][1]) + (dms[1][0] / dms[1][1])/60 + (dms[2][0] / dms[2][1])/3600

img = "IMG_7589.HEIC"

# Extract geotag metadata from the image
extract_geotag_data(img)