def dec_dms(degrees):
    sign = -1 if degrees < 0 else 1
    degrees_abs = abs(degrees)
    degrees_int = int(degrees_abs)
    minutes = int((degrees_abs - degrees_int) * 60)
    seconds = (degrees_abs - degrees_int - minutes / 60) * 3600
    return sign*degrees_int, minutes, seconds