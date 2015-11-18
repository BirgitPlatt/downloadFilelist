# download_filelist

Small python project for a script that takes a plaintext file as an argument and 
downloads all images, storing them on the local hard disk. The file has one URL per line.

Project folder download_filelist contains the script download_filelist.py. 
Folder input_sample contains example filelists using different encodings.

This python project was developed using Visual Studio 2015 and python 3.5.0. 
It requires installation of module wget (https://pypi.python.org/pypi/wget/3.2).

wget is used for downloading the files. It handles file name conflicts 
by adding a (<Number>) postfix to the filename and handles URLs that specify 
different filenames in response header (Content-Disposition).

To get help for download_filelist.py just call it without parameters or add –h.
