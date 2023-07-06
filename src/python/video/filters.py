class FilterInput:
    def __init__(self, stream, metadata):
        self.stream = stream
        self.metadata = metadata

    def apply_filter(self, filter_name, **kwargs):
        self.stream = self.stream.filter(filter_name, **kwargs)


def pad_center_native(input : FilterInput, output_resolution, color='black'):
    input.apply_filter(
        "pad", 
        width=output_resolution['width'], 
        height=output_resolution['height'], 
        x=f"({output_resolution['width']}-{input.metadata['width']})/2", 
        y=f"({output_resolution['height']}-{input.metadata['height']})/2", 
        color=color
    )

def pad_center_and_resize(input : FilterInput, output_resolution, resize_resolution, color='black'):

    assert output_resolution['width'] >= resize_resolution['width']
    assert output_resolution['height'] >= resize_resolution['height']

    pad_x = (output_resolution['width'] - resize_resolution['width']) // 2
    pad_y = (output_resolution['height'] - resize_resolution['height']) // 2

    input.apply_filter("scale", 
                       width=resize_resolution['width'], 
                       height=resize_resolution['height'])
    
    input.apply_filter("pad", 
                        width=output_resolution['width'], 
                        height=output_resolution['height'], 
                        x=pad_x, y=pad_y, color=color)

def rotate(input : FilterInput, degrees):
    input.apply_filter("rotate", angle=f"{degrees}*(PI/180)")

def repeat_until_duration(input : FilterInput, duration):
    input.apply_filter("setpts", expr=f"PTS-STARTPTS, N/(TB*{input.metadata['fps']})")
    input.apply_filter("loop", size=f"{duration}*TB", start=0)
