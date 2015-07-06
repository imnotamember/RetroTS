__author__ = 'Joshua'
'''
import PeakFinder as pf

a, b = pf.peak_finder(var_vector='Resp_epiRT_scan_14.dat',
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

c, d = pf.peak_finder(var_vector='ECG_epiRT_scan_14.dat',
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

for key, item in a.items():
    print "%s = %s" % (key, item)
for key, item in c.items():
    print "%s = %s" % (key, item)
'''

import RetroTS as rts

a = rts.retro_ts(respiration_file='Resp_epiRT_scan_14.dat',
                 cardiac_file='ECG_epiRT_scan_14.dat',
                 phys_fs=50,
                 number_of_slices=20,
                 volume_tr=2,
                 show_graphs=1,
                 quiet=0
                 )
# print a.keys()
# for key in a.keys():
#     print key
#     print a[key]

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
'''
def sf(a, b):
    if not kwargs:
        kwargs['a='] = 'm'
        kwargs['b='] = 13424
    for key, value in kwargs.iteritems():
        print key, value

s = {'d': 1, 'c': 'asdf', 'a': 'asdfjkl;', 'b': 23458098}
sf(**s)
#sf()
'''
'''
import zscale as z
import numpy

x = open('xfile.txt', 'r').read().splitlines()
for i in range(len(x)):
    x[i] = float(x[i])
print x
y = z.z_scale(x, 0, 2412.205169368427)#, [2, 98])
#y = numpy.clip(x, -604.581412763125, 2412.205169368427)
print y

from PhaseEstimator import phase_base
from RVT_from_PeakFinder import rvt_from_peakfinder

v = open('v.txt', 'r').read().splitlines()
for i in range(len(v)):
    v[i] = float(v[i])
print v
ptrace = open('ptrace.txt', 'r').read().splitlines()
for i in range(len(ptrace)):
    ptrace[i] = float(ptrace[i])
print ptrace
ntrace = open('ntrace.txt', 'r').read().splitlines()
for i in range(len(ntrace)):
    ntrace[i] = float(ntrace[i])
tptrace = open('tptrace.txt', 'r').read().splitlines()
for i in range(len(tptrace)):
    tptrace[i] = float(tptrace[i])
tntrace = open('tntrace.txt', 'r').read().splitlines()
for i in range(len(tntrace)):
    tntrace[i] = float(tntrace[i])
prd = open('prd.txt', 'r').read().splitlines()
for i in range(len(prd)):
    prd[i] = float(prd[i])
prdR = open('prdR.txt', 'r').read().splitlines()
for i in range(len(prdR)):
    prdR[i] = float(prdR[i])
tmidprd = open('tmidprd.txt', 'r').read().splitlines()
for i in range(len(tmidprd)):
    tmidprd[i] = float(tmidprd[i])
ptraceR = open('ptraceR.txt', 'r').read().splitlines()
for i in range(len(ptraceR)):
    ptraceR[i] = float(ptraceR[i])
ntraceR = open('ntraceR.txt', 'r').read().splitlines()
for i in range(len(ntraceR)):
    ntraceR[i] = float(ntraceR[i])

t = numpy.arange(0, 12019)
t = [float(i) for i in range(len(t))]
for i in range(len(t)):
    t[i] = float(t[i]) / 50.0
sliceoffset = [0,
1.00000000000000,
0.100000000000000,
1.10000000000000,
0.200000000000000,
1.20000000000000,
0.300000000000000,
1.30000000000000,
0.400000000000000,
1.40000000000000,
0.500000000000000,
1.50000000000000,
0.600000000000000,
1.60000000000000,
0.700000000000000,
1.70000000000000,
0.800000000000000,
1.80000000000000,
0.900000000000000,
1.90000000000000]
phasee = {'v': v,
          'p_trace': ptrace,
          'n_trace': ntrace,
          'p_traceR': ptraceR,
          'n_traceR': ntraceR,
          't': t,
          'tR': t,
          'tp_trace': tptrace,
          'tn_trace': tntrace,
          'show_graphs': 1,
          'phase': [],
          'phase_pol': [],
          'volume_tr': 2,
          'number_of_slices': 20,
          'slice_offset':sliceoffset,
          'quiet': 0,
          'prd': prd,
          'prdR': prdR,
          'tmidprd': tmidprd,
          'v_name': '.\Resp_epiRT_scan_14.dat'
          }
opt = {'phys_fs': (1 / 0.025),
       'zero_phase_offset': 0.5,
       'quiet': 0,
       'resample_fs': (1 / 0.025),
       'f_cutoff': 10,
       'fir_order': 80,
       'volume_TR': 2,
       'RVTshifts': [0,5,10,15,20],
       'ResamKernel': 'linear',
       'ShowGraphs': 1,
       'Demo': 0
       }
a = phase_base(0, phasee)
rvt_from_peakfinder(a, opt)
'''