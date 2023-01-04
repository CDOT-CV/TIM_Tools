expected_buffer_geometry_result = "POLYGON ((-100.0001 50, -100.00009951847267 50.000009801714036, -100.00009807852804 50.0000195090322, " \
    "-100.00009569403358 50.00002902846772, -100.00009238795325 50.00003826834324, -100.00008819212644 50.00004713967368, -100.00008314696123 " \
    "50.0000555570233, -100.00007730104534 50.000063439328414, -100.00007071067812 50.000070710678116, -100.00006343932841 50.00007730104534, " \
    "-100.0000555570233 50.00008314696123, -100.00004713967368 50.000088192126434, -100.00003826834323 50.00009238795325, -100.00002902846772 " \
    "50.000095694033575, -100.0000195090322 50.00009807852804, -100.00000980171403 50.000099518472666, -100 50.0001, -90 50.0001, " \
    "-89.99999019828597 50.000099518472666, -89.9999804909678 50.00009807852804, -89.99997097153228 50.000095694033575, -89.99996173165677 " \
    "50.00009238795325, -89.99995286032632 50.000088192126434, -89.9999444429767 50.00008314696123, -89.99993656067159 50.00007730104534, " \
    "-89.99992928932188 50.000070710678116, -89.99992269895466 50.000063439328414, -89.99991685303877 50.0000555570233, -89.99991180787356 " \
    "50.00004713967368, -89.99990761204675 50.00003826834324, -89.99990430596642 50.00002902846772, -89.99990192147196 50.0000195090322, " \
    "-89.99990048152733 50.000009801714036, -89.9999 50, -89.9999 40, -89.99990048152733 39.999990198285964, -89.99990192147196 39.9999804909678, " \
    "-89.99990430596642 39.99997097153228, -89.99990761204675 39.99996173165676, -89.99991180787356 39.99995286032632, -89.99991685303877 " \
    "39.9999444429767, -89.99992269895466 39.999936560671586, -89.99992928932188 39.999929289321884, -89.99993656067159 39.99992269895466, " \
    "-89.9999444429767 39.99991685303877, -89.99995286032632 39.999911807873566, -89.99996173165677 39.99990761204675, -89.99997097153228 " \
    "39.999904305966425, -89.9999804909678 39.99990192147196, -89.99999019828597 39.999900481527334, -90 39.9999, -90.00000980171403 39.999900481527334," \
    " -90.0000195090322 39.99990192147196, -90.00002902846772 39.999904305966425, -90.00003826834323 39.99990761204675, -90.00004713967368 " \
    "39.999911807873566, -90.0000555570233 39.99991685303877, -90.00006343932841 39.99992269895466, -90.00007071067812 39.999929289321884, " \
    "-90.00007730104534 39.999936560671586, -90.00008314696123 39.9999444429767, -90.00008819212644 39.99995286032632, -90.00009238795325 " \
    "39.99996173165676, -90.00009569403358 39.99997097153228, -90.00009807852804 39.9999804909678, -90.00009951847267 39.999990198285964, " \
    "-90.0001 40, -90.0001 49.9999, -99.9999 49.9999, -99.9999 40, -99.99990048152733 39.999990198285964, -99.99990192147196 39.9999804909678, " \
    "-99.99990430596642 39.99997097153228, -99.99990761204675 39.99996173165676, -99.99991180787356 39.99995286032632, -99.99991685303877 " \
    "39.9999444429767, -99.99992269895466 39.999936560671586, -99.99992928932188 39.999929289321884, -99.99993656067159 39.99992269895466, " \
    "-99.9999444429767 39.99991685303877, -99.99995286032632 39.999911807873566, -99.99996173165677 39.99990761204675, -99.99997097153228 " \
    "39.999904305966425, -99.9999804909678 39.99990192147196, -99.99999019828597 39.999900481527334, -100 39.9999, -100.00000980171403 " \
    "39.999900481527334, -100.0000195090322 39.99990192147196, -100.00002902846772 39.999904305966425, -100.00003826834323 39.99990761204675, " \
    "-100.00004713967368 39.999911807873566, -100.0000555570233 39.99991685303877, -100.00006343932841 39.99992269895466, -100.00007071067812 " \
    "39.999929289321884, -100.00007730104534 39.999936560671586, -100.00008314696123 39.9999444429767, -100.00008819212644 39.99995286032632, " \
    "-100.00009238795325 39.99996173165676, -100.00009569403358 39.99997097153228, -100.00009807852804 39.9999804909678, -100.00009951847267 " \
    "39.999990198285964, -100.0001 40, -100.0001 50))"


rsu_intersect_result = [{
    "latitude": 0,
    "longitude": 0,
    "rsuId": "rsu1",
    "route": "route1",
    "milepost": 0,
    "rsuTarget": "10.10.10.10",
    "rsuRetries": 3,
    "rsuTimeout": 5000,
    "rsuIndex": 2
}, {
    "latitude": 1,
    "longitude": 1,
    "rsuId": "rsu2",
    "route": "route2",
    "milepost": 0,
    "rsuTarget": "10.10.10.11",
    "rsuRetries": 3,
    "rsuTimeout": 5000,
    "rsuIndex": 2
}]

example_feature = {
    "id": "79808e1c-48b1-56c4-8f8d-609c7abdb710",
    "type": "Feature",
    "properties": {
          "core_details": {
              "event_type": "work-zone",
              "data_source_id": "01181511-8667-48b4-8bb3-85b0c894fa89",
              "road_names": ["I-25"],
              "direction": "southbound",
              "name": "OpenTMS-Event6377643515_southbound",
              "description": "Between Exit 150: North Academy Boulevard and Exit 149: Woodmen Road (1 mile north of Colorado Springs) from Mile Point 150.1 to Mile Point 150.1. Road construction. Width limit in effect. Width limit 11'0\". Starting November 11, 2022 at 7:00AM MDT until November 11, 2022 at about 5:30PM MDT.",
              "update_date": "2022-11-03T20:01:36Z"
          },
        "start_date": "2022-11-11T14:00:00Z",
        "end_date": "2022-11-12T00:30:00Z",
        "is_start_date_verified": False,
        "is_end_date_verified": False,
        "is_start_position_verified": False,
        "is_end_position_verified": False,
        "location_method": "channel-device-method",
        "vehicle_impact": "all-lanes-open",
        "lanes": [
              {"order": 1, "type": "general", "status": "open"},
              {"order": 2, "type": "general", "status": "open"},
              {"order": 3, "type": "general", "status": "open"},
              {"order": 4, "type": "general", "status": "open"}
          ],
        "beginning_cross_street": "Exit 150: North Academy Boulevard",
        "ending_cross_street": "Exit 149: Woodmen Road (1 mile north of Colorado Springs)",
        "types_of_work": [
              {"type_name": "roadway-creation", "is_architectural_change": True}
          ],
        "beginning_milepost": 150.1,
        "ending_milepost": 150.1
    },
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [-104.810743, 38.95061],
            [-104.810743, 38.95061]
        ]
    }
}

expected_snmp_settings = {
    "rsuid": "83",
    "msgid": 31,
    "mode": 1,
    "channel": 178,
    "interval": 2,
    "deliverystart": "2022-11-11T14:00:00Z",
    "deliverystop": "2022-11-12T00:30:00Z",
    "enable": 1,
    "status": 4
}

expected_rsu_request = {
    "rsus": rsu_intersect_result,
    "snmp": expected_snmp_settings
}