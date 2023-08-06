import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
from scipy.stats import hypergeom, _distn_infrastructure
from typing import Union, List, Mapping, Tuple, Optional, Any
from typeguard import typechecked
import pandas as pd
from functools import partial
import multiprocessing
import time

### CONSTANTS
_GENOME_CONC_PG = 6.6
_PG_TO_NG = 0.001
_GENOME_CONC_NG = _GENOME_CONC_PG * _PG_TO_NG
_UG_TO_NG = 1000

@typechecked
def simulate_gRNA_library_prep(guide_library_size: int, PCR1_input_ug: float, MOI: float,  perfection_rate: float, genome_conc_ng: float = _GENOME_CONC_NG, _PCR1_input_number_duplicate:float = 1, PCR1_cycles: int = 5, _PCR1_purification_yield: float = 0.6,
                              _PCR1_purification_eluted_volume: int = 50, _PCR2_input_volume: float = 22.5,
                              PCR2_cycles:int = 7, _PCR2_purification_yield: float = 0.6,
                              _total_target_reads: Union[int, np.int32] = 150000, plot=True):
    _total_target_reads = int(_total_target_reads)

    '''
    PCR1 input
    '''
    _PCR1_input_number_molecules: float = (((PCR1_input_ug*_UG_TO_NG)/genome_conc_ng)) * MOI
    _PCR1_input_guide_coverage: float = ((_PCR1_input_number_molecules*perfection_rate)/_PCR1_input_number_duplicate)/guide_library_size
    #print(_PCR1_input_guide_coverage)
    '''
        PCR1 amplification
    '''
    
    _PCR1_product_number_molecules: float = _PCR1_input_number_molecules * 2**PCR1_cycles
    _PCR1_product_number_duplicates: float = _PCR1_input_number_duplicate * 2**PCR1_cycles
    _PCR1_product_guide_coverage: float = (_PCR1_product_number_molecules*perfection_rate) / guide_library_size

    #print(_PCR1_product_guide_coverage)
    '''
    PCR1 purification
    '''
    
    _PCR1_product_purified_number_molecules: float = _PCR1_product_number_molecules * _PCR1_purification_yield
    _PCR1_product_purified_number_duplicates: float = _PCR1_product_number_duplicates * _PCR1_purification_yield 

    '''
    PCR2 input
    '''
    _PCR2_input_fraction: float = _PCR2_input_volume/_PCR1_purification_eluted_volume
    _PCR2_input_number_molecules: float  = _PCR2_input_fraction * _PCR1_product_purified_number_molecules
    _PCR2_input_guide_coverage: float = _PCR2_input_number_molecules / guide_library_size
    #print(_PCR2_input_guide_coverage)
    
    '''
    Determine distribution of number of duplicates in PCR2 input
    
    Assuming PCR purification yield is deterministic
    '''
    population_size: int = int(_PCR1_product_purified_number_molecules)
    success_size: int = int(_PCR1_product_purified_number_duplicates)
    trial_count: int = int(_PCR2_input_number_molecules)

    #print(f"Number duplicates in PCR2 distribution: hypergeom(N={population_size}, M={success_size}, n={trial_count})")
    num_dups_in_PCR2_input_DIST: _distn_infrastructure.rv_frozen = hypergeom(population_size, success_size, trial_count)
    #num_dups_in_PCR2_input_EXPECTED_VALUE = hypergeom.mean(population_size, success_size, trial_count)

    #print(f"PCR2 input hypergeom interval inputs: hypergeom.interval({0.99}, population_size={population_size}, success_size={success_size}, trial_count={trial_count})")
    num_dups_in_PCR2_input_VALUES_LEFT_QUANTILE, num_dups_in_PCR2_input_VALUES_RIGHT_QUANTILE = hypergeom.interval(0.99, population_size, success_size, trial_count)

    num_dups_in_PCR2_input_VALUES_LEFT_QUANTILE: int = int(num_dups_in_PCR2_input_VALUES_LEFT_QUANTILE)
    num_dups_in_PCR2_input_VALUES_RIGHT_QUANTILE: int = int(num_dups_in_PCR2_input_VALUES_RIGHT_QUANTILE)
    #print(f"Considering PCR duplicates in range: {num_dups_in_PCR2_input_VALUES_LEFT_QUANTILE} to {num_dups_in_PCR2_input_VALUES_RIGHT_QUANTILE}")

    num_dups_in_PCR2_input_VALUES: np.ndarray  = np.arange(num_dups_in_PCR2_input_VALUES_LEFT_QUANTILE, num_dups_in_PCR2_input_VALUES_RIGHT_QUANTILE)
    # For each x-value in the interval of interest, get the probability of that number of rarities in the PCR1 input
    num_dups_in_PCR2_input_PROB: np.ndarray = num_dups_in_PCR2_input_DIST.pmf(num_dups_in_PCR2_input_VALUES)
    '''
    PCR2 amplification
    '''
    _PCR2_product_number_molecules: float = _PCR2_input_number_molecules * 2**PCR2_cycles
    num_dups_in_PCR2_prod_VALUES: np.ndarray = num_dups_in_PCR2_input_VALUES * 2**PCR2_cycles
    
    '''
    PCR2 purification
    '''
    _PCR2_product_purified_number_molecules: float = _PCR2_product_number_molecules * _PCR2_purification_yield
    num_dups_in_PCR2_prod_purified_VALUES: np.ndarray = num_dups_in_PCR2_prod_VALUES * _PCR2_purification_yield

    '''
        NGS
    '''
    population_size: int = int(_PCR2_product_purified_number_molecules)
    success_sizes: np.ndarray = num_dups_in_PCR2_prod_purified_VALUES.astype(np.int32)
    trial_count: int = _total_target_reads
    num_dups_in_NGS_input_2D_DIST: np.ndarray = np.asarray([hypergeom(population_size, success_size, trial_count) for success_size in success_sizes]) # for each potential amount of duplicates of a PCR1 input molecule, get distribution of number of duplicates in reads

    ngs_duplicate_threshold = 15
    num_dups_in_NGS_input_1D_DIST_MARGINAL_NGS_VALUES: np.ndarray = np.arange(0, ngs_duplicate_threshold) # number of reads per input molecule
    num_dups_in_NGS_input_1D_DIST_MARGINAL_NGS_PROBS: np.ndarray = np.asarray([sum([num_dups_in_NGS_input_2D_DIST[i].pmf(num_reads_per_input) *  num_dups_in_PCR2_input_PROB[i] for i in range(len(num_dups_in_PCR2_input_PROB))]) for num_reads_per_input in num_dups_in_NGS_input_1D_DIST_MARGINAL_NGS_VALUES])
    
    #average_num_of_duplicates_per_PCR1_input_molecule: float = sum(num_dups_in_NGS_input_1D_DIST_MARGINAL_NGS_PROBS[np.where(np.isin(num_dups_in_NGS_input_1D_DIST_MARGINAL_NGS_VALUES,np.arange(2,ngs_duplicate_threshold)))[0]] * (np.arange(2,ngs_duplicate_threshold)-1)) * _PCR1_input_number_molecules
    
    #num_dups_in_NGS_input_1D_DIST_MARGINAL_NGS_VALUES_ZT: np.ndarray = num_dups_in_NGS_input_1D_DIST_MARGINAL_NGS_VALUES[1:]
    #num_dups_in_NGS_input_1D_DIST_MARGINAL_NGS_PROBS_ZT: np.ndarray = num_dups_in_NGS_input_1D_DIST_MARGINAL_NGS_PROBS[1:]
    
    # Plot the hypergeometric distribution for number of duplicates in PCR1 input
    if plot:
        threshold=ngs_duplicate_threshold
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(num_dups_in_NGS_input_1D_DIST_MARGINAL_NGS_VALUES[:threshold], num_dups_in_NGS_input_1D_DIST_MARGINAL_NGS_PROBS[:threshold], 'bo', label="Exact Hypergeometric")
        ax.vlines(num_dups_in_NGS_input_1D_DIST_MARGINAL_NGS_VALUES[:threshold], 0, num_dups_in_NGS_input_1D_DIST_MARGINAL_NGS_PROBS[:threshold], lw=2)
        ax.set_xlabel('Number of average reads per\nPCR1 input molecule')
        ax.set_ylabel('Probability')
        ax.set_title("Number of Reads per PCR1 Input Molecule\nread coverage = {}".format(_total_target_reads))
        ax.set_xticklabels(ax.get_xticks(), rotation = 45)

        plt.show()

    # Get the exact guide coverage
    guide_coverage_exact = (((_PCR1_input_number_molecules*(1-num_dups_in_NGS_input_1D_DIST_MARGINAL_NGS_PROBS[0]))*perfection_rate)/_PCR1_input_number_duplicate)/guide_library_size
    
    return guide_coverage_exact




