from strategies.work_strategies.PTA import PTA4_WDDCr,PTA4_WDDCrE,PTA4_WDDCrVG,PTA4_WDVCr,PTA4_WLISICA,PTA8_WDOBBY_FREEr,PTA4_UNIVERSAL,PTA2_LISICA,PTA4_WDDC,PTA8_OBBY,PTA2_DDCrWork,PTA2_BDDCr_UNIVERSAL,PTA2_BDDC_FIX,PTA2_BVGFIX,PTA2_BBBU,PTA2_BBBUr,PTA2_DDCrVG,PTA2_DVCr,PTA2_VOLCHARA,PTA8_LOBSTER
from strategies.work_strategies.PTAX import PTA10_WIZARD,PTA10_SORCERER,PTA11_KUSURUKEN,PTA12_SWDDCr,PTA14_RWDDCr,PTA15_NOVA,PTA15_KERRIGAN,PTA15_WIDOWMAKER,PTA15_TRACER,PTA10_MAGIC,PTA13_DWDDCr,PTA15_SILVANA,PTA15_VALLA,PTA15_ANNA,PTA18_GULDAN,PTA18_DIABLO,PTA18_ARTAS,PTA18_CHOGALL,PTA18_DEHAKA,PTA18_KELTHUZAD,PTA18_REXXAR,PTA18_VARIAN,PTA18_BLAZE,PTA19_JOHANNA,PTA19_TYRAEL,PTA19_ANUBARAK

from strategies.work_strategies.STA_ml2 import STAML2_CHAOS,STAML2_NEWAVE,STAML2_SID,STAML2_GOLDENMEAN
from strategies.work_strategies.STA_ca import STA_mini,STA2,STA2_FAST,STA2_SLOW,STA2_ULTRA
from strategies.work_strategies.LTA import LTA_OKROSHKA,LTA_PIN,LTA_KARYCH
from strategies.work_strategies.LTA2 import LTA2_LOGAN
from strategies.work_strategies.OGTA import OGTA4_DOG


