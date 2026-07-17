def check_close_by_delta(params:dict,min_profit:int,max_loss:int):
    ps = params['price_step']
    if params['pos'] == 1: #long
        if params['y_bask'] > 0:
            if params['p_max'] != -1:
                enter_price = params['p_max']
            elif params['l_min'] != -1:
                enter_price = params['l_min']
            else:
                return None
            delta_p = (enter_price - params['y_bask']) // ps
        else:
            return None
    elif params['pos'] == -1: #short
        if params['y_bbid'] > 0:
            if params['p_min'] != -1:
                enter_price = params['p_min']
            elif params['l_max'] != -1:
                enter_price = params['l_max']
            else:
                return None
            delta_p = (params['y_bbid'] - enter_price) // ps
        else:
            return None
    else:
        return None
    if max_loss is not None:
        if delta_p < -max_loss:
            return 'close_all_pw'
    if min_profit is not None:
        if delta_p > min_profit:
            return 'close_all_pw'