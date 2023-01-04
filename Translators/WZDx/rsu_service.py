import logging
import pgquery as pgquery
import shapely.wkt


def get_rsus_intersecting_geometry(geometry):
    query = f"SELECT rsu_id, primary_route, milepost, ipv4_address,  ST_AsText(geography) point FROM rsus WHERE ST_Intersects('{str(geometry)}', geography)"
    try:
        result = pgquery.query_db(query)
    except Exception as e:
        logging.info(f'Error selecting intersected date')
        return  None
    return_value = [] if (len(result) > 0) else None
    logging.info(f'Found {len(result)} RSUs intersecting geometry')

    for row in result:
        pt = shapely.wkt.loads(row["point"])
        return_value.append({
            "latitude": pt.y,
            "longitude": pt.x,
            "rsuId": row["rsu_id"],
            "route": row["primary_route"],
            "milepost": row["milepost"],
            "rsuTarget": str(row["ipv4_address"]),
            "rsuRetries": 3,
            "rsuTimeout": 5000,
            "rsuIndex": 2
        })
    return return_value
