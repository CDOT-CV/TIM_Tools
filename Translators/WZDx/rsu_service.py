import logging
import pgquery as pgquery
import shapely.wkt

rsu_index_dict = {} # Used to store the current index of each RSU

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
            "rsuIndex": get_rsu_index(str(row["ipv4_address"]))
        })
    return return_value


def get_rsu_index(rsu_target):
    global rsu_index_dict
    if rsu_target not in rsu_index_dict:
        rsu_index_dict[rsu_target] = 1
    else:
        rsu_index_dict[rsu_target] += 1
    return rsu_index_dict[rsu_target]