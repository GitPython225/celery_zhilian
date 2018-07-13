import os
from pybloom_live import BloomFilter
import struct


def bloom_url(url):
    is_exist = os.path.exists(r'C:\spiders\zhilian_celery\bloom.blm')
    if is_exist:
        bf = BloomFilter.fromfile(open(r'C:\spiders\zhilian_celery\bloom.blm', 'rb', buffering=40))
    else:
        bf = BloomFilter(10000000, 0.001)

        # for animal in animals:
    if url in bf:
        print(1)
        return 0
    else:
        bf.add(url)
        bf.tofile(open(r'C:\spiders\zhilian_celery\bloom.blm', 'wb'))
        return 1