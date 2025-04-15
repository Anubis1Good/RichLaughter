from strategies.work_strategies.PTA import PTA4_WDDCr,PTA4_WDDCrE,PTA4_WDDCrVG,PTA4_WDVCr,PTA4_WLISICA,PTA8_WDOBBY_FREEr,PTA4_UNIVERSAL,PTA2_LISICA,PTA4_WDDC,PTA8_OBBY,PTA2_DDCrWork,PTA2_BDDCr_UNIVERSAL,PTA2_BDDC_FIX,PTA2_BVGFIX,PTA2_BBBU,PTA2_BBBUr,PTA2_DDCrVG,PTA2_DVCr,PTA2_VOLCHARA,PTA8_LOBSTER
from strategies.work_strategies.PTAX import PTA10_WIZARD,PTA10_SORCERER,PTA11_KUSURUKEN,PTA12_SWDDCr,PTA14_RWDDCr,PTA15_NOVA,PTA15_KERRIGAN,PTA15_WIDOWMAKER,PTA15_TRACER,PTA10_MAGIC,PTA13_DWDDCr

from strategies.work_strategies.STA_ml2 import STAML2_CHAOS,STAML2_BALANCE,STAML2_NEWAVE,STAML2_SID
from strategies.work_strategies.STA_ca import STA_mini
from strategies.work_strategies.LTA import LTA_OKROSHKA,LTA_PIN,LTA_KARYCH,LTA_LAKSA,LTA_LAKSAe
# from strategies.work_strategies.LTA2 import LTA2_MONSTER,LTA2_OVERLORD
from strategies.work_strategies.OGTA import OGTA4_DOG


wssMoexFut = [
    (LTA_LAKSA,(50,10)),
    (LTA_LAKSAe,(50,10)),
    (LTA_OKROSHKA,(10,80)),
    (LTA_PIN,(10,6,40,5)),

    (OGTA4_DOG,(10,40)),

    (STA_mini,(7,1)),
    (STA_mini,(7,0)),

    (STAML2_CHAOS,(60,2,30)),
    # (STAML2_BALANCE,(60,2,30,30)),
    (STAML2_NEWAVE,(5,5,0.5,30)),
    # (STAML2_SID,(200,10,5,30)),

    (PTA2_DDCrWork,(5,)),
    (PTA2_LISICA,(7,2)), 
    (PTA2_LISICA,(10,1)), 
    (PTA2_VOLCHARA,(10,1)), 
    (PTA2_DDCrVG,(10,)), 
    (PTA2_DVCr,(20,)), 

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
    (PTA8_LOBSTER,(20,1)),
    (PTA8_LOBSTER,(40,2)),

    (PTA10_MAGIC,(40,80,3)),
    (PTA10_WIZARD,(50,55,12,10,30)),
    (PTA10_WIZARD,(20,55,12,25,20)),
    (PTA10_WIZARD,(30,55,3,15,20)),
    (PTA10_WIZARD,(20,80,3,30,20)),
    (PTA10_SORCERER,(80,20,15,30,5,20)),
    (PTA10_SORCERER,(90,10,3,30,15,20)),

    (PTA11_KUSURUKEN,(50,6,5,20,'c')), #A
    (PTA11_KUSURUKEN,(50,3,20,10,'c')), #F
    (PTA11_KUSURUKEN,(70,3,10,40,'hl')), #F
    (PTA11_KUSURUKEN,(10,9,35,30,'c')), #A
    (PTA11_KUSURUKEN,(10,12,10,40,'hl')), #A

    (PTA12_SWDDCr,(10,40,0.25,5,5)), #F
    (PTA12_SWDDCr,(15,30,0.25,5,20)), #A
    (PTA12_SWDDCr,(10,30,0.5,5,15)), #A

    (PTA13_DWDDCr,(70,40,10)), #A

    (PTA14_RWDDCr,(15,30,35,45)), #F
    (PTA14_RWDDCr,(10,30,90,80)), #F

   
    (PTA15_KERRIGAN,(5,)), #A
    (PTA15_NOVA,(5,)), #A
    (PTA15_WIDOWMAKER,(5,30)), 

    (PTA15_TRACER,(10,0)), 
    (PTA15_TRACER,(10,1)), 
    (PTA15_TRACER,(10,-1)), 
]

