import ffmpeg
import json
import os
from defaults import METADATA_ROOT
from files import create_output_path

def probe_video_metadata(input_file):
    probe = ffmpeg.probe(input_file)
    stream_meta = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    fps = float(stream_meta['avg_frame_rate'].split('/')[0]) / float(stream_meta['avg_frame_rate'].split('/')[1])
    stream_meta['fps'] = fps
    return stream_meta

def save_video_metadata(input_file, output_file=None):
    info = probe_video_metadata(input_file)
    if output_file is None:
        output_file = create_output_path(input_file, METADATA_ROOT, '.json', prefix='metadata_')
    with open(output_file, 'w') as f:
        json.dump(info, f)