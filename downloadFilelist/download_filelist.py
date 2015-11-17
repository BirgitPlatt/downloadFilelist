#!/usr/bin/env python3.5
# coding=utf-8

import sys
import os
import codecs
import collections
from datetime import datetime
from optparse import OptionParser  # used in __main__
import wget
""" downloadFilelist requires module wget

    wget:
    Public domain by anatoly techtonik <techtonik@gmail.com>
    Also available under the terms of MIT license
    Copyright (c) 2010-2015 anatoly techtonik
"""
__version__ = "1.2"
__author__ = "Birgit Platt"


usage = """
usage: download_filelist.py <filename> [options]

options:
  -o --output <dir>           output directory
                                  to be used for saving instead of current dir
  -e --encoding <encoding>    encoding of filename, if not specified
                                  "preferred encoding" is used instead
  -h --help

returncodes: 
  -1: failure
   other: number of failed lines
"""

DATETIME_MASK_FOR_PRINT = "%Y-%m-%d %H:%M:%S"


def download_url_filelist(filelist, out=None, encoding=None):
    """
    This function takes a file containing one URL per line
    and downloads the corresponding file to out dirctory.

    UTF-8 should be used as encoding of filelist, if non-ANSI chars are to
    be expected in the contained URLs. Parameter encoding should be set to
    utf-8 in this case - otherwise URLs containing non-ANSI chars would fail
    to download.

    wget.download() is used for downloding the files referenced by the URLs

    :param out:      output directory
                     if out=None files are stored in current directory
                         this is default behavior of wget.download()
    :param encoding: encoding of filelist
                     if encoding=None locale.getpreferredencoding() is used

    :return:         Namedtuple('success_count', 'error_count')
                     None to indicate failure
    """

    # counters for success and error
    success_count = 0
    error_count = 0

    if (out is not None):
        # if out is not valid wget.download will not work correctly
        if(not os.path.exists(out)):
            print("FAILED: out directory '{0:s}' doesn't exist".format(out))
            return None
        if(not os.path.isdir(out)):
            print(
                "FAILED: out directory '{0:s}' is not a directory".format(out))
            return None

    try:
        # Using errors='replace' instead of (default) errors='strict' to make
        # iteration continue even if a line has an encoding error. This way we
        # get a line with '\ufffd' (REPLACEMENT CHARACTER) in place of
        # conflicting chars instead of the original line.
        # 'strict' error handling would raise a ValueError exception when
        # reading the "problematic" line and stop the completion of the loop.
        # Following lines would not be processed, even if they could.

        errors = 'replace'
        with codecs.open(filelist, 'r', encoding, errors) as f:
            for line in f:

                # First line might contain an additional char ("\ufeff")
                # ZERO WIDTH NO-BREAK SPACE  due to Byte Order Mark used in
                # file. This character will not be covered by the following
                # strip(), so we have to do it.Otherwise first line would
                # contain illegal char.
                if (not success_count and not error_count):
                    line = line.lstrip("\ufeff")

                filename = line.strip()
                try:
                    savedfile = wget.download(filename, out=out, bar=None)
                    # if no exception raised, this download was a success
                    success_count += 1
                    print("SUCCESS: '{0:s}' from {1:s}".format(
                        savedfile, filename))

                except Exception as e:
                    error_count += 1

                    # check for encoding errors (result of errors='replace')
                    found_at = line.find('\ufffd')
                    if (found_at != -1):
                        info = "character at {0:d} doesn't match encoding={1:s}"
                        exception_info = information.format(found_at, encoding)
                    else:
                        # create generic error message
                        error_type = str(e.__class__.__name__)
                        error_text = str(e)
                        exception_info = error_type + ": " + error_text

                    print("ERROR: '{0:s}' download failed ({1:s})".format(
                        filename, exception_info))

            # all lines processed, now generate result namedtuple of the two
            # counters
            result = collections.namedtuple('DownloadUrlListResult',
                                            ['success_count', 'error_count'])
            result.success_count, result.error_count = success_count, error_count
            return result

    except Exception as e:
        error_type = str(e.__class__.__name__)
        error_text = str(e)
        exception_info = error_type + ": " + error_text

        print("FAILED: {0:s}".format(exception_info))

        # continuation impossible
        return None


if __name__ == "__main__":

    try:
        # return usage text if less then arguments or help is explicitly
        # requested:
        if len(sys.argv) < 2 or "-h" in sys.argv or "--help" in sys.argv:
            sys.exit(usage)

        # if run by Python 2.x on Windows machine, convert arguments to unicode
        if not wget.PY3K and sys.platform == "win32":
            sys.argv = wget.win32_utf8_argv()

        # patch Python to write unicode characters to console (from wget main)
        if sys.platform == "win32":
            wget.win32_unicode_console()

        parser = OptionParser()
        parser.add_option("-o", "--output", dest="output")
        parser.add_option("-e", "--encoding", dest="encoding")

        (options, args) = parser.parse_args()

        destfolder = options.output
        encoding = options.encoding

        filelist = sys.argv[1]

        timestamp = datetime.now().strftime(DATETIME_MASK_FOR_PRINT)
        print("INFO: download_url_filelist '{0:s}' starts at {1:s}".format(
            filelist, timestamp))

        # this starts the actual processing of the given URL Filelist
        result = download_url_filelist(
            filelist, out=destfolder, encoding=encoding)
        if(result is None):
            sys.exit(-1)

        timestamp = datetime.now().strftime(DATETIME_MASK_FOR_PRINT)

        print("INFO: {0:s}, success:{1:d}, failed:{2:d} at {3:s}".format(
            "download_url_filelist finished", result.success_count,
            result.error_count, timestamp))

        sys.exit(result.error_count)

    except Exception as e:
        error_type = str(e.__class__.__name__)
        error_text = str(e)
        exceptionInfo = error_type + ": " + error_text

        print("EXCEPTION: download_filelist.py: exception in __main__ ({0:s})".format(
            exceptionInfo))
