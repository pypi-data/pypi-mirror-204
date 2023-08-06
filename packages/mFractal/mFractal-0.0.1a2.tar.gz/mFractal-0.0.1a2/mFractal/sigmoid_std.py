import numpy as np

def sigmoid_std(Timeseries, v = 1):
    """Run LEiDA Routine for BOLD signal.
    Args:

        Timeseries (ndarray): Signal vector. This function assumes that your time series 
        v (double): 
    Returns:

        sigma (ndarray): Standardised signal vector.


    References
    ----------
    .. [1] 
    França, L. G. S. et al. (2018) ‘Fractal and Multifractal Properties 
    of Electrographic Recordings of Human Brain Activity: Toward Its Use 
    as a Signal Feature for Machine Learning in Clinical Applications’, 
    Frontiers in Physiology, 9(December), pp. 1–18. 
    doi: 10.3389/fphys.2018.01767.
    
    """
    x = (Timeseries - np.mean(Timeseries))/np.std(Timeseries)
    sigma = np.divide(1, 1 + np.exp(-v*x))

    return sigma
