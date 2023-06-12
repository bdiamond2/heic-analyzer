from heicsimple import *
import os

# img = HEICSimple('IMG_7589.HEIC')
# print(img)
# print(img.id)
# print(img.path)
# print(img.dt)
# print(img.lat)
# print(img.long)


def get_heic_batch(path):
    heics = []
    for fn in os.listdir(path):
        heics.append(HEICSimple(os.path.join(path, fn)))
    return heics


batch1 = get_heic_batch('test_heics/batch_1')
batch2 = get_heic_batch('test_heics/batch_2')

for i in batch1:
    for j in batch2:
        diff = HEICDiff(i, j)
        if diff.tdelta_seconds() < 3600*6 and diff.dist_meters() < 1000:
            print(diff)
