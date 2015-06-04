__author__ = 'Joshua Zosky'

from numpy import zeros
from PeakFinder import peak_finder
from PhaseEstimator import phase_estimator


def retro_ts(respiration_file,cardiac_file,PhysFS, Nslices, VolTR,
            Prefix = 'Output_File_Name',
            SliceOffset = [],#figure this default out - needs to be a matrix of 0's based on Nslices
            RVTshifts = range(0, 20, 5),
            RespCutoffFreq = 3,
            CardCutoffFreq = 3,
            ResamKernel = 'linear',
            FIROrder = 40,
            Quiet = 1,
            Demo = 0,
            RVT_out = 0,
            Card_out = 0,
            Resp_out = 0,
            SliceOrder = 'alt+z',
            show_graphs = 1
            ):
    SliceOffset = zeros(0)
    main_info = {}

    # Create information copy for each type of signal
    respiration_info = main_info
    respiration_info['frequency_cutoff'] = main_info['respiration_cutoff_frequency']
    # Amplitude-based phase for respiration
    respiration_info['amp_phase'] = 1
    # respiration_info['as_percover'] = 50  # Percent overlap of windows for fft
    # respiration_info['as_windwidth'] = 0  # Window width in seconds for fft, 0 for full window
    # respiration_info['as_fftwin'] = 0     # 1 == hamming window. 0 == no windowing
    cardiac_info = main_info
    cardiac_info['frequency_cutoff'] = main_info['cardiac_cutoff_frequency']
    # Time-based phase for cardiac signal
    cardiac_info['AmpPhase'] = 0

    # Get the peaks for R and E
    if respiration_file:
        respiration_peak, error = peak_finder(respiration_file)
        if error:
            print 'Died in PeakFinder'
            return
    else:
        respiration_peak = {}
    if cardiac_file:
        cardiac_peak, error = peak_finder(cardiac_file)
        if error:
            print 'Died in PeakFinder'
            return
    else:
        cardiac_peak = {}

    # Get the phase
    if respiration_peak == {}:
        print 'Estimating phase for R'
        respiration_phased = phase_estimator(**respiration_peak, **respiration_info)
    if cardiac_peak == {}:
        print 'Estimating phase for E'
        cardiac_phased = phase_estimator(**cardiac_peak, **cardiac_info)
