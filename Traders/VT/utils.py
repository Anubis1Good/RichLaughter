from datetime import datetime
import json

def configuration_traiders(filename:str):
    fields = []
    with open(filename,'r') as f:
        lines = f.readlines()
        for line in lines:
            field = tuple(map(int,line.split(',')))
            fields.append(field)
    return fields

def configuration_traiders_grid(filename:str):
    fields = []
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        raw_glass_field = data['raw_glass_field_xyxy']
        raw_pos_field = data['raw_pos_filed_xyxy']
        raw_chart_field = data['raw_chart_field_xyxy']
        width_vt = (raw_glass_field[2]-raw_glass_field[0])//data['amount_vt']
        height_chart = raw_chart_field[3]-raw_chart_field[1]
        offset_glass = data['x_first_glass'] - raw_glass_field[0]
        part_pos = width_vt//3
        for i in range(data['amount_vt']):
            glass_field = (raw_glass_field[0]+offset_glass+width_vt*i,
                           raw_glass_field[1],
                           raw_glass_field[0]+width_vt*(i+1),
                           raw_glass_field[3])
            fields.append(glass_field) #0
            if data['direction_chart_grid'] == 'row':
                chart_field = (raw_chart_field[0]+width_vt*i,
                         raw_chart_field[1],
                         raw_chart_field[0]+width_vt*(i+1),
                         raw_chart_field[3])
            else: #column
                chart_field = (raw_chart_field[0],
                               raw_chart_field[1]+height_chart*i,
                               raw_chart_field[2],
                               raw_chart_field[1]+height_chart*(i+1))
            fields.append(chart_field) #1
            pos_field = (raw_pos_field[0]+width_vt*i+part_pos,
                         raw_pos_field[1],
                         raw_pos_field[0]+width_vt*(i+1)-part_pos,
                         raw_pos_field[3])
            fields.append(pos_field) #2
            tape_field = (raw_glass_field[0]+data['xx_first_tape'][0]+width_vt*i,
                           raw_glass_field[1],
                           raw_glass_field[0]+data['xx_first_tape'][1]+width_vt*i,
                           raw_glass_field[3])
            fields.append(tape_field) #3
            cluster_field = (raw_glass_field[0]+data['xx_first_cluster'][0]+width_vt*i,
                           raw_glass_field[1],
                           raw_glass_field[0]+data['xx_first_cluster'][1]+width_vt*i,
                           raw_glass_field[3])
            fields.append(cluster_field) #4
            

    return fields

def only_close(action,hour,minute):
    now = datetime.now()
    chour = now.hour
    cminute = now.minute
    end_minute = minute + 15
    if hour == chour:
        if end_minute > cminute > minute:
            if action == 'long':
                return 'close_short'
            if action == 'short':
                return 'close_long'
        if end_minute < cminute:
            return 'close_all'
    return action