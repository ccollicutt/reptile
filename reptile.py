#! /usr/bin/env python

import textile
import sys, os, shutil
from optparse import OptionParser
from Cheetah.Template import Template

VERSION = '0.1.1'
TEMPLATE = 'templates/reptile.tpl'

class Reptile:
    
    def __init__(self, template, in_directory, out_directory):
        self.in_directory = in_directory
        self.out_directory = out_directory
        self.template = template
        self.set_files(in_directory)
        self.create_out_directory()
        self.export_html()

    def set_files(self, directory):
        dirs = os.listdir(directory)
        files = []
        # The point is this mumbo-jumbo is to only go down one level into the main dir
        for dir in dirs:
            dir_files = os.listdir(os.path.join(directory, dir))
            for dir_file in dir_files:
                if os.path.isfile(os.path.join(directory, dir, dir_file)):
                    files.append(os.path.join(directory, dir, dir_file))

        self.files = files

    # FIXME
    def create_out_directory(self):
        if os.path.isdir(self.out_directory):
            try:
                shutil.rmtree(self.out_directory)
            except:
                print "ERROR: Could not remove " + self.out_directory
                sys.exit(1)
        
        try:
            os.mkdir(self.out_directory)
        except:
            print "ERROR: Could not create " + self.out_directory
            sys.exit(1)

    # FIXME
    def create_sub_directory(self, dir):
        try:
            os.mkdir(dir)
        except:
            print "ERROR: Could not create " + dir

    def export_html(self):

        for file in self.files:
            first_level_dir, file_name = os.path.split(file)
            root_level_dir, first_level_dir = os.path.split(first_level_dir)
            file_name, extension = os.path.splitext(file_name)
            file_name = file_name + '.html'
            output_html_file = os.path.join(self.out_directory, first_level_dir, file_name)

            self.create_sub_directory(os.path.join(self.out_directory, first_level_dir))

            if os.path.isfile(file):   
                f = open(file)         
                html = textile.textile(f.read())
                textile_file = open(output_html_file, 'w')
                self.template.body = html
                self.template.file_name = file_name
                textile_file.write(self.template.respond())
            
def main(args):

    try:
        # Make sure required args are set
        sys.argv[1]
        sys.argv[2]
    except:
        print "ERROR: Usage: " + str(sys.argv[0]) + " input_dir output_dir"
        sys.exit(1)
        
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]

    t = Template(file=TEMPLATE)
    r = Reptile(t, in_directory, out_directory)

if __name__ == '__main__':
    main(sys.argv)
