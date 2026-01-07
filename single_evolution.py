def main():
    raw_file = 'DataForTests\DataMoexFut5P\_5IMOEXF_1_1766374056.parquet'
    n_save_cores = 1
    n_individuals = 100
    step_save = 2
    init_population_dir=None
    # init_population_dir='modelML\_nls_models'
    close_on_time = False
    kind_test = 0
    normalization = False
    new_tf = None
    vtb = True
    evo = Evolutionist3(n_individuals,raw_file,NLSTA1_UNION,[],NLSNN1,n_save_cores=n_save_cores,step_save=step_save,init_population_dir=init_population_dir,need_adapt=False,kind_test=kind_test,normalization=normalization,close_on_time=close_on_time,new_tf=new_tf,vtb=vtb)
    evo.evolution(500)

if __name__ == '__main__':
    from strategies.work_strategies.NLSTA import NLSTA1_UNION
    from Optimiztion.models_nn.linear_models import NLSNN1
    from Optimiztion.generation_wss.Evolutionist3 import Evolutionist3
    main()
