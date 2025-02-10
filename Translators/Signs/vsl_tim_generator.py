from itis_codes import ItisCodes

def get_itis_codes():
    return [ItisCodes.SPEED_LIMIT.value]

def get_geometry(geometry):
    if len(geometry) == 0:
        return []
    annotated_geometry = []
    # Check if the geometry is a single point
    if type(geometry[0]) == float:
        annotated_geometry.append({"latitude": geometry[1], "longitude": geometry[0]})
        return annotated_geometry
    
    for coord in geometry:
        annotated_geometry.append({"latitude": coord[1], "longitude": coord[0]})
    return annotated_geometry
