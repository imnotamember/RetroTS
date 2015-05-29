__author__ = 'Joshua Zosky'
import os


def get_path(path_string):
    """
    Breaks the string 'pathString' into a path and file part.
    :param path_string: a string (i.e. 'C:\Users\file.txt')
    :return: a tuple of three values: (err, p, f)
        err : 0=No Problem/1=Mucho Problem
        p = path component of string (i.e. 'C:\Users\')
        f = file component of string (i.e. 'file.txt')
    """
    err = 1
    p = '.'
    f = ''
    split_head_tail = os.path.split(path_string)
    if split_head_tail != ('', ''):
        err = 0
        p = split_head_tail[0]
        f = split_head_tail[1]
    return err, p, f
