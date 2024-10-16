def dec_dms(degrees):
    degrees_int = int(degrees)
    minutes = int((degrees - degrees_int) * 60)
    seconds = (degrees - degrees_int - minutes / 60) * 3600
    return degrees_int, minutes, seconds