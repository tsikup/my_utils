import glob
import re
import os
import sys
import math
import fnmatch


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


def findfiles(which, where=".", ignore_case=True):
    """
    Returns list of filenames from `where` path matched by 'which'
    shell pattern. Matching is case-insensitive.
    :param which:
    :param where:
    :param ignore_case:
    :return:
    """

    # TODO: recursive param with walk() filtering
    if ignore_case:
        rule = re.compile(fnmatch.translate(which), re.IGNORECASE)
    else:
        rule = re.compile(fnmatch.translate(which))
    return [name for name in os.listdir(where) if rule.match(name)]


def get_image_path(folders, patient_id, ignore_case=True, ext=".ndpi"):
    s_name = patient_id + "*" + ext
    s_path = None
    for in_folder in folders:
        for _num in range(5):
            if _num > 0:
                _s_path = os.path.join(in_folder, patient_id + "_" + str(_num) + ext)
            else:
                _s_path = os.path.join(in_folder, patient_id + ext)
            if os.path.exists(_s_path):
                return _s_path
        _s_path = findfiles(s_name, in_folder, ignore_case=ignore_case)
        if len(_s_path) == 0:
            continue
        if len(_s_path) > 1:
            raise ValueError(f"More than one file found for {s_name}.")
        if s_path is not None:
            raise ValueError(
                f"More than one file found for {s_name} in different folders."
            )
        s_path = os.path.join(in_folder, _s_path[0])
    return s_path
