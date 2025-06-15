def split_segments(data, max_gap=0.3):
    """Split list of (time, altitude) into segments where time jumps are small."""
    segments = []
    current = [data[0]]
    for prev, curr in zip(data, data[1:]):
        if abs(curr[0] - prev[0]) > max_gap:
            segments.append(current)
            current = [curr]
        else:
            current.append(curr)
    if current:
        segments.append(current)
    return segments