@typechecked
def get_target_coverage_linear_interop(guide_coverages_np: np.ndarray, total_reads_targets_np: np.ndarray, target_coverage: float = 100):
    '''
        Provided the list of reads and their simulated guide coverage, get the interpolated reads given the target coverage
    '''
    # Get the closest simulated coverages to the guide coverages
    target_coverage_indices = np.argsort(abs(guide_coverages_np-target_coverage))[0:2]
    target_coverage_indices = target_coverage_indices[np.argsort(-total_reads_targets_np[target_coverage_indices])]

    # Calculate the interpolation and return
    return total_reads_targets_np[target_coverage_indices[0]]  - ((total_reads_targets_np[target_coverage_indices[0]] - total_reads_targets_np[target_coverage_indices[1]]) * (guide_coverages_np[target_coverage_indices[0]] - target_coverage)/(guide_coverages_np[target_coverage_indices[0]] - guide_coverages_np[target_coverage_indices[1]]))


# TODO 20230417 - For target_coverage_percentage, a future step is to determine the inflection point manually by either the simulation result or from solving the hypergeometric distribution (which is definitely possible) 
@typechecked
def get_target_coverage(gDNA_amount: float, moi: float, sample_name:str, perfection_rate: float, guide_library_size:int, genome_conc_ng: float = _GENOME_CONC_NG, target_coverage_input=None, target_coverage_percentage: float=0.70, read_intervals_count: int= 20, cores=1):

    PCR1_input_coverage = (((((gDNA_amount*_UG_TO_NG)/genome_conc_ng)*moi))*perfection_rate)/guide_library_size
    target_coverage_suggested = PCR1_input_coverage * target_coverage_percentage
    max_reads = PCR1_input_coverage * guide_library_size * 5
    
    # Retrieve list of reads to pass into simulation then run simulation
    total_reads_targets_res = np.arange(max_reads/read_intervals_count, max_reads, max_reads/read_intervals_count).astype(int)

    simulate_gRNA_library_prep_p = partial(simulate_gRNA_library_prep, guide_library_size = guide_library_size, PCR1_input_ug = gDNA_amount, MOI = moi, perfection_rate=perfection_rate, genome_conc_ng=genome_conc_ng, plot=False)
    if cores == 1:
         guide_coverages_res = [simulate_gRNA_library_prep_p(_total_target_reads=total_reads) for total_reads in total_reads_targets_res]
    else:
        with multiprocessing.Pool(processes=cores) as pool:
            guide_coverages_res = pool.map(simulate_gRNA_library_prep_p, total_reads_targets_res)
            

    guide_coverages_res = [simulate_gRNA_library_prep(guide_library_size = guide_library_size, PCR1_input_ug = gDNA_amount, MOI = moi,
                                    _total_target_reads=int(total_reads), perfection_rate=perfection_rate, genome_conc_ng=genome_conc_ng, plot=False) for total_reads in total_reads_targets_res]
    
    # Get the reads for the target coverage
    get_target_coverage_linear_interop_p = partial(get_target_coverage_linear_interop, np.asarray(guide_coverages_res), np.asarray(total_reads_targets_res))

    target_read_amount_suggested = get_target_coverage_linear_interop_p(target_coverage=target_coverage_suggested)

    if target_coverage_input is not None:
        target_read_amount_input = get_target_coverage_linear_interop_p(target_coverage=target_coverage_input)
        if target_coverage_input > PCR1_input_coverage:
            target_read_amount_input=np.nan


    # Visualize
    fig, ax = plt.subplots()
    ax.scatter(total_reads_targets_res, guide_coverages_res)
    
    # Show coverage indicators
    ax.axhline(y=PCR1_input_coverage, color="blue", label=f"Maximum coverage: {PCR1_input_coverage:.2f}")
    ax.axhline(y=target_coverage_input, color="blue", linestyle="dashed", label=f"Desired coverage: {target_coverage_input:.2f}")
    ax.axhline(y=target_coverage_suggested, color="blue", linestyle="dotted", label=f"Suggested coverage: {target_coverage_suggested:.2f}")

    ax.axvline(x=target_read_amount_input, color="black", linestyle="dashed", label=f"For desired coverage {target_coverage_input:.2f}, target reads for coverage={target_read_amount_input:.2f}")
    ax.axvline(x=target_read_amount_suggested, color="black", linestyle="dotted", label=f"For suggested coverage {target_coverage_suggested:.2f}, target reads ={target_read_amount_suggested:.2f}")
    
    ax.set_xlabel("Total Reads Sequenced")
    ax.set_ylabel("Guide Coverage")
    ax.set_title(f"Sample={sample_name}\nGuide Coverage by Total Reads Sequence\ngDNA amount={gDNA_amount}, MOI={moi}")
    ax.set_ylim(0, PCR1_input_coverage + 20)
    ax.set_xlim(0, np.maximum(max_reads + (max_reads/10), target_read_amount_suggested + (target_read_amount_suggested/10)))
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

    return {
        "target_read_amount_suggested": target_read_amount_suggested, 
        "target_coverage_suggested": target_coverage_suggested, 
        "target_read_amount_desired": target_read_amount_input,
        "target_coverage_desired": target_coverage_input,
        "total_reads_targets_simulated_list": total_reads_targets_res,
        "guide_coverages_simulated_list": guide_coverages_res,
        "get_reads_for_desired_target_coverage_callable": get_target_coverage_linear_interop_p,
        "visualization_ax": ax
        }


