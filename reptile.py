#! /usr/bin/env python

import textile
import sys, os, shutil, random
from optparse import OptionParser
from BeautifulSoup import BeautifulSoup
from Cheetah.Template import Template

VERSION = '0.1.1'
HOME = '/home/curtis/working/reptile'
TEMPLATE = HOME + '/templates/reptile.tpl'
# FIXME - bad name here
CSS = HOME + '/css'

class TextileFile:
    
    def __init__(self, path):
        self.path = path
        self.html = ''
        # Contains {somerandomnumber: notextile_text}
        self.notextiles = {}

        try:
            self.text = open(self.path).read()
        except:
            print "ERROR opening " + self.path
            sys.exit(1)

        self.create_html()

    def create_html(self):
        self.html = self.extract_notextile()
        #print self.html
        self.html = textile.textile(self.html)
        #print self.html
        self.html = self.replace_notextile()
        #print self.html

    def extract_notextile(self):
        soup = BeautifulSoup(self.text)
        # obv this isn't going to work because pres will
        # only be for one file and there will be many files...
        for idx, nt in enumerate(soup.findAll('notextile')):
            rand = str(random.random())
            # FIXME 
            nt.replaceWith('\n\n' + rand + '\n\n')
            self.notextiles[rand] = nt
            
        return soup.prettify()

    def replace_notextile(self):
        soup = BeautifulSoup(self.html)
        for k, v in self.notextiles.items():
            for nt in soup.findAll(text=k):
                nt.replaceWith(v)
               
        return soup.prettify()

class Reptile:
    
    def __init__(self, template, in_directory, out_directory):
        self.in_directory = in_directory
        self.out_directory = out_directory
        self.template = template
        self.css_dir = CSS
        # Will be a list of noTextile objects
        self.files = []
        self.set_files(in_directory)
        # FIXME - Should also set 1st level dirs too

    def run(self):
        self.create_out_directory()
        self.copy_css()
        self.export_html()
 
    def copy_css(self):
        try:
            shutil.copytree(self.css_dir, os.path.join(self.out_directory, 'css'))
        except:
            print "ERROR: Could not copy " + CSS + " to " + os.path.join(self.out_directory, 'css')
            sys.exit(1)
        
    # FIXME
    def set_files(self, directory):
        dirs = os.listdir(directory)
        # The point is this mumbo-jumbo is to only go down one level into the main dir
        for dir in dirs:
            dir_files = os.listdir(os.path.join(directory, dir))
            for dir_file in dir_files:
                if os.path.isfile(os.path.join(directory, dir, dir_file)):
                    f = open(os.path.join(directory, dir, dir_file))
                    # Create new textilefile
                    t = TextileFile(os.path.join(directory, dir, dir_file))
                    self.files.append(t)

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
            # FIXME Need to only try to make once
            #sys.exit(1)

    # FIXME
    def create_sub_directory(self, dir):
        try:
            os.mkdir(dir)
        except:
            print "ERROR: Could not create " + dir

    def export_html(self):
        for nt in self.files:
            first_level_dir, file_name = os.path.split(nt.path)
            root_level_dir, first_level_dir = os.path.split(first_level_dir)
            file_name, extension = os.path.splitext(file_name)
            file_name = file_name + '.html'
            output_html_file = os.path.join(self.out_directory, first_level_dir, file_name)
            self.create_sub_directory(os.path.join(self.out_directory, first_level_dir))
            if os.path.isfile(nt.path): 
                html_file = open(output_html_file, 'w')
                # Send the html as the "body" in the template
                self.template.body = nt.html
                self.template.file_name = file_name
                # Finally write the template to the html file
                html_file.write(self.template.respond())
 
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
    r.run()

if __name__ == '__main__':
    main(sys.argv)