wssMoexFut1 = [
    (LTA_OKROSHKA,(10,80)),
    (LTA_PIN,(10,6,40,5)),
    (LTA2_LOGAN,(10,100,30)),
    (LTA2_LOGAN,(30,100,30)),

    (OGTA4_DOG,(10,40)),

    (STA2,(100,3,25)),
    (STA2_FAST,(100,3,20,25)),
    (STA2_SLOW,(100,5,15,25)),
    (STA2_ULTRA,(100,3,20,15)),

    (STAML2_GOLDENMEAN,(60,2,30,30)),
    (STAML2_NEWAVE,(5,5,0.5,30)),

    (PTA2_DDCrWork,(5,)),
    (PTA2_LISICA,(7,2)), 
    (PTA2_VOLCHARA,(10,1)), 
    (PTA2_DDCrVG,(10,)), 
    (PTA2_DVCr,(20,)), 

    (PTA2_BDDCr_UNIVERSAL,(7,1,1)), 
    (PTA2_BDDCr_UNIVERSAL,(7,1,0)), 
    (PTA2_BDDCr_UNIVERSAL,(7,0,1)), 

    (PTA2_BVGFIX,(7,1,1)), 
    (PTA2_BVGFIX,(7,1,0)), 
    (PTA2_BVGFIX,(7,0,1)), 

    (PTA2_BBBU,(14,1,1)), 
    (PTA2_BBBU,(14,1,0)), 
    (PTA2_BBBU,(14,0,1)), 

    (PTA2_BBBUr,(7,1,1)), 
    (PTA2_BBBUr,(7,1,0)), 
    (PTA2_BBBUr,(7,0,1)), 

    (PTA4_WDDCrE,(11,30)), #C
    (PTA4_WDDCrE,(10,20)), #C
    (PTA4_WDDCrE,(6,30)), #C
    (PTA4_WDDCr,(6,30)), #C
    (PTA4_WDDCr,(11,30)), #C

    (PTA4_WDDCrVG,(11,30)),
    (PTA4_WDVCr,(11,30)),
    (PTA4_WLISICA,(7,2,30)),

    (PTA4_UNIVERSAL,(7,7,30,30,"DC",'rsi',1,1)),
    (PTA4_UNIVERSAL,(7,7,60,20,"DC",'rsi',1,0)),
    (PTA4_UNIVERSAL,(7,7,20,60,"DC",'rsi',0,1)),

    (PTA8_WDOBBY_FREEr,(6,0.5,30)),

    (PTA10_WIZARD,(20,55,12,25,20)),
    (PTA10_WIZARD,(30,55,3,15,20)),
    (PTA10_WIZARD,(50,55,12,10,30)),
    (PTA10_MAGIC,(40,80,3)),

    (PTA11_KUSURUKEN,(50,6,5,20,'c')), #A
    (PTA11_KUSURUKEN,(70,3,10,40,'hl')), #F
    (PTA11_KUSURUKEN,(50,3,20,10,'c')), #F

    (PTA12_SWDDCr,(15,30,0.25,5,20)), #A
    (PTA12_SWDDCr,(10,30,0.5,5,15)), #A

    (PTA13_DWDDCr,(70,40,10)), #Проблемы оптимизации

    (PTA14_RWDDCr,(15,30,35,45)), #F
    (PTA14_RWDDCr,(10,30,90,80)), #F

    (PTA15_WIDOWMAKER,(5,30)), 
    # (PTA15_KERRIGAN,(5,)), #A
    (PTA15_SILVANA,(5,30,5)), 
    (PTA15_ANNA,(5,30)), 

    (PTA15_VALLA,(10,0)), 
    (PTA15_VALLA,(10,1)), 
    (PTA15_VALLA,(10,-1)), 

    (PTA15_TRACER,(10,0)), 
    (PTA15_TRACER,(10,1)), 
    (PTA15_TRACER,(10,-1)), 

    (PTA18_ARTAS,(100,3,10,20)), 
    (PTA18_KELTHUZAD,(100,3,10,10)), 
    (PTA18_CHOGALL,(100,7,10,40)), 
    (PTA18_GULDAN,(100,7,10,40)), 
    (PTA18_DIABLO,(100,5,15,30)), 
    (PTA18_DEHAKA,(100,5,15,30)), 
    (PTA18_REXXAR,(100,5,10,50,30)), 
    (PTA18_VARIAN,(100,3,10,20,25)),    
    (PTA18_BLAZE,(70,10,71,40,30,0)),    
    (PTA18_BLAZE,(70,10,71,40,30,1)),  

    (PTA19_ANUBARAK,(30,10,40,20,10,0)),    
    (PTA19_ANUBARAK,(30,10,40,20,10,1)),    
    (PTA19_JOHANNA,(100,7,10,10,40,20,0)),    
    (PTA19_JOHANNA,(100,7,10,10,40,20,1)),    
    (PTA19_TYRAEL,(100,10,5,10,50,40,0)),    
    (PTA19_TYRAEL,(100,10,5,10,50,40,1)),    
 

]
wssMoexFut5 = [
    (LTA_OKROSHKA,(10,80)),
    (LTA_PIN,(10,6,40,5)),
    (LTA_PIN,(20,3,40,3)), #2104
    (LTA2_LOGAN,(10,100,30)),
    
    (OGTA4_DOG,(40,30)),
    (OGTA4_DOG,(10,40)),
    (OGTA4_DOG,(30,50)), #2104

    (STA_mini,(7,1)),
    (STA_mini,(7,0)),
    (STA2,(100,5,5)),
    (STA2_FAST,(100,3,20,27)),
    (STA2_SLOW,(100,3,20,25)),
    (STA2_ULTRA,(100,7,5,15)),

    (STAML2_GOLDENMEAN,(60,2,30,30)),
    (STAML2_NEWAVE,(5,5,0.5,30)),

    (PTA2_DDCrWork,(5,)),
    (PTA2_LISICA,(7,2)), 
    (PTA2_LISICA,(70,1.5)), 
    (PTA2_DDCrVG,(5,)), 
    (PTA2_DVCr,(5,)), 
    (PTA2_DVCr,(50,)), 

    (PTA2_BDDCr_UNIVERSAL,(7,1,1)), 
    (PTA2_BDDCr_UNIVERSAL,(7,1,0)), 
    (PTA2_BDDCr_UNIVERSAL,(7,0,1)), 

    (PTA2_BVGFIX,(7,1,1)), 
    (PTA2_BVGFIX,(7,1,0)), 
    (PTA2_BVGFIX,(7,0,1)), 

    (PTA2_BDDC_FIX,(10,1,1)), 
    (PTA2_BDDC_FIX,(10,1,0)), 
    (PTA2_BDDC_FIX,(10,0,1)), 

    (PTA2_BBBU,(14,1,1)), 
    (PTA2_BBBU,(14,1,0)), 
    (PTA2_BBBU,(14,0,1)), 

    (PTA2_BBBUr,(7,1,1)), 
    (PTA2_BBBUr,(7,1,0)), 
    (PTA2_BBBUr,(7,0,1)), 

    # (PTA4_WDDCrE,(11,30)), #C
    # (PTA4_WDDCrE,(10,20)), #C
    (PTA4_WDDCrE,(6,30)), #C
    # (PTA4_WDDCr,(6,30)), #C
    (PTA4_WDDCr,(11,30)), #C

    (PTA4_WDDCrVG,(7,30)),
    (PTA4_WDVCr,(7,30)),
    (PTA4_WLISICA,(7,2,30)),

    (PTA4_UNIVERSAL,(7,7,30,30,"DC",'rsi',1,1)),
    (PTA4_UNIVERSAL,(7,7,60,20,"DC",'rsi',1,0)),
    (PTA4_UNIVERSAL,(7,7,20,60,"DC",'rsi',0,1)),

    (PTA4_UNIVERSAL,(15,15,50,50,"VC",'uo',1,1)),
    (PTA4_UNIVERSAL,(20,10,50,30,"BB",'mfi',1,1)),

    (PTA8_WDOBBY_FREEr,(6,0.5,30)),

    (PTA10_MAGIC,(80,10,9)),
    (PTA10_WIZARD,(20,10,6,30,20)),
    (PTA10_WIZARD,(20,55,12,25,20)),
    (PTA10_WIZARD,(30,55,3,15,20)),

    (PTA11_KUSURUKEN,(10,9,30,40,'c')), #F
    (PTA11_KUSURUKEN,(10,12,10,40,'hl')), #A
    (PTA11_KUSURUKEN,(50,3,20,10,'c')), #F

    (PTA12_SWDDCr,(20,40,1,10,5)), #A
    (PTA12_SWDDCr,(10,30,0.5,5,15)), #A

    (PTA14_RWDDCr,(10,30,50,40)), #F
    (PTA14_RWDDCr,(10,30,90,80)), #F

    (PTA15_WIDOWMAKER,(5,30)), 
    (PTA15_SILVANA,(5,30,5)), 
    (PTA15_ANNA,(5,30)), 

    (PTA15_VALLA,(10,0)), 
    (PTA15_VALLA,(10,1)), 
    (PTA15_VALLA,(10,-1)), 

    (PTA18_ARTAS,(100,5,5,20)), 
    (PTA18_KELTHUZAD,(100,5,5,20)), 
    (PTA18_REXXAR,(100,5,5,50,20)), 
    (PTA18_CHOGALL,(100,5,5,40)), 
    (PTA18_GULDAN,(100,5,5,40)), 
    (PTA18_DEHAKA,(100,5,5,20)), 
    (PTA18_DIABLO,(100,5,5,20)), 
    (PTA18_VARIAN,(100,5,5,20,25)), 
    (PTA18_BLAZE,(10,5,101,50,40,0)),    
    (PTA18_BLAZE,(10,5,101,50,40,1)),       
  
    (PTA19_ANUBARAK,(10,5,50,40,20,0)),    
    (PTA19_ANUBARAK,(10,5,50,40,20,1)),    
    (PTA19_JOHANNA,(100,3,5,10,40,10,0)),    
    (PTA19_JOHANNA,(100,3,5,10,40,10,1)),    
    (PTA19_TYRAEL,(100,3,5,50,40,30,0)),    
    (PTA19_TYRAEL,(100,3,5,50,40,30,1)),      

]