@typechecked
def get_target_coverage_per_sample(ideal_gDNA_amount: Union[None, float], max_gDNA_amount: float, moi: float, sample_name:str, perfection_rate: float, guide_library_size:int, genome_conc_ng: float = _GENOME_CONC_NG, target_coverage_input=None, target_coverage_percentage: float=0.70, max_target_coverage_input: int = 600, read_intervals_count: int= 20, gDNA_intervals_count: int = 5, cores=1):
    print(f"Processing sample: {sample_name}")
    # Generate list of all gDNA ranges to test
    gDNA_amount_tests = np.arange(max_gDNA_amount/gDNA_intervals_count, max_gDNA_amount, max_gDNA_amount/gDNA_intervals_count)
    
    # Add the max gDNA and ideal gDNA amount
    gDNA_amount_tests = np.append(gDNA_amount_tests, max_gDNA_amount)
    if (ideal_gDNA_amount is not None) and (ideal_gDNA_amount not in gDNA_amount_tests):
        gDNA_amount_tests = np.append(gDNA_amount_tests, ideal_gDNA_amount)
    
    # Perform simulation for each gDNA test and visualize
    get_target_coverage_p = partial(get_target_coverage, moi=moi, sample_name=sample_name, perfection_rate=perfection_rate, guide_library_size=guide_library_size, genome_conc_ng=genome_conc_ng, target_coverage_input=target_coverage_input, target_coverage_percentage=target_coverage_percentage, read_intervals_count=read_intervals_count, cores=1)

    if cores == 1:
        print(gDNA_amount_tests)
        target_coverage_result_list = [get_target_coverage_p(gDNA_amount=gDNA_amount_test) for gDNA_amount_test in gDNA_amount_tests]
    else:
        with multiprocessing.Pool(processes=cores) as pool:
            target_coverage_result_list = pool.map(get_target_coverage_p, gDNA_amount_tests)
            
            for target_coverage_result in target_coverage_result_list:
                plt.show(target_coverage_result["visualization_ax"])
        
    target_coverage_suggested_list = [target_coverage_result["target_coverage_suggested"] for target_coverage_result in target_coverage_result_list]
    fig, ax = plt.subplots()
    ax.scatter(gDNA_amount_tests, target_coverage_suggested_list)
    ax.set_title(f"Sample={sample_name}\nGuide Coverage by Total Reads Sequence\nmax gDNA amount={max_gDNA_amount}, MOI={moi}")
    ax.set_xlabel("gDNA Amount (ug)")
    ax.set_ylabel("Suggested Target Coverage")
    plt.show()

    # Get result for the max gDNA available and the ideal gDNA desired
    max_gDNA_target_coverage_suggested_result = target_coverage_result_list[np.where(gDNA_amount_tests == max_gDNA_amount)[0][0]]
    ideal_gDNA_target_coverage_suggested_result = None
    if ideal_gDNA_amount is not None:
        ideal_gDNA_target_coverage_suggested_result = target_coverage_result_list[np.where(gDNA_amount_tests == ideal_gDNA_amount)[0][0]]

    # Get target gDNA to achieve the max sufficient coverage
    target_gDNA_for_max_coverage = get_target_coverage_linear_interop(np.asarray(target_coverage_suggested_list), np.asarray(gDNA_amount_tests), target_coverage=max_target_coverage_input)

    target_gDNA_target_coverage_result = None
    if target_gDNA_for_max_coverage > max_gDNA_amount:
            target_gDNA_for_max_coverage = np.nan
    else:
        target_gDNA_target_coverage_result = get_target_coverage_p(gDNA_amount=target_gDNA_for_max_coverage)

    # Provide a callable for getting gDNA given a desired suggested target coverage
    get_target_coverage_linear_interop_p = partial(get_target_coverage_linear_interop, np.asarray(target_coverage_suggested_list), np.asarray(gDNA_amount_tests))
    
    return {
        "target_gDNA_for_max_coverage_result": (target_gDNA_for_max_coverage, target_gDNA_target_coverage_result, max_target_coverage_input),
        "max_gDNA_target_coverage_suggested_result": (max_gDNA_amount, max_gDNA_target_coverage_suggested_result),
        "ideal_gDNA_target_coverage_suggested_result": (ideal_gDNA_amount, ideal_gDNA_target_coverage_suggested_result),
        "simulation_result": {
            "gDNA_amount_tests": gDNA_amount_tests,
            "target_coverage_suggested_list": target_coverage_suggested_list,
            "target_coverage_result_list": target_coverage_result_list,
        },
        "get_gDNA_for_suggested_target_coverage_callable": get_target_coverage_linear_interop_p,
        "get_target_coverage_for_gDNA_callable": get_target_coverage_p,
        "visualization_ax": ax
    }

