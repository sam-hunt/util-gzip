'''
Created on 13 Nov 2016

@author: Sam
'''

import gzip, sys, argparse, fnmatch, os

def doGzipActions(directory, unixFilenamePattern='*', recursiveSubdirs=False, doCompress=False, doDecompress=False, doOverwrite=False, doRemoveAfter=False, quiet=True):

    # Check that only one of the compress/decompress options is set, so that we don't get weird behaviour
    if doCompress and doDecompress:
        if not quiet:
            print('Only one action (doCompress or doDecompress) should be used per execution.')
        return

    for dir_path, _, file_names in os.walk(directory):
        if not quiet:
            print('Inspecting directory: "' + dir_path + '"')

        # Inspect each file in the directory
        for file_name in file_names:

            # Get the full file path of the file and check it matches our unix-style pattern
            file_path = dir_path + "/" + file_name
            if not fnmatch.fnmatch(file_name, unixFilenamePattern):
                continue

            # If we are decompressing, then check that the file ends in .gz
            if doDecompress and not file_path[-3:] == '.gz':
                continue

            # Dry run, so just report the files found, and continue
            if not quiet and not doCompress and not doDecompress:
                print('\tFile found: ' + file_name)
                continue

            if doDecompress:
                new_file_path = file_path[:-3]  # Remove the '.gz' extension
                if doOverwrite or not os.path.isfile(new_file_path):
                    if not quiet:
                        print('\tDecompressing file "' + file_name + '" to "' + new_file_path + '"')
                    with gzip.open(file_path, 'rb') as f_in, open(new_file_path, 'w') as f_out:
                        f_out.writelines(str(f_in.read(), 'latin'))
                    if doRemoveAfter:
                        os.remove(file_path)

            if doCompress:
                new_file_path = file_path + '.gz'
                if doOverwrite or not os.path.isfile(new_file_path):
                    if not quiet:
                        print('\tCompressing file "' + file_name + '" to "' + new_file_path + '"')
                    with open(file_path, 'rb') as f_in, gzip.open(new_file_path, 'wb') as f_out:
                        f_out.write(f_in.read())
                    if doRemoveAfter:
                        os.remove(file_path)
                        if not quiet:
                            print('\tDeleted source file "' + file_name + '"')

        if not recursiveSubdirs:
            break
    return


if __name__ == "__main__":

    # Initialize the command line interface 
    parser = argparse.ArgumentParser(description='Gzip up files in a directory.')
    parser.add_argument('dir', type=str, help='directory to look for files in')
    parser.add_argument('-p', '--unixpattern', type=str, default='*', help='unix pattern for matching specific files/folders')
    parser.add_argument('-c', '--compress', action='store_true', help='compress found files adding .gz to filename')
    parser.add_argument('-d', '--decompress', action='store_true', help='decompress found .gz files removing .gz from filename')
    parser.add_argument('-r', '--recursive', action='store_true', help='also look for files in subdirectories')
    parser.add_argument('-o', '--overwrite', action='store_true', help='overwrite existing files if they exist when compressing or decompressing')
    parser.add_argument('-a', '--alltheway', action='store_true', help='remove source files after compressing or decompressing')
    parser.add_argument('-v', '--verbose', action='store_true', help='show additional information while processing')

    # Parse command line arguments
    args = parser.parse_args()

    # Run the script
    doGzipActions(args.dir, args.unixpattern, args.recursive, args.compress, args.decompress, args.overwrite, args.alltheway, not args.verbose)
