__author__ = 'Joshua'

import PeakFinder as pf
pf.peak_finder(var_vector='Resp_epiRT_scan_14.dat',
               phys_fs=50,
               zero_phase_offset=0,
               quiet=1,
               resample_fs=50,
               f_cutoff=3,
               fir_order=40,
               resample_kernel='linear',
               demo=0,as_window_width=0,
               as_percover=0,
               as_fftwin=0,
               sep_dups=0)

