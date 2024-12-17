from itis_codes import ItisCodes, ItisCodeExtraKeywords
from string import digits

def get_itis_codes(feature):
    itisCodes = []

    # need to iterate over entries & split to check for keywords
    for entry in feature["properties"]["currentConditions"]:
        itis_codes = entry["conditionDescription"].split(",")
        for code in itis_codes:
            code = code.translate({ord(k): None for k in digits}).replace("-", "").strip()
            if code == "forecast text included":
                continue
            for key in ItisCodes:
                searchKey = key.name.replace("_", " ").lower()
                if searchKey in code.lower() and key.value not in itisCodes:
                    itisCodes.append(key.value)
                elif searchKey in ItisCodeExtraKeywords:
                    if (
                        ItisCodeExtraKeywords[searchKey] in code.lower()
                        and key.value not in itisCodes
                    ):
                        itisCodes.append(key.value)

    return itisCodes

def get_geometry(geometry):
    annotated_geometry = []
    for coord in geometry:
        annotated_geometry.append({"latitude": coord[1], "longitude": coord[0]})
    return annotated_geometry
