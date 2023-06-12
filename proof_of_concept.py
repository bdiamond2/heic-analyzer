import pyheif
import piexif
from datetime import datetime
import os
import pprint
import math


# takes the path of an HEIC image and returns the datetime and geotag
# as a lat/long in a list
def heic_dt_gps(image_path):
    # Open the HEIC image using pyheif
    heif_file = pyheif.read(image_path)

    # Extract the metadata from the image
    metadata = heif_file.metadata
    exif_data_bytes = metadata[0]['data']
    exif_dict = piexif.load(exif_data_bytes)

    # EXIF reference:
    # https://exiv2.org/tags.html
    # dt = exif_dict['0th'][306].decode('utf-8')
    dt = datetime.strptime(exif_dict['0th'][306].decode(
        'utf-8'), "%Y:%m:%d %H:%M:%S")
    lat_long = decode_gps(exif_dict['GPS'])
    return [dt, lat_long]

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


def list_files(path):
    fns = []
    for fn in os.listdir(path):
        fns.append(os.path.join(path, fn))
    return fns

batch1 = list_files('test_heics/batch_1')
batch2 = list_files('test_heics/batch_2')

batch1_data = {}
for heic in batch1:
    batch1_data[heic] = heic_dt_gps(heic)

batch2_data = {}
for heic in batch2:
    batch2_data[heic] = heic_dt_gps(heic)

comp = {}
deg_to_m = 111139
for img1 in batch1_data:
    comp[img1] = {}
    for img2 in batch2_data:
        tdelta = (batch1_data[img1][0] - batch2_data[img2][0]).total_seconds()
        p1 = batch1_data[img1][1]
        p2 = batch2_data[img2][1]
        dist = deg_to_m * math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        comp[img1][img2] = [tdelta, dist]

pprint.pprint(comp)

# pprint.pprint('batch 1:')
# pprint.pprint(batch_1_data)

# pprint.pprint('\nbatch 2:')
# pprint.pprint(batch_2_data)
