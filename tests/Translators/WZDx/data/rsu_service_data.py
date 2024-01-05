import ipaddress

###################################### Single Result ##########################################
return_value_single_result = [
    {
        "rsu_id": 228,
        "primary_route": "primary",
        "milepost": 50,
        "ipv4_address": ipaddress.ip_address("10.10.10.10"),
        "point": "POINT(-105.20139 39.7028)"
    }
]

expected_rsu_data_single_result = [
    {
        "latitude": 39.7028,
        "longitude": -105.20139,
        "rsuId": 228,
        "route": "primary",
        "milepost": 50,
        "rsuTarget": "10.10.10.10",
        "rsuRetries": 3,
        "rsuTimeout": 5000,
        "rsuIndex": 2
    }
]


###################################### Multiple Results ##########################################
return_value_multiple_results = [
    {
        "rsu_id": 228,
        "primary_route": "primary",
        "milepost": 50,
        "ipv4_address": ipaddress.ip_address("10.10.10.10"),
        "point": "POINT(-105.20139 39.7028)"
    },
    {
        "rsu_id": 229,
        "primary_route": "primary2",
        "milepost": 51,
        "ipv4_address": ipaddress.ip_address("10.10.10.9"),
        "point": "POINT(-105.20140 39.7027)"
    }
]

expected_rsu_data_multiple_results = [
    {
        "latitude": 39.7028,
        "longitude": -105.20139,
        "rsuId": 228,
        "route": "primary",
        "milepost": 50,
        "rsuTarget": "10.10.10.10",
        "rsuRetries": 3,
        "rsuTimeout": 5000,
        "rsuIndex": 2
    },
    {
        "latitude": 39.7027,
        "longitude": -105.20140,
        "rsuId": 229,
        "route": "primary2",
        "milepost": 51,
        "rsuTarget": "10.10.10.9",
        "rsuRetries": 3,
        "rsuTimeout": 5000,
        "rsuIndex": 2
    }
]
