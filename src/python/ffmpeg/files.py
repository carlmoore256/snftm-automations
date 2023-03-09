import os

def output_path(input_file, output_root, extension, prefix=None):
    basename = os.path.basename(input_file)
    if prefix is not None:
        basename = prefix + basename
    basename = basename.replace(' ', '_')
    if not extension.startswith('.'):
        extension = '.' + extension
    output_file = os.path.join(output_root, basename.split('.')[0] + extension)
    return output_file

def delete_if_exists(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)