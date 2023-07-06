def closest_resolution_multiple(original_resolution, target_resolution):
    """
    Given an original resolution, find the closest resolution to the target_resolution
    that is an integer multiple of the constraint resolution. Values must be under the target_resolution.
    """
    # if original_resolution['width'] > target_resolution['width'] or original_resolution['height'] > target_resolution['height']:
    constraint_width = target_resolution['width'] / original_resolution['width']
    constraint_height = target_resolution['height'] / original_resolution['height']
    constraint = min(constraint_width, constraint_height)
    constraint = int(constraint)
    if constraint == 0:
        constraint = 1
    return {
        'width': original_resolution['width'] * constraint,
        'height': original_resolution['height'] * constraint
    }