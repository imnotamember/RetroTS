__author__ = 'Joshua Zosky'
import GetPath as getpath
import os, datetime


def get_file_attributes(filename):
    """
    Returns a dictionary with the same information as 'listing = dir (name)' in Matlab
    :param filename: filename, path and extension included. I.E. 'C:\folder\brik.head'
    :return: file_attributes: a dictionary with these key-value pairs:
        name: name of file and extension
        date: modification date timestamp
        bytes: size of file in bytes
        is_a_directory: 'True' if filename is a directory, 'False' if not
    """
    err, pathname, filename = getpath.get_path(filename)
    date = 'N/A'
    bytes = 'N/A'
    if filename != 0 and filename != '':
        name = filename
        bytes = os.path.getsize(filename)
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
                       'Size in bytes':bytes,
                       'Is a directory':is_a_directory}
    return file_attributes

def zglobb(identifiers, list_type='list', remove_ext=''):
    """
    Returns the list of files specified in Identifiers
        Example Usage:  err, error_message, file_list = zglobb(identifiers, list_type='l', no_ext='')
                        or
                        file_list =  zglobb(identifiers, list_type='l', no_ext='')
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

    number_of_bricks = len(identifiers)
    count = 0
    i = 0
    for item in identifiers:
        # grab the path if it is there
        gp_error, gp_path, gp_file = getpath.get_path(str(item))
        if gp_path[-1] != os.sep:
            gp_path = gp_path + os.sep
        some_info = get_file_attributes(item)
        for item in some_info:
            print "%s: %s" % (item, some_info[item])
