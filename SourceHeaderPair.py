import os
import pathlib


class SourceHeaderPair:

    def __init__(self, src_path, h_path):
        self.source_filepath = src_path
        self.header_filepath = h_path

    def __str__(self):
        return 'Source file path: ' + self.source_filepath.as_posix() + \
               ' ; Header file path: ' + self.header_filepath.as_posix()


# takes  list of PurePath objects
def create_pairs(sources: list):
    pairs = []
    while sources:
        filepath = sources.pop()
        if filepath.name.endswith('.c'):
            name_to_find = filepath.name.replace('.c', '.h')
            header = next((x for x in sources if x.name == name_to_find), None)
            if header:
                sources.remove(header)
                pairs.append(SourceHeaderPair(filepath, header))
        else:
            name_to_find = filepath.name.replace('.h', '.c')
            source = next((x for x in sources if x.name == name_to_find), None)
            if source:
                sources.remove(source)
                pairs.append(SourceHeaderPair(source, filepath))
    return pairs


def get_paths(dirpath):
    sources = []
    for path, subdirs, files in os.walk(dirpath):
        for name in files:
            if name.endswith(('.c', '.h')):
                sources.append(pathlib.PurePath(path, name))
    return sources


import re

includes_pattern = r'#include <.+>'

def extract_inludes():
    with open('C:\\Users\\Admin\\Desktop\\test\\include\\two.h') as f:
        includes = re.findall(includes_pattern, f.read())
        return includes