wssMoexStocks = [
    (LTA_LAKSA,(30,10)),
    (LTA_LAKSA,(100,10)),
    (LTA_LAKSAe,(30,10)),
    (LTA_OKROSHKA,(10,10)),
    (LTA_PIN,(40,9,40,3)),

    (OGTA4_DOG,(40,30)),

    (STA_mini,(60,0)),
    (STA_mini,(60,1)),

    # (STAML2_BALANCE,(60,2,200,30)),

    (PTA2_LISICA,(10,1)), 
    (PTA2_LISICA,(60,2)), 
    (PTA2_DDCrWork,(50,)),

    (PTA2_BDDCr_UNIVERSAL,(30,1,1)), 
    (PTA2_BDDCr_UNIVERSAL,(30,1,0)), 
    (PTA2_BDDCr_UNIVERSAL,(30,0,0)), 

    (PTA2_BVGFIX,(30,1,1)), 
    (PTA2_BVGFIX,(30,1,0)), 
    (PTA2_BVGFIX,(30,0,1)), 

    (PTA2_BDDC_FIX,(30,1,1)), 
    (PTA2_BDDC_FIX,(30,1,0)), 
    (PTA2_BDDC_FIX,(30,0,1)), 

    (PTA2_BBBU,(30,1,1)), 
    (PTA2_BBBU,(30,1,0)), 
    (PTA2_BBBU,(30,0,1)), 

    (PTA2_BBBUr,(30,1,1)), 
    (PTA2_BBBUr,(30,1,0)), 
    (PTA2_BBBUr,(30,0,1)), 

    (PTA4_WLISICA,(30,2,30)),

    # (PTA4_WDDCrE,(11,30)), #C
    (PTA4_WDVCr,(21,30)),
    # (PTA4_WDDCrE,(6,30)), #C
    (PTA4_WDDCrVG,(21,30)),
    # (PTA4_WDDCrE,(10,20)), #C
    # (PTA4_WDDCr,(6,20)), #C
    (PTA4_WDDCr,(21,30)), #C
    (PTA4_WDDCr,(10,20)), #C

    (PTA4_UNIVERSAL,(30,15,30,30,"DC",'rsi',1,1)),
    (PTA4_UNIVERSAL,(30,15,50,20,"DC",'rsi',1,0)),
    (PTA4_UNIVERSAL,(30,15,20,50,"DC",'rsi',0,1)),

    # (PTA8_WDOBBY_FREEr,(6,0.5,30)),
    # (PTA8_WDOBBY_FREEr,(11,0.5,30)),
    (PTA8_LOBSTER,(30,2)),

    (PTA10_WIZARD,(50,55,12,10,30)),
    # (PTA10_WIZARD,(30,55,3,15,20)),
    # (PTA10_WIZARD,(20,55,12,25,20)),
    (PTA10_WIZARD,(50,90,3,30,20)),
    (PTA10_WIZARD,(20,90,12,20,20)),

    (PTA11_KUSURUKEN,(70,15,35,10,'c')), #A
    # (PTA11_KUSURUKEN,(50,3,20,10,'c')), #F
    (PTA11_KUSURUKEN,(40,3,25,20,'c')), #F
    (PTA11_KUSURUKEN,(90,3,35,20,'c')), #F

    # (PTA12_SWDDCr,(15,30,0.25,5,20)), #A
    (PTA12_SWDDCr,(30,40,0.5,5,25)), #A

    (PTA13_DWDDCr,(90,50,40)), #A
    
    # (PTA14_RWDDCr,(15,30,35,45)), #F
    (PTA14_RWDDCr,(90,50,10,90)), #F

    (PTA15_WIDOWMAKER,(30,30)), 

    (PTA15_TRACER,(20,0)), 
    (PTA15_TRACER,(20,1)), 
    (PTA15_TRACER,(20,-1)), 

]

wssBitgetFut1 = [

    (OGTA4_DOG,(45,15)),

    (STA_mini,(14,1)),
    (STA_mini,(14,0)),

    (STAML2_BALANCE,(60,2,200,30)),
    # (STAML2_SID,(200,10,5,30)),

    (PTA2_BDDCr_UNIVERSAL,(14,True,True)), 
    (PTA2_BDDCr_UNIVERSAL,(14,True,False)), 
    (PTA2_BDDCr_UNIVERSAL,(14,False,True)), 

    (PTA2_BVGFIX,(14,1,1)), 
    (PTA2_BVGFIX,(14,1,0)), 
    (PTA2_BVGFIX,(14,0,1)), 

    (PTA2_BDDC_FIX,(40,1,1)), 
    (PTA2_BDDC_FIX,(40,1,0)), 
    (PTA2_BDDC_FIX,(40,0,1)), 

    (PTA2_BBBU,(28,1,1)), 
    (PTA2_BBBU,(28,1,0)), 
    (PTA2_BBBU,(28,0,1)), 

    (PTA2_BBBUr,(14,1,1)), 
    (PTA2_BBBUr,(14,1,0)), 
    (PTA2_BBBUr,(14,0,1)), 

    (PTA4_WDDC,(30,30)), #C
    (PTA4_UNIVERSAL,(14,14,30,30,"DC",'rsi',True,True)),
    (PTA4_UNIVERSAL,(14,14,50,20,"DC",'rsi',True,False)),
    (PTA4_UNIVERSAL,(14,14,20,50,"DC",'rsi',False,True)),

    (PTA10_WIZARD,(50,55,12,10,30)),
    (PTA10_WIZARD,(30,55,3,15,20)),
    (PTA10_WIZARD,(20,55,12,25,20)),

    (PTA11_KUSURUKEN,(50,3,20,10,'c')), #F

    (PTA12_SWDDCr,(15,30,0.25,5,20)), #A

    (PTA15_TRACER,(20,0)), 
    (PTA15_TRACER,(20,1)), 
    (PTA15_TRACER,(20,-1)), 
]

