import mgrs 

# Calculate from latitude and longitude to mgrs
def calculateMGRS(lat, lon): 
    m = mgrs.MGRS() 
    c = m.toMGRS(lat,lon) 
    print("calculate MGRS is called")
    return c