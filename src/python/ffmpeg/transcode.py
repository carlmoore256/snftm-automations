import ffmpeg
import json
from video_info import probe_video_metadata
from filters import FilterInput
from defaults import DEFAULT_RENDER_PROFILE, DEFAULT_FORMAT, TRANSCODE_OUTPUT_ROOT
from files import output_path, delete_if_exists
import subprocess

def transcode_video(input_file, output_file=None, profile=DEFAULT_RENDER_PROFILE, filters=[], extension=DEFAULT_FORMAT):
    if output_file is None:
        output_file = output_path(input_file, TRANSCODE_OUTPUT_ROOT, 
                                  extension=extension, prefix='PADDED_')
    stream = ffmpeg.input(input_file)
    metadata = probe_video_metadata(input_file)
    filter_input = FilterInput(stream, metadata)
    for filter in filters:
        filter(filter_input)
    delete_if_exists(output_file)
    output = ffmpeg.output(filter_input.stream, output_file, pix_fmt='yuv420p', **profile)
    ffmpeg.run(output, capture_stdout=True)

# def loop_video(input_file, output_file=None, loops=10):
#     if output_file is None:
#         output_file = output_path(input_file, TRANSCODE_OUTPUT_ROOT, extension='.mp4', prefix='LOOPED_')
#     stream = ffmpeg.input(input_file)
#     delete_if_exists(output_file)
#     output = ffmpeg.output(stream, stream_loop=loops, filename=output_file)
#     ffmpeg.run(output, capture_stdout=True)

def loop_video(input_file, output_file=None, loops=10):
    if output_file is None:
        output_file = output_path(input_file, TRANSCODE_OUTPUT_ROOT, extension='.mp4', prefix='LOOPED_')
    delete_if_exists(output_file)
    cmd = f'ffmpeg -stream_loop {loops} -i {input_file} -c copy {output_file}'
    subprocess.run(cmd, shell=True)



if __name__ == '__main__':
    input_file = '/Users/kalianevan/Downloads/Monica Rizzolli_Fuchsia_2021.mp4'
    output_file = '../data/transcoding/output/Monica_Rizzolli_Fuchsia_2021_PADDED.mp4'
    info = probe_video_metadata(input_file)
    
    # transcode_video(input_file, output_file)
    # stream = stream.filter("pad", width=output_resolution['width'], height=output_resolution['height'], x=f"({output_resolution[0]}-{info['width']})/2", y=f"({output_resolution[1]}-{info['height']})/2", color="black")


        # stream = stream.filter("pad", width=output_resolution['width'], height=output_resolution['height'], x=f"({output_resolution[0]}-{info['width']})/2", y=f"({output_resolution[1]}-{info['height']})/2", color="black")
