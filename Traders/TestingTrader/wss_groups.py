from strategies.work_strategies.PTA import PTA4_WDDCr,PTA4_WDDCrE,PTA4_WDDCrVG,PTA4_WDVCr,PTA4_WLISICA,PTA8_WDOBBY_FREEr,PTA4_WDDCr2,PTA4_UNIVERSAL,PTA2_LISICA,PTA4_WDDC,PTA8_OBBY,PTA2_DDCrWork,PTA4_WDDCr2E,PTA8_DOBBY,PTA8_DOBBY_FREEr,PTA2_BDDCr_UNIVERSAL,PTA2_BDDC_FIX,PTA2_BVGFIX,PTA2_BBBU,PTA2_BBBUr
from strategies.work_strategies.PTAX import PTA10_WIZARD,PTA10_SORCERER,PTA11_KUSURUKEN,PTA12_SWDDCr,PTA14_RWDDCr,PTA15_NOVA,PTA15_KERRIGAN,PTA15_WIDOWMAKER,PTA15_TRACER

from strategies.work_strategies.STA_ml2 import STAML2_CHAOS,STAML2_TRADITION,STAML2_BALANCE,STAML2_NEWAVE
from strategies.work_strategies.STA_ca import STA_mini
from strategies.work_strategies.LTA import LTA_KROSH,LTA_OKROSHKA,LTA_PIN,LTA_APHOBO,LTA_NUSHA,LTA_KARYCH,LTA_KOPATYCH,LTA_OKROSHKA2,LTA_LOSYASH,LTA_SAVUNIA,LTA_EJIK,LTA_BARASH
from strategies.work_strategies.LTA2 import LTA2_MONSTER,LTA2_OVERLORD
from strategies.work_strategies.OGTA import OGTA4_DOG


wssMoexFut = [
    (LTA_PIN,(10,9,45,3)),
    
    (OGTA4_DOG,(25,30)),

    (STA_mini,(7,1)),
    (STA_mini,(7,0)),

    (STAML2_CHAOS,(60,2,30)),
    (STAML2_BALANCE,(60,2,30,30)),
    (STAML2_TRADITION,(5,5,0.5)),
    (STAML2_NEWAVE,(5,5,0.5,30)),

    (PTA2_LISICA,(7,2)), 

    (PTA2_BDDCr_UNIVERSAL,(7,True,True)), 
    (PTA2_BDDCr_UNIVERSAL,(7,True,False)), 
    (PTA2_BDDCr_UNIVERSAL,(7,False,True)), 

    (PTA2_BVGFIX,(7,1,1)), 
    (PTA2_BVGFIX,(7,1,0)), 
    (PTA2_BVGFIX,(7,0,1)), 

    (PTA2_BDDC_FIX,(20,1,1)), 
    (PTA2_BDDC_FIX,(20,1,0)), 
    (PTA2_BDDC_FIX,(20,0,1)), 

    (PTA2_BBBU,(14,1,1)), 
    (PTA2_BBBU,(14,1,0)), 
    (PTA2_BBBU,(14,0,1)), 

    (PTA2_BBBUr,(7,1,1)), 
    (PTA2_BBBUr,(7,1,0)), 
    (PTA2_BBBUr,(7,0,1)), 

    (PTA4_WDDCr,(30,30)), #C
    (PTA4_WDDCr,(10,20)), #C
    (PTA4_WDDCr,(11,30)), #C
    (PTA4_WDDCr,(6,30)), #C
    (PTA4_WDDCrE,(11,30)), #C
    (PTA4_WDDCrE,(10,20)), #C
    (PTA4_WDDCrE,(6,30)), #C
    (PTA4_WDDCrVG,(11,30)),

    (PTA4_WDVCr,(11,30)),
    (PTA4_WLISICA,(7,2,30)),

    (PTA4_UNIVERSAL,(7,7,30,30,"DC",'rsi',True,True)),
    (PTA4_UNIVERSAL,(7,7,60,20,"DC",'rsi',True,False)),
    (PTA4_UNIVERSAL,(7,7,20,60,"DC",'rsi',False,True)),

    (PTA8_WDOBBY_FREEr,(11,0.5,30)),
    (PTA8_WDOBBY_FREEr,(6,0.5,30)),

    (PTA10_WIZARD,(50,55,12,10,30)),
    (PTA10_WIZARD,(20,55,12,25,20)),
    (PTA10_WIZARD,(30,55,3,15,20)),
    (PTA10_SORCERER,(80,20,15,30,5,20)),

    (PTA11_KUSURUKEN,(50,6,5,20,'c')), #A
    (PTA11_KUSURUKEN,(50,3,20,10,'c')), #F
    (PTA11_KUSURUKEN,(70,3,10,40,'hl')), #F

    (PTA12_SWDDCr,(10,20,1,20,15)), #A
    (PTA12_SWDDCr,(10,40,0.25,5,5)), #F
    (PTA12_SWDDCr,(15,30,0.25,5,20)), #A

    (PTA14_RWDDCr,(15,30,35,45)), #F
    (PTA14_RWDDCr,(10,40,30,40)), #F
   
    (PTA15_KERRIGAN,(5,)), #A
    (PTA15_NOVA,(5,)), #A
    (PTA15_NOVA,(15,)), #A
    (PTA15_WIDOWMAKER,(5,30)), 

    (PTA15_TRACER,(10,0)), 
    (PTA15_TRACER,(10,1)), 
    (PTA15_TRACER,(10,-1)), 
]

