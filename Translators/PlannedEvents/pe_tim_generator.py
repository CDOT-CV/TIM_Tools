from itis_codes import ItisCodes

def get_itis_codes():
    return [ItisCodes.CLOSED_FOR_SEASON.value]

def get_geometry(geometry):
    annotated_geometry = []
    for coord in geometry:
        annotated_geometry.append({"latitude": coord[1], "longitude": coord[0]})
    return annotated_geometry
