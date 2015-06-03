__author__ = 'Joshua Zosky'

from numpy import zeros
from PeakFinder import peak_finder


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
            ShowGraphs = 1
            ):
    SliceOffset = zeros(0)
    '''
    # Create option copy for each type of signal
    OptR = Opt
    OptR.fcutoff = Opt.RespCutoffFreq;
    OptR.AmpPhase = 1;   %amplitude based phase for respiration
    %OptR.as_percover = 50; %percent overlap of windows for fft
    %OptR.as_windwidth = 0; %window width in seconds for fft, 0 for full window
    %OptR.as_fftwin = 0 ; %1 == hamming window. 0 == no windowing
    OptE = Opt;
    OptE.fcutoff = Opt.CardCutoffFreq;
    OptE.AmpPhase = 0;   %time based phase for cardiac signal
    '''
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
    print respiration_peak.keys()
    print cardiac_peak.keys()
    return