import pyproj


def get_direction_from_bearing(bearing):
    direction: int = 0

    if (bearing >= 0 and bearing <= 22.5):
        direction = 1
    elif (bearing > 22.5 and bearing <= 45):
        direction = 2
    elif (bearing > 45 and bearing <= 67.5):
        direction = 4
    elif (bearing > 67.5 and bearing <= 90):
        direction = 8
    elif (bearing > 90 and bearing <= 112.5):
        direction = 16
    elif (bearing > 112.5 and bearing <= 135):
        direction = 32
    elif (bearing > 135 and bearing <= 157.5):
        direction = 64
    elif (bearing > 157.5 and bearing <= 180):
        direction = 128
    elif (bearing > 180 and bearing <= 202.5):
        direction = 256
    elif (bearing > 202.5 and bearing <= 225):
        direction = 512
    elif (bearing > 225 and bearing <= 247.5):
        direction = 1024
    elif (bearing > 247.5 and bearing <= 270):
        direction = 2048
    elif (bearing > 270 and bearing <= 292.5):
        direction = 4096
    elif (bearing > 292.5 and bearing <= 315):
        direction = 8192
    elif (bearing > 315 and bearing <= 337.5):
        direction = 16384
    elif (bearing > 337.5 and bearing <= 360):
        direction = 32768

    return direction

def calculate_direction(coords, anchor):
    '''Creates a heading HeadingSlice from passed in coordinates and anchor point

    Parameters:
        coords (list): A list of coordinates
        anchor (dict): A coordinate representing the anchor point, or initial point to begin from

    Returns:
        headingSlice (dict): A HeadingSlice object'''
    # coords is array of [lon,lat]
    timDirection: int = 0
    startLat = float(anchor["latitude"])
    startLon = float(anchor["longitude"])
    geodesic = pyproj.Geod(ellps='WGS84')
    for i in range(len(coords)):
        lat = float(coords[i][1])
        lon = float(coords[i][0])

        fwd_azimuth, back_azimuth, distance = geodesic.inv(
            startLon, startLat, lon, lat)
        if (fwd_azimuth < 0):
            fwd_azimuth = 360 + fwd_azimuth
        timDirection |= get_direction_from_bearing(fwd_azimuth)
        # reset for next round
        startLat = lat
        startLon = lon

    # set direction based on bearings
    dirTest = str(bin(timDirection)[2:])
    # pad with zeros to 16 bits
    dirTest = dirTest.zfill(16)
    # reverse
    dirTest = dirTest[::-1]
    return dirTest