wssMoexStocks1 = [
    (LTA_OKROSHKA,(20,10)),
    (LTA_PIN,(60,12,40,3)),
    (LTA2_LOGAN,(100,100,30)),
    (OGTA4_DOG,(60,30)),

    (STA_mini,(90,0)),
    (STA_mini,(90,1)),
    (STA2_FAST,(100,3,40,35)),
    (STA2_SLOW,(100,3,35,35)),
    (STA2_ULTRA,(100,3,20,35)),

    (STAML2_GOLDENMEAN,(60,2,200,30)),
    # (STAML2_SID,(200,10,5,30,0.2)),

    (PTA2_LISICA,(60,1)), 
    (PTA2_LISICA,(90,2)), 
    (PTA2_DDCrWork,(100,)),

    (PTA2_BDDCr_UNIVERSAL,(60,1,1)), 
    (PTA2_BDDCr_UNIVERSAL,(60,1,0)), 
    (PTA2_BDDCr_UNIVERSAL,(60,0,0)), 

    (PTA2_BVGFIX,(60,1,1)), 
    (PTA2_BVGFIX,(60,1,0)), 
    (PTA2_BVGFIX,(60,0,1)), 

    (PTA2_BBBU,(60,1,1)), 
    (PTA2_BBBU,(60,1,0)), 
    (PTA2_BBBU,(60,0,1)), 

    (PTA2_BBBUr,(60,1,1)), 
    (PTA2_BBBUr,(60,1,0)), 
    (PTA2_BBBUr,(60,0,1)), 

    (PTA4_WLISICA,(30,2,30)),
    (PTA4_WDVCr,(30,30)),
    (PTA4_WDDCrVG,(30,30)),
    (PTA4_WDDCr,(30,30)), #C

    (PTA4_UNIVERSAL,(30,15,30,30,"DC",'rsi',1,1)),
    (PTA4_UNIVERSAL,(30,15,50,20,"DC",'rsi',1,0)),
    (PTA4_UNIVERSAL,(30,15,20,50,"DC",'rsi',0,1)),

    (PTA11_KUSURUKEN,(120,30,35,10,'c')), #A
    (PTA11_KUSURUKEN,(90,3,35,20,'c')), #F

    (PTA12_SWDDCr,(90,40,0.5,5,25)), #A

    (PTA13_DWDDCr,(90,50,40)), #A
    
    (PTA14_RWDDCr,(90,50,10,90)), #F

    (PTA15_WIDOWMAKER,(30,30)), 
    (PTA15_SILVANA,(30,30,20)), 
    (PTA15_ANNA,(30,30)), 
    (PTA15_TRACER,(60,0)), 
    (PTA15_TRACER,(60,1)), 
    (PTA15_TRACER,(60,-1)), 
    (PTA15_VALLA,(60,0)), 
    (PTA15_VALLA,(60,1)), 
    (PTA15_VALLA,(60,-1)), 

    (PTA18_ARTAS,(100,7,15,20)), 
    (PTA18_KELTHUZAD,(100,7,15,20)), 
    (PTA18_CHOGALL,(100,10,10,30)), 
    (PTA18_GULDAN,(100,10,10,30)), 
    (PTA18_DIABLO,(100,7,15,30)), 
    (PTA18_DEHAKA,(100,7,15,30)), 
    (PTA18_REXXAR,(100,7,15,40,10)), 
    (PTA18_VARIAN,(100,7,15,10,10)), 
    (PTA18_BLAZE,(10,15,11,50,10,0)),    
    (PTA18_BLAZE,(10,15,11,50,10,1)),  

    (PTA19_ANUBARAK,(30,35,50,20,20,0)),    
    (PTA19_ANUBARAK,(30,35,50,20,20,1)),    
    (PTA19_JOHANNA,(100,3,35,30,50,20,0)),    
    (PTA19_JOHANNA,(100,3,35,30,50,20,1)),    
    (PTA19_TYRAEL,(100,5,35,46,40,20,0)),    
    (PTA19_TYRAEL,(100,5,35,46,40,20,1)),    

]
wssMoexStocks5 = [
    (LTA_OKROSHKA,(10,30)),
    (LTA_PIN,(40,9,40,3)),
    (LTA2_LOGAN,(20,100,30)),

    (OGTA4_DOG,(40,30)),

    (STA_mini,(20,0)),
    (STA_mini,(20,1)),
    (STA2_FAST,(100,3,40,35)),
    (STA2_SLOW,(100,3,35,35)),
    (STA2_ULTRA,(100,3,20,35)),

    (STAML2_GOLDENMEAN,(60,2,200,30)),
    # (STAML2_SID,(200,10,5,30,0.2)),

    (PTA2_LISICA,(10,1)), 
    (PTA2_DDCrWork,(20,)),
    (PTA2_DDCrWork,(50,)),

    (PTA2_BDDCr_UNIVERSAL,(30,1,1)), 
    (PTA2_BDDCr_UNIVERSAL,(30,1,0)), 
    (PTA2_BDDCr_UNIVERSAL,(30,0,1)), 

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
    (PTA4_WDVCr,(21,30)),
    (PTA4_WDDCrVG,(21,30)),
    (PTA4_WDDCr,(21,30)), #C

    (PTA4_UNIVERSAL,(30,15,30,30,"DC",'rsi',1,1)),
    (PTA4_UNIVERSAL,(30,15,50,20,"DC",'rsi',1,0)),
    (PTA4_UNIVERSAL,(30,15,20,50,"DC",'rsi',0,1)),

    (PTA4_UNIVERSAL,(20,5,20,20,"BB",'mfi',1,1)),
    (PTA4_UNIVERSAL,(20,10,30,30,"WC",'rsi',1,1)),
    (PTA4_UNIVERSAL,(20,5,30,30,"VG",'mfi',1,1)),

    (PTA10_WIZARD,(20,50,12,30,20)),

    (PTA11_KUSURUKEN,(10,9,20,20,'c')), #A
    (PTA11_KUSURUKEN,(70,15,35,10,'c')), #A

    (PTA12_SWDDCr,(10,30,1,10,20)), #A

    (PTA13_DWDDCr,(60,40,10)), #A
    
    (PTA14_RWDDCr,(10,40,10,100)), #F

    (PTA15_ANNA,(5,30)), 
    (PTA15_VALLA,(10,0)), 
    (PTA15_VALLA,(10,1)), 
    (PTA15_VALLA,(10,-1)), 

    (PTA18_ARTAS,(100,10,5,10)), 
    (PTA18_KELTHUZAD,(100,10,5,10)), 
    (PTA18_CHOGALL,(100,10,5,40)), 
    (PTA18_GULDAN,(100,10,5,40)), 
    (PTA18_DIABLO,(100,10,10,20)), 
    (PTA18_DEHAKA,(100,10,10,20)), 
    (PTA18_REXXAR,(100,10,5,40,10)), 
    (PTA18_VARIAN,(100,7,5,10,30)), 
    (PTA18_BLAZE,(30,5,26,40,10,0)),    
    (PTA18_BLAZE,(30,5,26,40,10,1)),    

    (PTA19_ANUBARAK,(30,5,40,10,20,0)),    
    (PTA19_ANUBARAK,(30,5,40,10,20,1)),    
    (PTA19_JOHANNA,(100,7,5,90,30,10,0)),    
    (PTA19_JOHANNA,(100,7,5,90,30,10,1)),    
    (PTA19_TYRAEL,(100,3,10,70,40,30,0)),    
    (PTA19_TYRAEL,(100,3,10,70,40,30,1)),    
]

