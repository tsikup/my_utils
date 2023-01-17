import math
import sys


def getsizeof(obj):
    """
    Apply a set of filters to an image and optionally save and/or display filtered images.
    Args:
       obj: Object.
    Returns:
       size of object
    """
    size_bytes = sys.getsizeof(obj)
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])
