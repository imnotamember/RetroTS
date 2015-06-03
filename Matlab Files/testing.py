__author__ = 'Joshua'
'''
import PeakFinder as pf
a = pf.peak_finder(var_vector='Resp_epiRT_scan_14.dat',
                   phys_fs=50,
                   zero_phase_offset=0,
                   quiet=0,
                   resample_fs=50,
                   f_cutoff=3,
                   fir_order=40,
                   resample_kernel='linear',
                   demo=0,
                   as_window_width=0,
                   as_percover=0,
                   as_fftwin=0,
                   sep_dups=0)
print a
b = pf.peak_finder(var_vector='ECG_epiRT_scan_14.dat',
                   phys_fs=50,
                   zero_phase_offset=0,
                   quiet=0,
                   resample_fs=50,
                   f_cutoff=3,
                   fir_order=40,
                   resample_kernel='linear',
                   demo=0,
                   as_window_width=0,
                   as_percover=0,
                   as_fftwin=0,
                   sep_dups=0)
print b
'''
import RetroTS as rts

rts.retro_ts(respiration_file='Resp_epiRT_scan_14.dat',
             cardiac_file='ECG_epiRT_scan_14.dat',
             PhysFS=50,
             Nslices=20,
             VolTR=2)
'''
for i in a:
    print '%s' i
    print '======\n%s\n======' % a[i]
'''
######missing v from peakfinder(probably v_np)
#### all trace arrays have value 0 same as value 1
### p_trace_R is high and doesn't change at 50, it changes at 244!
### n_trace_R is high and doesn't change at 5, it changes at 161!
### prdR is whacky