wssBitgetFut1 = [

    (OGTA4_DOG,(45,15)),

    (STA_mini,(14,1)),
    (STA_mini,(14,0)),

    (STAML2_GOLDENMEAN,(60,2,200,30)),
    (STAML2_SID,(200,10,5,30,0.2)),

    (PTA2_BDDCr_UNIVERSAL,(14,1,1)), 
    (PTA2_BDDCr_UNIVERSAL,(14,1,0)), 
    (PTA2_BDDCr_UNIVERSAL,(14,0,1)), 

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
    (PTA4_UNIVERSAL,(14,14,30,30,"DC",'rsi',1,1)),
    (PTA4_UNIVERSAL,(14,14,50,20,"DC",'rsi',1,0)),
    (PTA4_UNIVERSAL,(14,14,20,50,"DC",'rsi',0,1)),

    (PTA10_WIZARD,(50,55,12,10,30)),
    (PTA10_WIZARD,(30,55,3,15,20)),
    (PTA10_WIZARD,(20,55,12,25,20)),

    (PTA11_KUSURUKEN,(50,3,20,10,'c')), #F

    (PTA12_SWDDCr,(15,30,0.25,5,20)), #A

    (PTA15_VALLA,(70,0)), 
    (PTA15_VALLA,(70,1)), 
    (PTA15_VALLA,(70,-1)), 

    (PTA15_TRACER,(20,0)), 
    (PTA15_TRACER,(20,1)), 
    (PTA15_TRACER,(20,-1)), 
]

