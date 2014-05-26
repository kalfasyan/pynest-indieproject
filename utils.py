import os
import re
import numpy as np
import json


def extract_trace(d, gid):
    """
    d : voltage trace data (column 1: GID (int), col 2: time (float), col 3: voltage)
    gid : cell_gid
    """
    indices = (d[:, 0] == gid).nonzero()[0]
    time_axis, volt = d[indices, 1], d[indices, 2]
    return time_axis, volt


def find_files(folder, to_match):
    """
    Use re module to find files in folder and return list of files matching the 'to_match' string
    Arguments:
    folder -- string to folder
    to_match -- a string (regular expression) to match all files in folder
    """
    assert (to_match != None), 'utils.find_files got invalid argument'
    list_of_files = []
    for fn in os.listdir(folder):
        m = re.match(to_match, fn)
        if m:
            path = folder + fn
            list_of_files.append(path)
    return list_of_files

