# util-gzip
A simple command-line utility for compressing and decompressing files and folders

`usage: doGzipActions.py [-h] [-p UNIXPATTERN] [-c] [-d] [-r] [-o] [-a] [-v] dir`

```
Gzip up files in a directory.

positional arguments:
  dir                   directory to look for files in

optional arguments:
  -h, --help            show this help message and exit
  -p UNIXPATTERN, --unixpattern UNIXPATTERN
                        unix pattern for matching specific files/folders
  -c, --compress        compress found files adding .gz to filename
  -d, --decompress      decompress found .gz files removing .gz from filename
  -r, --recursive       also look for files in subdirectories
  -o, --overwrite       overwrite existing files if they exist when
                        compressing or decompressing
  -a, --alltheway       remove source files after compressing or decompressing
  -v, --verbose         show additional information while processing
```
