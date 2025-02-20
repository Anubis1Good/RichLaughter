import pandas as pd
import numpy as np

long_price,short_price = -1,-1
def get_price_reverse_rails(row):
    global long_price,short_price
    if row.name > 1:
        if row['rails'] == 1:
            long_price = row['middle']
        if row['rails'] == -1:
            short_price = row['middle']
    return np.array([long_price,short_price,short_price,long_price])

def get_price_reverse_dbb(row):
    long_price,short_price = -1,-1
    if row.name > 1:
        long_price = row['bbd']
        short_price = row['bbu']
    return np.array([long_price,short_price,short_price,long_price])

def get_price_dbb(row):
    long_price,short_price,close_price = -1,-1,-1
    if row.name > 1:
        long_price = row['bbd']
        short_price = row['bbu']
        close_price = row['sma']
    return np.array([long_price,short_price,close_price,close_price])

def get_price_reverse_bb(row):
    long_price,short_price = -1,-1
    if row.name > 1:
        long_price = row['bbu']
        short_price = row['bbd']
    return np.array([long_price,short_price,short_price,long_price])

def get_price_bb(row):
    long_price,short_price,close_price = -1,-1,-1
    if row.name > 1:
        long_price = row['bbu']
        short_price = row['bbd']
        close_price = row['sma']
    return np.array([long_price,short_price,close_price,close_price])

def get_price_bb_buff(row):
    long_price,short_price,close_price = -1,-1,-1
    if row.name > 1:
        long_price = row['top_buff']
        short_price = row['bottom_buff']
        close_price = row['sma']
    return np.array([long_price,short_price,close_price,close_price])

def get_price_ddc(row):
    long_price,short_price,close_price = -1,-1,-1
    if row.name > 1:
        long_price = row['middle_min']
        short_price = row['middle_max']
        close_price = row['avarege']
    return np.array([long_price,short_price,close_price,close_price])

def get_price_ddc_prev(row):
    long_price,short_price,close_price = -1,-1,-1
    if row.name > 1:
        long_price = row['prev_min']
        short_price = row['prev_max']
        close_price = row['avarege']
    return np.array([long_price,short_price,close_price,close_price])

def get_price_rddc(row):
    long_price,short_price = -1,-1
    if row.name > 1:
        long_price = row['middle_min']
        short_price = row['middle_max']
    return np.array([long_price,short_price,short_price,long_price])

def get_price_rddc_prev(row):
    long_price,short_price = -1,-1
    if row.name > 1:
        long_price = row['prev_min']
        short_price = row['prev_max']
    return np.array([long_price,short_price,short_price,long_price])

def get_price_rddc_prev_ba(row):
    long_price,short_price = -1,-1
    if row.name > 1:
        long_price = row['bottom_buff']
        short_price = row['top_buff']
    return np.array([long_price,short_price,short_price,long_price])

def get_price_bddc(row):
    long_price,short_price,close_price = -1,-1,-1
    if row.name > 1:
        long_price = row['middle_max']
        short_price = row['middle_min']
        close_price = row['avarege']
    return np.array([long_price,short_price,close_price,close_price])

def get_price_rbddc(row):
    long_price,short_price = -1,-1
    if row.name > 1:
        long_price = row['middle_max']
        short_price = row['middle_min']
    return np.array([long_price,short_price,short_price,long_price])


