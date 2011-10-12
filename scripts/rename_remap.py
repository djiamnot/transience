#!/usr/bin/env python

import os
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--mapping-file", dest="mapping_file",
           help="File containing the name map.")
(options, args) = parser.parse_args()
print(options.mapping_file)
mapping_file = options.mapping_file
# A dict with keys being the old filenames and values being the new filenames
mapping = {}

# Read through the mapping file line-by-line and populate 'mapping'
with open(mapping_file) as map:
    for line in map:
        # Split the line along whitespace
        # Note: this fails if your filenames have whitespace
        old_name, new_name = line.split()
        mapping[old_name] = new_name

# List the files in the current directory
for filename in os.listdir('.'):
    root, extension = os.path.splitext(filename)
    os.rename(filename, ''.join(mapping[root] + extension))