wssBitgetFut5 = [
    (LTA_KARYCH,(30,35)),

    (STA_mini,(14,1)),
    (STA_mini,(14,0)),

    (STAML2_GOLDENMEAN,(60,2,200,30)),
    (STAML2_SID,(200,10,5,30,0.2)),

    (PTA2_BDDCr_UNIVERSAL,(14,1,1)), 
    (PTA2_BDDCr_UNIVERSAL,(14,1,0)), 
    (PTA2_BDDCr_UNIVERSAL,(14,0,1)), 

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

    (PTA4_UNIVERSAL,(14,14,30,30,"DC",'rsi',1,1)),
    (PTA4_UNIVERSAL,(14,14,50,20,"DC",'rsi',1,0)),
    (PTA4_UNIVERSAL,(14,14,20,50,"DC",'rsi',0,1)),

    (PTA10_WIZARD,(50,55,12,10,30)),
    (PTA10_WIZARD,(30,55,3,15,20)),
    (PTA10_WIZARD,(20,55,12,25,20)),

    (PTA11_KUSURUKEN,(70,9,5,10,'c')), #S
    (PTA11_KUSURUKEN,(50,9,10,10,'c')), #S

    (PTA11_KUSURUKEN,(70,15,35,10,'c')), #A
    
    (PTA12_SWDDCr,(5,10,0.25,10,5)), #A
    (PTA12_SWDDCr,(15,30,0.25,5,20)), #A

    (PTA14_RWDDCr,(10,10,20,25)), #A

    (PTA15_SILVANA,(35,40,50)), 
    (PTA15_TRACER,(20,0)), 
    (PTA15_TRACER,(20,1)), 
    (PTA15_TRACER,(20,-1)), 

]
wssBitgetFut15 = [

    (STA_mini,(14,1)),
    (STA_mini,(14,0)),

    (STAML2_GOLDENMEAN,(60,2,200,30)),
    (STAML2_SID,(200,10,5,30,0.2)),

    (PTA2_BDDCr_UNIVERSAL,(7,1,1)), 
    (PTA2_BDDCr_UNIVERSAL,(7,1,0)), 
    (PTA2_BDDCr_UNIVERSAL,(7,0,1)), 
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

    (PTA4_UNIVERSAL,(7,7,30,30,"DC",'rsi',1,1)),
    (PTA4_UNIVERSAL,(7,7,50,20,"DC",'rsi',1,0)),
    (PTA4_UNIVERSAL,(7,7,20,50,"DC",'rsi',0,1)),

    (PTA8_OBBY,(21,0.5)), #S

    (PTA12_SWDDCr,(20,30,0.25,15,5)), #A
    (PTA12_SWDDCr,(5,10,0.25,10,20)), #A

    (PTA15_SILVANA,(45,40,35)), 
    
    (PTA15_VALLA,(45,0)), 
    (PTA15_VALLA,(45,1)), 
    (PTA15_VALLA,(45,-1)), 
    (PTA15_TRACER,(20,0)), 
    (PTA15_TRACER,(20,1)), 
    (PTA15_TRACER,(20,-1)), 

]
wssBitgetFut30 = [
    (STA_mini,(7,1)),
    (STA_mini,(7,0)),

    (STAML2_GOLDENMEAN,(60,2,200,30)),
    (STAML2_SID,(200,10,5,30,0.2)),

    (PTA2_BDDCr_UNIVERSAL,(7,1,1)), 
    (PTA2_BDDCr_UNIVERSAL,(7,1,0)), 
    (PTA2_BDDCr_UNIVERSAL,(7,0,1)), 
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
    (PTA4_UNIVERSAL,(7,7,30,30,"DC",'rsi',1,1)),
    (PTA4_UNIVERSAL,(7,7,50,20,"DC",'rsi',1,0)),
    (PTA4_UNIVERSAL,(7,7,20,50,"DC",'rsi',0,1)),
    
    (PTA15_WIDOWMAKER,(10,30)), #A
    (PTA15_ANNA,(10,30)), #A
    (PTA15_TRACER,(10,0)), 
    (PTA15_TRACER,(10,1)), 
    (PTA15_TRACER,(10,-1)), 

]
wssBitgetFut60 = (
    (STA_mini,(10,1)),
    (STA_mini,(10,0)),
    (PTA2_BDDCr_UNIVERSAL,(7,1,1)), 
    (PTA2_BDDCr_UNIVERSAL,(7,1,0)), 
    (PTA2_BDDCr_UNIVERSAL,(7,0,1)), 
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
    (PTA4_UNIVERSAL,(7,7,30,30,"DC",'rsi',1,1)),
    (PTA4_UNIVERSAL,(7,7,50,20,"DC",'rsi',1,0)),
    (PTA4_UNIVERSAL,(7,7,20,50,"DC",'rsi',0,1)),

    (PTA15_KERRIGAN,(10,)), #A
    (PTA15_WIDOWMAKER,(5,40)), #A
    (PTA15_ANNA,(5,40)), #A
    (PTA15_NOVA,(45,)), #A
    (PTA15_TRACER,(5,0)), 
    (PTA15_TRACER,(5,1)), 
    (PTA15_TRACER,(5,-1)), 
)

