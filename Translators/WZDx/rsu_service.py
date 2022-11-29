import logging
import pgquery
from shapely.geometry import Point
import shapely.wkt


def getRsusIntersectingGeometry(geometry):
    query = f"SELECT rsu_id, primary_route, milepost, ipv4_address,  ST_AsText(geography) point FROM rsus WHERE ST_Intersects('{str(geometry)}', geography)"
    try:
        result = pgquery.query_db(query)
    except Exception as e:
        logging.info(f'Error selecting intersected date')
        return  None
    return_value = [] if (len(result) > 0) else None

    for row in result:
        pt = shapely.wkt.loads(row["point"])
        return_value.append({
            "latitude": pt.y,
            "longitude": pt.x,
            "rsuId": row["rsu_id"],
            "route": row["primary_route"],
            "milepost": row["milepost"],
            "rsuTarget": row["ipv4_address"],
            "rsuRetries": 3,
            "rsuTimeout": 5000,
            "rsuIndex": 2
        })
    return return_value
