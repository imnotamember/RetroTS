__author__ = 'Joshua Zosky'

import numpy # delete this and replace with specific functions
from numpy import nonzero, add, subtract, divide, mean, zeros
from scipy.signal import firwin, lfilter
from scipy.interpolate import interp1d
from pylab import plot, subplot, show, text, style, figure
from zscale import z_scale


def rvt_from_peakfinder(r):
    if r['demo']:
        quiet = 0
        print "quiet = %s" % quiet
    # Calculate RVT
    if len(r['p_trace']) != len(r['n_trace']):
        dd = abs(len(r['p_trace']) - len(r['n_trace']))
        if dd > 1:  # have not seen this yet, trap for it.
            print 'Error RVT_from_PeakFinder:\nPeak trace lengths differ by %d\nThis is unusual, please upload data' \
                  '\nsample to afni.nimh.nih.gov' % dd
            # keyboard
            return
        else:  # just a difference of 1, happens sometimes, seems ok to discard one sample
            print 'Notice RVT_from_PeakFinder:\nPeak trace lengths differ by %d\nClipping longer trace.' % dd
            dm = min(len(r['p_trace']), len(r['p_trace']))
            if len(r['p_trace']) != dm: 
               r['p_trace'] = r['p_trace'][0:dm]
               r['tp_trace'] = r['tp_trace'][0:dm]
            else:
               r['n_trace'] = r['n_trace'][0:dm]
               r['tn_trace'] = r['tn_trace'][0:dm]
    
    r['rv'] = subtract(r['p_trace'], r['n_trace'])
    # NEED TO consider which starts first and
    # whether to initialize first two values by means
    # and also, what to do when we are left with one 
    # incomplete pair at the end

    nptrc = len(r['tp_trace'])
    r['rvt'] = r['rv'][0:nptrc - 1] / r['prd']
    if r['p_trace_r'].any:
        r['rvr'] = subtract(r['p_trace_r'], r['n_trace_r'])
        r['rvtr'] = numpy.ndarray(numpy.shape(r['rvr']))
        divide(r['rvr'], r['prdR'], r['rvtr'])
        # Smooth RVT so that we can resample it at volume_tr later
        fnyq = r['phys_fs'] / 2             # nyquist of physio signal
        fcut = 2 / r['volume_tr']           # cut below nyquist for volume_tr
        w = float(r['frequency_cutoff']) / float(fnyq)     # cut off frequency normalized
        b = firwin(numtaps=(r['fir_order'] + 1), cutoff=w, window='hamming')
        v = r['rvtr']
        mv = mean(v)
        # remove the mean
        v = (v - mv)
        # filter both ways to cancel phase shift
        v = lfilter(b, 1, v)
        # v = numpy.flipud(v)  # Turns out these don't do anything in the MATLAB version(Might be a major problem)
        v = lfilter(b, 1, v)
        # v = numpy.flipud(v)  # Turns out these don't do anything in the MATLAB version(Might be a major problem)
        r['rvtrs'] = v + mv

    # create RVT regressors
    r['rvtrs_slc'] = zeros((len(r['rvt_shifts']), len(r['time_series_time'])))
    for i in range(0, len(r['rvt_shifts'])):
        shf = r['rvt_shifts'][i]
        nsamp = int(round(shf * r['phys_fs']))
        sind = add(range(0, len(r['t'])), nsamp)
        print sind
        sind[nonzero(sind < 0)] = 0
        sind[nonzero(sind > (len(r['t']) - 1))] = len(r['t']) - 1
        rvt_shf = interp1d(r['t'], r['rvtrs'][sind], r['interpolation_style'], bounds_error=False)
        rvt_shf_y = rvt_shf(r['time_series_time'])
        r['rvtrs_slc'][:][i] = rvt_shf_y

    if r['quiet'] == 0 and r['show_graphs'] == 1:
        print '--> Calculated RVT \n--> Created RVT regressors'
        subplot(211)
        plot(r['t_mid_prd'], z_scale(r['rvt'], min(r['p_trace']), max(r['p_trace'])), 'k')
        if any(r['p_trace_r']):
            plot(r['tR'], z_scale(r['rvtrs'], min(r['p_trace']), max(r['p_trace'])), 'm')
        show()
        if r['demo']:
            # uiwait(msgbox('Press button to resume', 'Pausing', 'modal'))
            pass

    return r
