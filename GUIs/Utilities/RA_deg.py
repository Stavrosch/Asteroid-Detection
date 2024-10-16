def RA_deg(ra):
    h,m,s = ra.split(' ')
    h,m,s = float(h), float(m), float(s)
    deg = (h*15) + (m/4) + (s/240)
    return deg

if __name__== "__main__" :
    ra='20 50 59.00'
    RA_deg(ra)
