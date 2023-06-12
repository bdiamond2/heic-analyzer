import pyheif
import piexif
from datetime import datetime
import math


class HEICSimple:
    count = 0

    def __init__(self, path):
        HEICSimple.count += 1
        self.id = HEICSimple.count
        self.path = path
        self.heif = pyheif.read(self.path)

        # set EXIF dictionary
        metadata = self.heif.metadata
        exif_data_bytes = metadata[0]['data']
        self.exif_dict = piexif.load(exif_data_bytes)

        self.dt = datetime.strptime(self.exif_dict['0th'][306].decode('utf-8'),
                                    "%Y:%m:%d %H:%M:%S")
        lat_long = self.decode_gps()
        self.lat = lat_long[0]
        self.long = lat_long[1]

    def decode_gps(self):
        gps_tag = self.exif_dict['GPS']
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
        lat_dec = lat_factor * HEICSimple.exif_dms_to_dec(lat)
        long_dec = long_factor * HEICSimple.exif_dms_to_dec(long)
        return [lat_dec, long_dec]

    # helper function that transforms an EXIF deg/min/sec to a simple decimal number
    def exif_dms_to_dec(dms):
        return (dms[0][0] / dms[0][1]) + (dms[1][0] / dms[1][1])/60 + (dms[2][0] / dms[2][1])/3600

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.__str__()


class HEICDiff:
    def __init__(self, heic1, heic2):
        self.heic1 = heic1
        self.heic2 = heic2
        self.tdelta = heic1.dt - heic2.dt
        self.distance = math.sqrt(
            (heic1.lat - heic2.lat)**2 + (heic1.long - heic2.long)**2
        )

    def tdelta_seconds(self):
        return abs(round(self.tdelta.total_seconds()))

    def dist_meters(self):
        return round(111139 * self.distance)

    def __str__(self):
        return f'{self.heic1}, {self.heic2}: {self.tdelta_seconds()} seconds and {self.dist_meters()} meters apart'
