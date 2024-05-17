expected_buffer_geometry_result = "POLYGON ((-100.01449275362319 50, -100.01442296705322 50.00142053826565, " \
    "-100.01421427942613 50.002827395971245, -100.01386870051786 50.00420702430804, -100.0133895584422 50.00554613670094, " \
    "-100.01278146759925 50.00683183676559, -100.01205028423627 50.00805174250753, -100.01120305004874 50.00919410556759, " \
    "-100.01024792436502 50.010247924365025, -100.00919410556759 50.011203050048735, -100.00805174250753 50.01205028423627, " \
    "-100.0068318367656 50.012781467599254, -100.00554613670094 50.01338955844219, -100.00420702430803 50.01386870051786, " \
    "-100.00282739597125 50.014214279426135, -100.00142053826565 50.01442296705322, -100 50.01449275362319, -90 50.01449275362319, " \
    "-89.99857946173435 50.01442296705322, -89.99717260402875 50.014214279426135, -89.99579297569197 50.01386870051786, " \
    "-89.99445386329906 50.01338955844219, -89.9931681632344 50.012781467599254, -89.99194825749247 50.01205028423627, " \
    "-89.99080589443241 50.011203050048735, -89.98975207563498 50.010247924365025, -89.98879694995126 50.00919410556759, " \
    "-89.98794971576373 50.00805174250753, -89.98721853240075 50.00683183676559, -89.9866104415578 50.00554613670094, " \
    "-89.98613129948214 50.00420702430804, -89.98578572057387 50.002827395971245, -89.98557703294678 50.00142053826565, " \
    "-89.98550724637681 50, -89.98550724637681 40, -89.98557703294678 39.99857946173435, -89.98578572057387 39.997172604028755, " \
    "-89.98613129948214 39.99579297569196, -89.9866104415578 39.99445386329906, -89.98721853240075 39.99316816323441, " \
    "-89.98794971576373 39.99194825749247, -89.98879694995126 39.99080589443241, -89.98975207563498 39.989752075634975, " \
    "-89.99080589443241 39.988796949951265, -89.99194825749247 39.98794971576373, -89.9931681632344 39.987218532400746, " \
    "-89.99445386329906 39.98661044155781, -89.99579297569197 39.98613129948214, -89.99717260402875 39.985785720573865, " \
    "-89.99857946173435 39.98557703294678, -90 39.98550724637681, -90.00142053826565 39.98557703294678, -90.00282739597125 " \
    "39.985785720573865, -90.00420702430803 39.98613129948214, -90.00554613670094 39.98661044155781, -90.0068318367656 " \
    "39.987218532400746, -90.00805174250753 39.98794971576373, -90.00919410556759 39.988796949951265, -90.01024792436502 " \
    "39.989752075634975, -90.01120305004874 39.99080589443241, -90.01205028423627 39.99194825749247, -90.01278146759925 " \
    "39.99316816323441, -90.0133895584422 39.99445386329906, -90.01386870051786 39.99579297569196, -90.01421427942613 " \
    "39.997172604028755, -90.01442296705322 39.99857946173435, -90.01449275362319 40, -90.01449275362319 49.98550724637681, " \
    "-99.98550724637681 49.98550724637681, -99.98550724637681 40, -99.98557703294678 39.99857946173435, -99.98578572057387 " \
    "39.997172604028755, -99.98613129948214 39.99579297569196, -99.9866104415578 39.99445386329906, -99.98721853240075 " \
    "39.99316816323441, -99.98794971576373 39.99194825749247, -99.98879694995126 39.99080589443241, -99.98975207563498 " \
    "39.989752075634975, -99.99080589443241 39.988796949951265, -99.99194825749247 39.98794971576373, -99.9931681632344 " \
    "39.987218532400746, -99.99445386329906 39.98661044155781, -99.99579297569197 39.98613129948214, -99.99717260402875 " \
    "39.985785720573865, -99.99857946173435 39.98557703294678, -100 39.98550724637681, -100.00142053826565 39.98557703294678, " \
    "-100.00282739597125 39.985785720573865, -100.00420702430803 39.98613129948214, -100.00554613670094 39.98661044155781, " \
    "-100.0068318367656 39.987218532400746, -100.00805174250753 39.98794971576373, -100.00919410556759 39.988796949951265, " \
    "-100.01024792436502 39.989752075634975, -100.01120305004874 39.99080589443241, -100.01205028423627 39.99194825749247, " \
    "-100.01278146759925 39.99316816323441, -100.0133895584422 39.99445386329906, -100.01386870051786 39.99579297569196, " \
    "-100.01421427942613 39.997172604028755, -100.01442296705322 39.99857946173435, -100.01449275362319 40, -100.01449275362319 50))"


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
    "channel": 183,
    "interval": 1000,
    "deliverystart": "2022-11-11T14:00:00Z",
    "deliverystop": "2022-11-12T00:30:00Z",
    "enable": 1,
    "status": 4
}

expected_rsu_request = {
    "rsus": [{
    "latitude": 0,
    "longitude": 0,
    "rsuId": "rsu1",
    "route": "route1",
    "milepost": 0,
    "rsuTarget": "10.10.10.10",
    "rsuRetries": 3,
    "rsuTimeout": 5000,
    "rsuIndex": 2,
    "rsuUsername": "username",
    "rsuPassword": "password",
    "snmpProtocol": "NTCIP1218"
}, {
    "latitude": 1,
    "longitude": 1,
    "rsuId": "rsu2",
    "route": "route2",
    "milepost": 0,
    "rsuTarget": "10.10.10.11",
    "rsuRetries": 3,
    "rsuTimeout": 5000,
    "rsuIndex": 2,
    "rsuUsername": "username",
    "rsuPassword": "password",
    "snmpProtocol": "NTCIP1218",
}],
    "snmp": expected_snmp_settings
}

expected_snmp_info = [{
    "nickname": "nickname",
    "username": "username",
    "password": "password"
}]

expected_snmp_protocol = [{
    "version_code": "1218"
}]

check_rsu_online_no_result = [
    { "result": 0 },
    { "result": 0 },
    { "result": 0 },
    { "result": 0 },
    { "result": 0 },
]

check_rsu_online_result = [
    { "result": 1 },
    { "result": 1 },
    { "result": 1 },
    { "result": 1 },
    { "result": 1 }
]