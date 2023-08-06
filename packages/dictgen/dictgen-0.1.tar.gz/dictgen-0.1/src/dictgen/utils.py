def max_depth(d):
    """
    Helper function that returns the maximum depth of a dictionary. Used
    for testing the output of generate.

    :param d: Dictionary to analyse
    """
    if isinstance(d, dict):
        return 1 + (max(map(max_depth, d.values())) if d else 0)
    elif isinstance(d, list):
        return 1 + (max(map(max_depth, d)) if d else 0)
    return 0


def max_height(d):
    """
    Helper function that returns the maximum height of a dictionary. Used
    for testing the output of generate.

    :param d: Dictionary to analyse
    """
    current_height = 0
    found_max = []
    if isinstance(d, dict):
        for key in d.keys():
            if isinstance(d[key], dict) or isinstance(d[key], list):
                found_max.append(max_height(d[key]))
            current_height += 1
    elif isinstance(d, list):
        for item in d:
            if isinstance(item, dict) or isinstance(item, list):
                found_max.append(max_height(item))
            current_height += 1
    found_max.append(current_height)
    return max(found_max)