wssMoexStocks = [
    (LTA_PIN,(10,9,45,3)),

    (OGTA4_DOG,(25,30)),

    (STA_mini,(7,1)),
    (STA_mini,(7,0)),

    (STAML2_CHAOS,(60,2,30)),
    (STAML2_BALANCE,(60,2,200,30)),
    (STAML2_BALANCE,(60,2,30,30)),

    (PTA2_LISICA,(7,2)), 
    (PTA2_LISICA,(14,2)), 

    (PTA2_BDDCr_UNIVERSAL,(7,True,True)), 
    (PTA2_BDDCr_UNIVERSAL,(7,True,False)), 
    (PTA2_BDDCr_UNIVERSAL,(7,False,True)), 

    (PTA2_BVGFIX,(7,1,1)), 
    (PTA2_BVGFIX,(7,1,0)), 
    (PTA2_BVGFIX,(7,0,1)), 

    (PTA2_BDDC_FIX,(20,1,1)), 
    (PTA2_BDDC_FIX,(20,1,0)), 
    (PTA2_BDDC_FIX,(20,0,1)), 

    (PTA2_BBBU,(14,1,1)), 
    (PTA2_BBBU,(14,1,0)), 
    (PTA2_BBBU,(14,0,1)), 

    (PTA2_BBBUr,(7,1,1)), 
    (PTA2_BBBUr,(7,1,0)), 
    (PTA2_BBBUr,(7,0,1)), 

    (PTA4_WLISICA,(7,2,30)),
    (PTA4_WDDCrE,(11,30)), #C
    (PTA4_WDVCr,(11,30)),
    (PTA4_WDDCrE,(6,30)), #C
    (PTA4_WDDCrVG,(11,30)),
    (PTA4_WDDCrE,(10,20)), #C
    (PTA4_WDDCr,(6,20)), #C
    (PTA4_WDDCr,(11,30)), #C
    (PTA4_WDDCr,(10,20)), #C
    (PTA4_WDDCr,(30,30)), #C

    (PTA4_UNIVERSAL,(7,7,30,30,"DC",'rsi',True,True)),
    (PTA4_UNIVERSAL,(7,7,50,20,"DC",'rsi',True,False)),
    (PTA4_UNIVERSAL,(7,7,20,50,"DC",'rsi',False,True)),

    (PTA8_WDOBBY_FREEr,(6,0.5,30)),
    (PTA8_WDOBBY_FREEr,(11,0.5,30)),

    (PTA10_WIZARD,(50,55,12,10,30)),
    (PTA10_WIZARD,(30,55,3,15,20)),
    (PTA10_WIZARD,(20,55,12,25,20)),
    (PTA10_SORCERER,(80,20,15,30,5,20)),

    (PTA11_KUSURUKEN,(70,15,35,10,'c')), #A
    (PTA11_KUSURUKEN,(50,3,20,10,'c')), #F
    (PTA11_KUSURUKEN,(70,3,10,40,'hl')), #F

    (PTA12_SWDDCr,(15,30,0.25,5,20)), #A
    (PTA12_SWDDCr,(10,40,0.25,5,5)), #F
    (PTA12_SWDDCr,(10,20,1,20,15)), #A

    (PTA14_RWDDCr,(15,30,35,45)), #F
    (PTA14_RWDDCr,(10,40,30,40)), #F
    
    (PTA15_WIDOWMAKER,(5,30)), 
    (PTA15_NOVA,(5,)), #A
    (PTA15_KERRIGAN,(5,)), #A
    (PTA15_WIDOWMAKER,(10,20)), 

    (PTA15_TRACER,(10,0)), 
    (PTA15_TRACER,(10,1)), 
    (PTA15_TRACER,(10,-1)), 

]

