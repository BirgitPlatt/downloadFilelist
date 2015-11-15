""" downloadFilelist requires module wget
    
    wget:
    Public domain by anatoly techtonik <techtonik@gmail.com>
    Also available under the terms of MIT license
    Copyright (c) 2010-2015 anatoly techtonik
"""
__version__ = "1.0"
__author__ ="Birgit Platt"

usage = """\
usage: downloadFilelist.py filename [options]

options:
  -o --output DIR           output directory
  -e --encoding ENCODING    encoding of filename
  -h --help
  --version
"""

import wget
import sys
import codecs


def downloadFilelist(filelist, out=None, encoding=None):
    """this function takes a file containing one URL per line 
       and donloads the corresponding file to current dirctory (default, if out=None)

       wget.download is used for downloding the files
  
    :param out: output directory
                if out=None files are stored in current directory
    :param encoding: encoding of filelist 
                if encoding=None locale.getpreferredencoding() is used

    :return:    (successCount, errorCount) 
    """
    
    #counters for success and error
    _successCount=0
    _errorCount=0

    try:
        with codecs.open(filelist, 'r' , encoding ) as f:
            for line in f:

                # first line might contain BOM
                if (_successCount == 0) and (_errorCount == 0):
                    # removeZERO WIDTH NO-BREAK SPACE at beginning of utf-8 string
                    ZWNBS = codecs.decode(b'\xEF\xBB\xBF', "utf-8" )
                    pos=line.find(ZWNBS)
                    if pos==0:
                        line=line.replace(ZWNBS, '', 1)
 
                try:
                    filename=line.strip()
                    savedfile=wget.download(filename,None,None);
                    _successCount+=1
                    print("SUCCESS: '" + savedfile + "' from " + filename)
   
                except Exception as e:
                    _errorCount+=1
                    exceptionInfo=str(e.__class__.__name__)+": "
                    for arg in e.args:
                        exceptionInfo+=str(arg)+", "
                    exceptionInfo=exceptionInfo.rstrip(", ")

                    print("EXCEPTION: '" + filename + "' download failed ("+exceptionInfo+")")

            return(_successCount,_errorCount)

    except Exception as e:
        exceptionInfo=str(e.__class__.__name__)+": "
        for arg in e.args:
            exceptionInfo+=str(arg)+", "

    print("ERROR: unable to open '" + filelist + "' ("+exceptionInfo+")")
    
    return(_doneCount,_errorCount)


if __name__ == "__main__":

    try:
        # parsing comandline arguments like wget:
        if len(sys.argv) < 2 or "-h" in sys.argv or "--help" in sys.argv:
            sys.exit(usage)

        if "--version" in sys.argv:
            sys.exit("downloadFilelist.py " + __version__)

        # patch Python 2.x to read unicode from command line
        if not wget.PY3K and sys.platform == "win32":
            sys.argv = wget.win32_utf8_argv()

        # patch Python to write unicode characters to console
        if sys.platform == "win32":
            wget.win32_unicode_console()

        from optparse import OptionParser
        parser = OptionParser()
        parser.add_option("-o", "--output", dest="output")
        parser.add_option("-e", "--encoding", dest="encoding")
        (options, args) = parser.parse_args()
    
        destfolder=options.output
        encoding=options.encoding

        filelist=sys.argv[1]
   
        DATETIME_MASK_FOR_PRINT="%Y-%m-%d %H:%M:%S"

        from datetime import datetime
        strTimestamp=datetime.now().strftime(DATETIME_MASK_FOR_PRINT)
        print("INFO: downloadFilelist '" + filelist +"' starts at "+strTimestamp)

        (doneCount, errorCount)=downloadFilelist(filelist, destfolder, encoding)

        strTimestamp=datetime.now().strftime(DATETIME_MASK_FOR_PRINT)
        print("INFO: downloadFilelist finished, success:"+str(doneCount)+" , failed:"+str(errorCount)+" at "+strTimestamp);

    except Exception as e:
        exceptionInfo=str(e.__class__.__name__)+": "
        for arg in e.args:
            exceptionInfo+=str(arg)+", "
        print("ERROR: downloadFilelist.py: unexpected exception in __main__ ("+exceptionInfo+")")
