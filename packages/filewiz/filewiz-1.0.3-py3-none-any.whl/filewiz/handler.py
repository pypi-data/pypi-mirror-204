import sys
import os

from filewiz import move_file


DEFAULT_ROOT_DIR = "~/Dropbox/accounts/"

def main():
    source = sys.argv[1]
    if 'FILEWIZ_TARGET_ROOT' in os.environ:
        root_dir = os.environ['FILEWIZ_TARGET_ROOT']
    else:
        root_dir = DEFAULT_ROOT_DIR
    move_file(source, root_dir)

