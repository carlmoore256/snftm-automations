import os
import json

def create_output_path(input_file, output_root, extension, prefix=None):
    basename = os.path.basename(input_file)
    if prefix is not None:
        basename = prefix + basename
    basename = basename.replace(' ', '_')
    if not extension.startswith('.'):
        extension = '.' + extension
    output_file = os.path.join(output_root, basename.split('.')[0] + extension)
    output_file = os.path.abspath(output_file)
    return output_file

def delete_if_exists(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)

def make_dir_if_not_exists(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
