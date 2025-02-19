from single_optimization import optimization
from strategies.test_strategies.universal import universal_test_strategy as ts

# from strategies.work_strategies.PTA import PTA2_BDDC,PTA2_BDDCde,PTA2_BDDCr,PTA2_DDCr,PTA2_DDCde
from strategies.work_strategies.PTA import PTA8_OBBY,PTA8_OBBY_VOR, PTA8_LOBBY,PTA8_OBBY_PF, PTA8_FOBBY,PTA8_OBBY_FREE,PTA8_OBBY_FREEr

test_folder = 'DataForTests\DataFromBitget'
params = [
    [3,4] + list(range(5,16,5)),
    (0.5,1,1.5)
]
group = (
    (PTA8_OBBY,params),
    (PTA8_OBBY_VOR,params),
    (PTA8_LOBBY,params),
    (PTA8_OBBY_PF,params),
    (PTA8_FOBBY,params),
    (PTA8_OBBY_FREE,params),
    (PTA8_OBBY_FREEr,params)
)
# params = [
#     (3,4,5,6,7,8,9,10,15,20,30,40,50,60,80,100)
# ]
# group = (
#     (PTA2_BDDC,params),
#     (PTA2_BDDCde,params),
#     (PTA2_BDDCr,params),
#     (PTA2_DDCr,params),
#     (PTA2_DDCde,params),
# )

for part in group:
    print(part[0])
    optimization(part[0],ts,part[1],test_folder)