wssBitgetFut1 = [

    (OGTA4_DOG,(45,15)),
    (OGTA4_DOG,(35,20)),

    (STA_mini,(7,1)),
    (STA_mini,(7,0)),

    (STAML2_CHAOS,(60,2,200)),
    (STAML2_BALANCE,(60,2,200,30)),
    (STAML2_BALANCE,(60,2,60,30)),

    (PTA2_BDDCr_UNIVERSAL,(7,True,True)), 
    (PTA2_BDDCr_UNIVERSAL,(7,True,False)), 
    (PTA2_BDDCr_UNIVERSAL,(7,False,True)), 

    (PTA2_BVGFIX,(7,1,1)), 
    (PTA2_BVGFIX,(7,1,0)), 
    (PTA2_BVGFIX,(7,0,1)), 

    (PTA2_BDDC_FIX,(20,1,1)), 
    (PTA2_BDDC_FIX,(20,1,0)), 
    (PTA2_BDDC_FIX,(20,0,1)), 

    (PTA2_BBBU,(14,1,1)), 
    (PTA2_BBBU,(14,1,0)), 
    (PTA2_BBBU,(14,0,1)), 

    (PTA2_BBBUr,(7,1,1)), 
    (PTA2_BBBUr,(7,1,0)), 
    (PTA2_BBBUr,(7,0,1)), 

    (PTA4_WDDCr,(21,20)), #C
    (PTA4_WDDC,(30,20)), #C
    (PTA4_UNIVERSAL,(7,7,30,30,"DC",'rsi',True,True)),
    (PTA4_UNIVERSAL,(7,7,50,20,"DC",'rsi',True,False)),
    (PTA4_UNIVERSAL,(7,7,20,50,"DC",'rsi',False,True)),

    (PTA11_KUSURUKEN,(90,3,25,30,'hl')),#S

    (PTA15_TRACER,(10,0)), 
    (PTA15_TRACER,(10,1)), 
    (PTA15_TRACER,(10,-1)), 
]

