def ra_hms(degrees):
    hours = int(degrees // 15)
    minutes = int((degrees % 15) * 4)
    seconds = ((degrees % 15) * 4 - minutes) * 60
    return hours, minutes, seconds