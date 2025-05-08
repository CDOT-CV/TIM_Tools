from Translators.Shared.itis_codes import ItisCodes

def get_itis_codes():
    return [ItisCodes.SPEED_LIMIT.value]

def get_geometry(geometry):
    if len(geometry) == 0:
        return []
    annotated_geometry = []
    coords = geometry['coordinates']
    # Check if the geometry is a single point
    if geometry['type'] == 'Point':
        annotated_geometry.append({"latitude": coords[1], "longitude": coords[0]})
        return annotated_geometry
    
    for coord in coords:
        annotated_geometry.append({"latitude": coord[1], "longitude": coord[0]})
    return annotated_geometry
