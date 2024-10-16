coords = [
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
    [-100.00000000000000, 40.00000000000000],
]

anchor = {
    'longitude': -100.00000000000000,
    'latitude': 40.00000000000000
}

expected_dataframes = [
    {'startDateTime': '2022-02-13T16:00:00Z',
     'durationTime': 30,
     'sspTimRights': '1',
     'frameType': 'advisory',
     'msgId': 'some-id',
     'priority': '5',
     'sspLocationRights': '1',
     'regions': [
         {'name': 'I_some-road_IDENTIFIER',
          'anchorPosition':
          {'longitude': -100.0, 'latitude': 40.0},
             'laneWidth': '50',
             'directionality': '3',
             'closedPath': 'false',
             'description': 'path',
             'path': {
              'scale': 0,
              'nodes': [
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                  {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0}],
              'type': 'll'},
             'direction': '0000000100000000'},
         {
             'name': 'I_some-road_IDENTIFIER',
             'anchorPosition':
             {'longitude': -100.0, 'latitude': 40.0},
             'laneWidth': '50',
             'directionality': '3',
             'closedPath': 'false',
             'description': 'path',
             'path': {
                 'scale': 0,
                 'nodes': [
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0},
                     {'delta': 'node-LL', 'nodeLat': 0.0, 'nodeLong': 0.0}],
                 'type': 'll'},
             'direction': '0000000100000000'
         }
     ],
        'sspMsgTypes': '1',
     'sspMsgContent': '1',
     'content': 'workZone',
     'items': ['1025'],
     'url': 'null'}]
