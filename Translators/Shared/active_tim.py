from pgquery import query_db

def active_tim(tim_type, tim_body):
    tim_id = tim_body["clientId"]
    # if TIM has an active TIM holding record that is current & info is the same as the current TIM record, then do not update
    active_tim_holding = query_db(f"SELECT * FROM active_tim_holding WHERE client_id LIKE '%{tim_id}%'")
    if len(active_tim_holding) > 0:
        active_tim_holding = active_tim_holding[0]
        return (active_tim_holding["direction"] == tim_body["direction"] and 
            f"{active_tim_holding['start_latitude']:.8f}" == f"{tim_body['geometry'][0]['latitude']:.8f}" and 
            f"{active_tim_holding['start_longitude']:.8f}" == f"{tim_body['geometry'][0]['longitude']:.8f}" and 
            f"{active_tim_holding['end_latitude']:.8f}" == f"{tim_body['geometry'][-1]['latitude']:.8f}" and 
            f"{active_tim_holding['end_longitude']:.8f}" == f"{tim_body['geometry'][-1]['longitude']:.8f}")

    # if TIM has an active TIM record that is current & info is the same as the current TIM record, then do not update
    active_tim = query_db(f"SELECT * FROM active_tim WHERE client_id LIKE '%{tim_id}%' AND tim_type_id = (SELECT tim_type_id FROM tim_type WHERE type = '{tim_type.upper()}') AND marked_for_deletion = false")
    if len(active_tim) > 0:
        active_tim = active_tim[0]
        return (active_tim["direction"] == tim_body["direction"] and
            f"{active_tim['start_latitude']:.8f}" == f"{tim_body['geometry'][0]['latitude']:.8f}" and
            f"{active_tim['start_longitude']:.8f}" == f"{tim_body['geometry'][0]['longitude']:.8f}" and
            f"{active_tim['end_latitude']:.8f}" == f"{tim_body['geometry'][-1]['latitude']:.8f}" and
            f"{active_tim['end_longitude']:.8f}" == f"{tim_body['geometry'][-1]['longitude']:.8f}")