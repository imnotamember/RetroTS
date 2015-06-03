__author__ = 'Joshua Zosky'


def phase_estimator(**kwargs, **kwargs):
    """
    Example: PhaseEstimator.phase_estimator(respiration_peak, )
    or PhaseEstimator.phase_estimator(v) where v is a column vector
    if v is a matrix, each column is processed separately.
    :param var_vector: column vector--list of list(s)
    :param phys_fs: Sampling frequency
    :param zero_phase_offset: Fraction of the period that corresponds to a phase of 0
                                0.5 means the middle of the period, 0 means the 1st peak
    :param quiet:
    :param resample_fs:
    :param f_cutoff:
    :param fir_order: BC ???
    :param resample_kernel:
    :param demo:
    :param as_window_width:
    :param as_percover:
    :param fftwin:
    :param sep_dups:
    :return: [r, e] r = Peak of var_vector; e = error value
    """
    if amp_phase:
       for (icol=1:1:length(R)),
          %Calculate the phase of the trace, with the peak
          %to be the start of the phase
          nptrc = length(R(icol).tptrace);
          R(icol).phz=-2.*ones(size(R(icol).t));
          i=1;
          j=1;