def process_sample_sheet(sample_sheet: pd.DataFrame, target_coverage_percentage: float, max_target_coverage_input: float, suggested_target_coverage_amounts: List[Union[float, int]], cores=1):
    def process_row(row):
        return get_target_coverage_per_sample(
            ideal_gDNA_amount=None,
            max_gDNA_amount=row["gDNA_amount_ug"], 
            moi=row["moi"],
            sample_name=row["sample_name"],
            guide_library_size=row["guide_library_size"], 
            target_coverage_input=row["target_coverage_input"], 
            perfection_rate=row["perfection_rate"],
            target_coverage_percentage=target_coverage_percentage,
            max_target_coverage_input=max_target_coverage_input,
            cores=cores)
    result_dict_list = sample_sheet.apply(process_row, axis=1)


    # Prepare final results for each sample
    result_series_list = []
    for result_dict in result_dict_list:
        
        target_coverage_suggested_list = []
        target_read_amount_suggested_list = []
        gDNA_for_target_coverage_list = []
        for suggested_target_coverage_amount in suggested_target_coverage_amounts:
            gDNA_for_target_coverage = result_dict["get_gDNA_for_suggested_target_coverage_callable"](suggested_target_coverage_amount)
            
            target_coverage_result = result_dict["get_target_coverage_for_gDNA_callable"](gDNA_for_target_coverage)  
            
            target_coverage_suggested = target_coverage_result["target_coverage_suggested"]
            target_read_amount_suggested = target_coverage_result["target_read_amount_suggested"]

            target_coverage_suggested_list.append(target_coverage_suggested)
            target_read_amount_suggested_list.append(target_read_amount_suggested)
            gDNA_for_target_coverage_list.append(gDNA_for_target_coverage)

        
        added_values = []
        added_indices = []    
        for i in range(len(suggested_target_coverage_amounts)):
            added_values.extend([
                gDNA_for_target_coverage_list[i],
                target_coverage_suggested_list[i], 
                target_read_amount_suggested_list[i]])
            
            added_indices.extend([
                f"gDNA_for_suggested_target_coverage_{suggested_target_coverage_amounts[i]}",
                f"coverage_for_suggested_target_coverage_{suggested_target_coverage_amounts[i]}",
                f"reads_for_suggested_target_coverage_{suggested_target_coverage_amounts[i]}"])
        
        result_series_values = [
            f"{result_dict['target_gDNA_for_max_coverage_result'][0]:.2f}",
            f"{result_dict['target_gDNA_for_max_coverage_result'][1]['target_coverage_suggested']:.2f}" if result_dict['target_gDNA_for_max_coverage_result'][1] is not None else None,
            f"{result_dict['target_gDNA_for_max_coverage_result'][2]:.2f}",
            f"{result_dict['max_gDNA_target_coverage_suggested_result'][0]:.2f}",
            f"{result_dict['max_gDNA_target_coverage_suggested_result'][1]['target_coverage_suggested']:.2f}" if result_dict['max_gDNA_target_coverage_suggested_result'][1] is not None else None,
            f"{result_dict['ideal_gDNA_target_coverage_suggested_result'][0]:.2f}" if result_dict['ideal_gDNA_target_coverage_suggested_result'][0] is not None else None,
            f"{result_dict['ideal_gDNA_target_coverage_suggested_result'][1]['target_coverage_suggested']:.2f}" if result_dict['ideal_gDNA_target_coverage_suggested_result'][1] is not None else None,
        ]
        result_series_values.extend(added_values)
        

        result_series_indices = ["target_gDNA_for_max_coverage", "target_gDNA_target_coverage_suggested", "max_target_coverage_input", 
        "max_gDNA_amount", "max_gDNA_target_coverage_suggested", 
        "ideal_gDNA_amount", "ideal_gDNA_target_coverage_suggested"]
        result_series_indices.extend(added_indices)

        result_series = pd.Series(result_series_values, index=result_series_indices)
        result_series_list.append(result_series)

    # Add sample results to the sample_sheet
    result_df = pd.DataFrame(result_series_list)
    sample_sheet_with_results = sample_sheet.copy()
    sample_sheet_with_results = pd.concat([sample_sheet_with_results, result_df], axis=1)


    return {
        "result_dict_list": result_dict_list,
        "sample_sheet_with_results": sample_sheet_with_results
    }