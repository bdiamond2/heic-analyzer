import exifread
import pyheif
from io import BytesIO

def print_metadata(heic_path):
    heif_file = pyheif.read(heic_path)
    metadata = heif_file.metadata

    for item in metadata or []:
        if item['type'] == 'Exif':
            byte_string = item['data']
            break

    image_file = BytesIO(byte_string)
    tags = exifread.process_file(image_file)
    print(tags)

# Example usage
heic_path = 'test_heics/batch_1/IMG_7589.HEIC'
print_metadata(heic_path)

