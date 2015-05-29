__author__ = 'Joshua Zosky'
import os, datetime
from os import listdir
from os.path import isfile, join
from GetPath import get_path

def get_file_attributes(filename, list_directory=0):
    """
    Returns a dictionary with the same information as 'listing = dir (name)' in Matlab
    :param  filename: filename, path and extension included. I.E. 'C:\folder\brik.head'
            or
            filename: a list of filenames in a directory as specified by 'list_directory'.
    :param  list_directory: default is zero(0) if filename refers to a single filename
            or
            list_directory: a string with the directory which contains the files in the 'filename' if a list
    :return: file_attributes: a dictionary with these key-value pairs:
        name: name of file and extension
        date: modification date timestamp
        file_bytes: size of file in bytes
        is_a_directory: 'True' if filename is a directory, 'False' if not
    """
    err, pathname, filename = get_path(filename)
    date = 'N/A'
    file_bytes = 'N/A'
    #if list_directory !=
    if filename != 0 and filename != '':
        name = filename
        file_bytes = os.path.getsize(filename)
        is_a_directory = False
        try:
            mtime = os.path.getmtime(filename)
        except OSError:
            mtime = 0
        date = datetime.datetime.fromtimestamp(mtime)
    elif pathname != 0 and pathname != '':
        name = pathname
        is_a_directory = True
    else:
        name = 'error'
        is_a_directory = False
    file_attributes = {'File name':name,
                       'Date modified':date,
                       'Size in bytes':file_bytes,
                       'Is a directory':is_a_directory}
    return file_attributes

def zglobb(identifiers, list_type='list', remove_ext=''):
    """
    Returns the list of files specified in Identifiers
        Example Usage:  err, error_message, file_list = zglobb(identifiers, list_type='l', remove_ext='')
                        or
                        file_list =  zglobb(identifiers, list_type='l', remove_ext='')
    :param identifiers: Identifiers is a list identifying which briks to use
        Example: identifiers = ['ADzst2r*ir.alnd2AAzs+orig.HEAD' , 'AFzst2r*ir.alnd2AAzs+orig.HEAD']
    :param list_type: type of output list
        Options:    'list' (default) Create a list with values identical to those returned by dir
                    'string' Create a '|' delimited string with all the file names in it
    :param remove_ext: (default is '') a string containing a '|' delimited list of filename extensions to remove
        example '.HEAD|.BRIK'
    :return: a tuple with 3 values: (err, error_message, file_list)
        err : 0 = No Problem/1 = Mucho Problems
        error_message : Any error or warning messages
        file_list : the list of files with a format depending on 'list_type'
    """
    # Initialize return variables
    err = 1
    error_message = 'Undetermined'
    file_list = ''
    if list_type == 'list':
        file_list = []
    elif list_type == 'string':
        file_list = ''
    else:
        error_message = '%s is an unknown Opt.LsType value' % list_type
        return err, error_message, file_list

    if isinstance(identifiers, basestring):
        identifiers = identifiers.split(',')
    for item in identifiers:
        item = str(item).strip()

    some_info_list = []
    number_of_bricks = len(identifiers)
    count = 0
    i = 0
    for item in identifiers:
        # grab the path if it is there
        gp_error, gp_path, gp_file = get_path(str(item))
        if gp_path != '':
            check_error = False
            if gp_file == '':
                directory_files = [join(gp_path, f) for f in listdir(gp_path) if isfile(join(gp_path, f))]
                print directory_files
                for next_file in directory_files:
                    some_info_list.append(get_file_attributes(next_file))
                    print some_info_list
        elif gp_file != '':
            check_error = False
            some_info_list.append(get_file_attributes(item))
        else:
            check_error = True
            error_message = 'Identifier item is not a file or directory'
        if not check_error:
            for some_info in some_info_list:
                for some_item in some_info:
                    print "%s: %s" % (some_item, some_info[some_item])