wssBitgetFut5 = [
    (LTA_KARYCH,(30,35)),

    (STA_mini,(14,1)),
    (STA_mini,(14,0)),

    (STAML2_BALANCE,(60,2,200,30)),
    # (STAML2_SID,(200,10,5,30)),

    (PTA2_BDDCr_UNIVERSAL,(14,True,True)), 
    (PTA2_BDDCr_UNIVERSAL,(14,True,False)), 
    (PTA2_BDDCr_UNIVERSAL,(14,False,True)), 

    (PTA2_BVGFIX,(14,1,1)), 
    (PTA2_BVGFIX,(14,1,0)), 
    (PTA2_BVGFIX,(14,0,1)), 

    (PTA2_BDDC_FIX,(40,1,1)), 
    (PTA2_BDDC_FIX,(40,1,0)), 
    (PTA2_BDDC_FIX,(40,0,1)), 

    (PTA2_BBBU,(28,1,1)), 
    (PTA2_BBBU,(28,1,0)), 
    (PTA2_BBBU,(28,0,1)), 

    (PTA2_BBBUr,(14,1,1)), 
    (PTA2_BBBUr,(14,1,0)), 
    (PTA2_BBBUr,(14,0,1)), 

    (PTA4_UNIVERSAL,(14,14,30,30,"DC",'rsi',True,True)),
    (PTA4_UNIVERSAL,(14,14,50,20,"DC",'rsi',True,False)),
    (PTA4_UNIVERSAL,(14,14,20,50,"DC",'rsi',False,True)),

    (PTA10_WIZARD,(50,55,12,10,30)),
    (PTA10_WIZARD,(30,55,3,15,20)),
    (PTA10_WIZARD,(20,55,12,25,20)),

    (PTA11_KUSURUKEN,(70,9,5,10,'c')), #S
    (PTA11_KUSURUKEN,(50,9,10,10,'c')), #S

    (PTA11_KUSURUKEN,(70,15,35,10,'c')), #A
    
    (PTA12_SWDDCr,(5,10,0.25,10,5)), #A
    (PTA12_SWDDCr,(15,30,0.25,5,20)), #A

    (PTA14_RWDDCr,(10,10,20,25)), #A

    (PTA15_TRACER,(20,0)), 
    (PTA15_TRACER,(20,1)), 
    (PTA15_TRACER,(20,-1)), 

]
wssBitgetFut15 = [

    (STA_mini,(14,1)),
    (STA_mini,(14,0)),

    (STAML2_BALANCE,(60,2,200,30)),
    # (STAML2_SID,(200,10,5,30)),

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

    (PTA8_OBBY,(21,0.5)), #S

    (PTA12_SWDDCr,(20,30,0.25,15,5)), #A
    (PTA12_SWDDCr,(5,10,0.25,10,20)), #A

    (PTA15_TRACER,(20,0)), 
    (PTA15_TRACER,(20,1)), 
    (PTA15_TRACER,(20,-1)), 

]
wssBitgetFut30 = [
    (STA_mini,(7,1)),
    (STA_mini,(7,0)),

    (STAML2_BALANCE,(60,2,200,30)),
    # (STAML2_SID,(200,10,5,30)),


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
    
    (PTA15_WIDOWMAKER,(10,30)), #A
    (PTA15_TRACER,(10,0)), 
    (PTA15_TRACER,(10,1)), 
    (PTA15_TRACER,(10,-1)), 

]
wssBitgetFut60 = (
    (STA_mini,(10,1)),
    (STA_mini,(10,0)),
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

    (PTA15_KERRIGAN,(10,)), #A
    (PTA15_WIDOWMAKER,(5,40)), #A
    (PTA15_NOVA,(45,)), #A
    (PTA15_TRACER,(5,0)), 
    (PTA15_TRACER,(5,1)), 
    (PTA15_TRACER,(5,-1)), 
)

