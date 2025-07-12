tickersMoexFut = (
    ('CRU5',True),
    ('MMU5',True),
    ('MXU5',True),
    ('GZU5',True),
    ('SRU5',True),
    ('RIU5',True),
    ('RMU5',True),
    ('SiU5',True),
    ('IMOEXF',True),
    ('CNYRUBF',True),
    ('NGN5',True),
    ('BRQ5',True),
    ('EDU5',True),
    ('EURRUBF',True),
)

tickersMoexStock = (
    ('SBER',False),
    ('GAZP',False),
    ('LKOH',False),
    ('ROSN',False),
    ('MTLR',False),
    ('MGNT',False),
    ('NVTK',False),
    ('GMKN',False),
    ('VTBR',False),
    ('TATN',False),
    ('TRNFP',False),
    ('AFKS',False),
    ('PIKK',False),
    ('MOEX',False),
    ('AFLT',False),
    ('CHMF',False),
    ('NLMK',False),
    ('SIBN',False),
    ('SNGSP',False),
    ('SNGS',False),
    ('ALRS',False),
    ('MAGN',False),
    ('MTSS',False),
    ('RUAL',False),
    ('FESH',False),
    ('IRAO',False),
    ('RTKM',False),
    ('UPRO',False),
    ('FEES',False),
    ('BANEP',False),
    ('TRMK',False),
    ('LSRG',False),
    ('CBOM',False),
    ('NMTP',False),
    ('HYDR',False),
    ('SELG',False),
    ('YDEX',False),
)

tickersMoexSpecial = []
for ticker in tickersMoexStock:
    item = (ticker[0]+'2',False)
    tickersMoexSpecial.append(item)
tickersMoexSpecial = tuple(tickersMoexSpecial)

tickersBitgetFut = (
    ("DOGEUSDT",True),
)