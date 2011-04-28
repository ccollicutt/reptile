#! /usr/bin/env python

import textile
import sys, os, shutil
from optparse import OptionParser
from Cheetah.Template import Template

VERSION = "0.1"
TEMPLATE = "templates/reptile.tpl"

def create_site(directory):

    dirs = os.listdir(directory)
    files = []
    # The point is this mumbo-jumbo is to only go down one level into the main dir
    for dir in dirs:
        dir_files = os.listdir(directory + "/" + dir)
        for dir_file in dir_files:
            if os.path.isfile(directory + "/" + dir + "/" + dir_file):
                files.append(directory + "/" + dir + "/" + dir_file)
                #print opts.directory + "/" + dir + "/" + dir_file

    return files

def main(args):

    # Optional Args
    parser = OptionParser(conflict_handler="resolve")
    # Just do one file
    parser.add_option("-f", "--file", dest="file")
    # Use a directory, create site based on a directory structure
    parser.add_option("-d", "--directory", dest="directory")
    # Output html to another dir, requires --directory
    parser.add_option("-o", "--output-directory", dest="output_directory")
    (opts, args) = parser.parse_args()

    if opts.directory and not opts.output_directory:
        print "ERROR: If option --directory is set, then --output-directoy must be as well"
        sys.exit(1)
    elif opts.directory and not os.path.exists(opts.directory):
        print "ERROR: Directory " + opts.directory + " does not exist"
        sys.exit(1)
    elif opts.directory:

        files = create_site(opts.directory)

        # Remove output_directory if it exists to make way for new output_dir
        if os.path.isdir(opts.output_directory):
            try:
                shutil.rmtree(opts.output_directory)
            except:
                print "ERROR: Could not remove " + opts.output_directory
                sys.exit(1)

        # Create the dir now
        try:
            os.mkdir(opts.output_directory)
        except:
            print "ERROR: Could not create " + opts.output_directory
            sys.exit(1)

        for input_textile_file in files:
            dir, file = os.path.split(input_textile_file)
            root, dir = os.path.split(dir)
            # Change the output file name to filename.html instead of filename.textile
            html_file_name, extension = os.path.splitext(file)
            html_file_name = html_file_name + ".html"
            output_html_file = opts.output_directory + "/" + dir + "/" + html_file_name
            
            # Create subdir
            try:
                os.mkdir(opts.output_directory + "/" + dir)
            except:
                print "ERROR: Could not create " + opts.output_directory + "/" + dir

            if os.path.isfile(input_textile_file):   
                f = open(input_textile_file)         
                html = textile.textile(f.read())
                textile_file = open(output_html_file, 'w')
                #textile_file.write(html)

                t = Template(file=TEMPLATE)
                t.body = html
                t.file_name = html_file_name
                textile_file.write(t.respond())

            print output_html_file
    else:
        if opts.file:
            f = open(opts.file, 'r')
        else:
            # Need to handle there being no input gracefully
            f = sys.stdin
        body = textile.textile(f.read())
        print body


if __name__ == '__main__':
    main(sys.argv)