wssBitgetFut5 = [
    (LTA_KARYCH,(30,35)),
    (LTA_OKROSHKA2,(20,65)),

    (STA_mini,(7,1)),
    (STA_mini,(7,0)),

    (STAML2_BALANCE,(60,2,200,30)),
    (STAML2_BALANCE,(60,2,60,30)),

    (PTA2_BDDCr_UNIVERSAL,(7,True,True)), 
    (PTA2_BDDCr_UNIVERSAL,(7,True,False)), 
    (PTA2_BDDCr_UNIVERSAL,(7,False,True)), 

    (PTA2_BVGFIX,(7,1,1)), 
    (PTA2_BVGFIX,(7,1,0)), 
    (PTA2_BVGFIX,(7,0,1)), 

    (PTA2_BDDC_FIX,(20,1,1)), 
    (PTA2_BDDC_FIX,(20,1,0)), 
    (PTA2_BDDC_FIX,(20,0,1)), 

    (PTA2_BBBU,(14,1,1)), 
    (PTA2_BBBU,(14,1,0)), 
    (PTA2_BBBU,(14,0,1)), 

    (PTA2_BBBUr,(7,1,1)), 
    (PTA2_BBBUr,(7,1,0)), 
    (PTA2_BBBUr,(7,0,1)), 

    (PTA4_WDDCr,(21,30)), #C
    (PTA4_WDDCr2,(20,35)), #C
    (PTA4_UNIVERSAL,(7,7,30,30,"DC",'rsi',True,True)),
    (PTA4_UNIVERSAL,(7,7,50,20,"DC",'rsi',True,False)),
    (PTA4_UNIVERSAL,(7,7,20,50,"DC",'rsi',False,True)),

    (PTA11_KUSURUKEN,(70,9,5,10,'c')), #S
    (PTA11_KUSURUKEN,(50,9,10,10,'c')), #S
    
    (PTA12_SWDDCr,(5,10,0.25,10,5)), #A

    (PTA14_RWDDCr,(20,30,10,10)), #A
    (PTA14_RWDDCr,(5,10,20,25)), #A

    (PTA15_NOVA,(95,)), #A
    (PTA15_KERRIGAN,(95,)), #A
    (PTA15_TRACER,(10,0)), 
    (PTA15_TRACER,(10,1)), 
    (PTA15_TRACER,(10,-1)), 

]
wssBitgetFut15 = [
    (LTA_KARYCH,(5,15)),
    (LTA_BARASH,(25,45)),
    (LTA_SAVUNIA,(65,35)),

    (OGTA4_DOG,(15,25)),

    (STA_mini,(7,1)),
    (STA_mini,(7,0)),

    (STAML2_BALANCE,(60,2,200,30)),
    (STAML2_TRADITION,(5,5,0.5)),
    (STAML2_TRADITION,(10,5,0.5)),

    (PTA2_LISICA,(7,1)),
    (PTA2_LISICA,(14,2)),
    (PTA2_DDCrWork,(5,)),
    (PTA2_BDDCr_UNIVERSAL,(7,True,True)), 
    (PTA2_BDDCr_UNIVERSAL,(7,True,False)), 
    (PTA2_BDDCr_UNIVERSAL,(7,False,True)), 
    (PTA2_BVGFIX,(7,1,1)), 
    (PTA2_BVGFIX,(7,1,0)), 
    (PTA2_BVGFIX,(7,0,1)), 

    (PTA2_BDDC_FIX,(20,1,1)), 
    (PTA2_BDDC_FIX,(20,1,0)), 
    (PTA2_BDDC_FIX,(20,0,1)), 

    (PTA2_BBBU,(14,1,1)), 
    (PTA2_BBBU,(14,1,0)), 
    (PTA2_BBBU,(14,0,1)), 

    (PTA2_BBBUr,(7,1,1)), 
    (PTA2_BBBUr,(7,1,0)), 
    (PTA2_BBBUr,(7,0,1)), 

    (PTA4_WDDCr2,(5,15)), #C
    (PTA4_WLISICA,(14,2,20)),
    (PTA4_WDDCr,(3,20)), #C
    (PTA4_UNIVERSAL,(7,7,30,30,"DC",'rsi',True,True)),
    (PTA4_UNIVERSAL,(7,7,50,20,"DC",'rsi',True,False)),
    (PTA4_UNIVERSAL,(7,7,20,50,"DC",'rsi',False,True)),

    (PTA8_OBBY,(11,0.5)), #S
    
    (PTA11_KUSURUKEN,(90,15,5,10,'c')), #S

    (PTA12_SWDDCr,(20,40,0.25,15,5)), #A
    (PTA12_SWDDCr,(5,10,0.25,10,20)), #A

    (PTA14_RWDDCr,(15,40,15,15)), #A

    (PTA15_NOVA,(45,)), #A
    (PTA15_NOVA,(30,)), #A
    (PTA15_TRACER,(10,0)), 
    (PTA15_TRACER,(10,1)), 
    (PTA15_TRACER,(10,-1)), 

]
wssBitgetFut30 = [
    (STA_mini,(7,1)),
    (STA_mini,(7,0)),

    (STAML2_CHAOS,(60,2,200)),
    (STAML2_BALANCE,(60,2,200,30)),

    (STAML2_NEWAVE,(5,5,0.5,30)),

    (PTA2_BDDCr_UNIVERSAL,(7,True,True)), 
    (PTA2_BDDCr_UNIVERSAL,(7,True,False)), 
    (PTA2_BDDCr_UNIVERSAL,(7,False,True)), 
    (PTA2_BVGFIX,(7,1,1)), 
    (PTA2_BVGFIX,(7,1,0)), 
    (PTA2_BVGFIX,(7,0,1)), 

    (PTA2_BDDC_FIX,(20,1,1)), 
    (PTA2_BDDC_FIX,(20,1,0)), 
    (PTA2_BDDC_FIX,(20,0,1)), 

    (PTA2_BBBU,(14,1,1)), 
    (PTA2_BBBU,(14,1,0)), 
    (PTA2_BBBU,(14,0,1)), 

    (PTA2_BBBUr,(7,1,1)), 
    (PTA2_BBBUr,(7,1,0)), 
    (PTA2_BBBUr,(7,0,1)), 
    (PTA4_UNIVERSAL,(7,7,30,30,"DC",'rsi',True,True)),
    (PTA4_UNIVERSAL,(7,7,50,20,"DC",'rsi',True,False)),
    (PTA4_UNIVERSAL,(7,7,20,50,"DC",'rsi',False,True)),

    (PTA8_DOBBY,(8,2)),
    (PTA8_DOBBY_FREEr,(4,0.5)),

    (PTA10_SORCERER,(40,30,9,30,20,10)),

    (PTA11_KUSURUKEN,(30,9,5,10,'hl')), #S
    (PTA11_KUSURUKEN,(90,15,5,10,'c')), #S
    
    (PTA12_SWDDCr,(5,10,0.25,10,20)), #A
    
    (PTA15_WIDOWMAKER,(10,40)), #A
    (PTA15_TRACER,(10,0)), 
    (PTA15_TRACER,(10,1)), 
    (PTA15_TRACER,(10,-1)), 

]
wssBitgetFut60 = (
    (STA_mini,(7,1)),
    (STA_mini,(7,0)),
    (PTA2_BDDCr_UNIVERSAL,(7,True,True)), 
    (PTA2_BDDCr_UNIVERSAL,(7,True,False)), 
    (PTA2_BDDCr_UNIVERSAL,(7,False,True)), 
    (PTA2_BVGFIX,(7,1,1)), 
    (PTA2_BVGFIX,(7,1,0)), 
    (PTA2_BVGFIX,(7,0,1)), 

    (PTA2_BDDC_FIX,(20,1,1)), 
    (PTA2_BDDC_FIX,(20,1,0)), 
    (PTA2_BDDC_FIX,(20,0,1)), 

    (PTA2_BBBU,(14,1,1)), 
    (PTA2_BBBU,(14,1,0)), 
    (PTA2_BBBU,(14,0,1)), 

    (PTA2_BBBUr,(7,1,1)), 
    (PTA2_BBBUr,(7,1,0)), 
    (PTA2_BBBUr,(7,0,1)), 
    (PTA4_UNIVERSAL,(7,7,30,30,"DC",'rsi',True,True)),
    (PTA4_UNIVERSAL,(7,7,50,20,"DC",'rsi',True,False)),
    (PTA4_UNIVERSAL,(7,7,20,50,"DC",'rsi',False,True)),

    (PTA15_KERRIGAN,(5,)), #A
    (PTA15_WIDOWMAKER,(5,40)), #A
    (PTA15_NOVA,(5,)), #A
    (PTA15_NOVA,(45,)), #A
    (PTA15_TRACER,(10,0)), 
    (PTA15_TRACER,(10,1)), 
    (PTA15_TRACER,(10,-1)), 
)

