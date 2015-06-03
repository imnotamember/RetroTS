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
