def Decl_deg(dec):
    d,d2,d3 = dec.split(' ')
    d = float(d)
    d2 = float(d2)
    d3 = float(d3)
    if dec[0]=='-':
        deg = d - (d2/60) - (d3/3600)
    else:
        deg = d + (d2/60) + (d3/3600)
    return deg

if __name__== "__main__" :
    dec='-20 34 23.0'
    print(Decl_deg(dec))