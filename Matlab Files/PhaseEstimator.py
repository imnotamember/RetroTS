__author__ = 'Joshua Zosky'

from numpy import ones, nonzero, pi
from numpy import size


def phase_base(amp_type, phasee):
    """
    
    :param amp_type:    if 0, it is a time-based phase estimation
                        if 1, it is an amplitude-based phase estimation
    :param phasee: phasee information
    :return:
    """
    if amp_type = 1:
        # Calculate the phase of the trace, with the peak to be the start of the phase
        nptrc = len(phasee['tp_trace'])
        phasee['phase'] = -2 * ones(size(phasee['t']))
        i=0
        j=0
        while i <= (nptrc-1):
            while phasee['t'][j] < phasee['tp_trace'][i+1]:
                if phasee['t'][j] >= phasee['tp_trace'][i]:
                    # Note: Using a constant 244 period for each interval
                    # causes slope discontinuity within a period.
                    # One should resample period[i] so that it is
                    # estimated at each time in phasee['t'][j],
                    # dunno if that makes much of a difference in the end however.
                    phasee['phase'][j] = phasee['t'][j] - phasee['tp_trace'][i] / phasee['prd'][i]\
                                         + phasee['zero_phase_offset']
                    if phasee.phase[j] < 0:
                        phasee['phase'][j] = -phasee['phase'][j]
                    if phasee.phase[j] > 1:
                        phasee['phase'][j] -= 1
                j += 1
            i += 1

            # Remove the points flagged as unset
            temp = nonzero(phasee['phase']<-1)
            phasee['phase'][temp]  = 0.0
            # Change phase to radians
            phasee['phase'] = phasee['phase'] * 2. * pi
    else: # phase based on amplitude
        # at first scale to the max
        mxamp = max(phasee['p_trace'])
        gR = zscale(phasee['v'], mxamp, 0) # Scale, per Glover 2000's paper
        bins = [1:1:100]./100 * mxamp
        [hb,bbins] = hist(gR, bins)
        if show_graphs:
            bar (bins, hb)
        #find the polarity of each time point in v
        i = 1 itp = 1 inp = 1
        while (  i <= length(phasee['v']) & ...
            phasee['t'](i) < phasee['tp_trace'](1) & ...
            phasee['t'](i) < phasee['tn_trace'](1) ),
        phasee['phase_pol'](i) = 0
        i = i + 1
        if (phasee['tp_trace'](1) < phasee['tn_trace'](1)), 
            cpol=-1    #expiring phase, peak behind us
            itp = 2
         else:
         cpol = 1 #inspiring phase (bottom behind us)
         inp = 2
      end
      phasee['phase_pol'] = zeros(size(phasee['v']))
      #add a fake point to tptrace and tntrace to avoid ugly if statements
      phasee['tp_trace'] = [phasee['tp_trace'] phasee['t'](end)]
      phasee['tn_trace'] = [phasee['tn_trace'] phasee['t'](end)]
      while(i <= length(phasee['v'])),
         phasee['phase_pol'](i) = cpol
         if (phasee['t'](i) == phasee['tp_trace'](itp)),
            cpol = -1 itp = min([itp+1, length(phasee['tp_trace'])])
         elseif (phasee['t'](i) == phasee['tn_trace'](inp)),
            cpol = +1 inp = min([inp+1, length(phasee['tn_trace'])])
         end
         #cpol, inp, itp, i, R
         i = i + 1
      end
      phasee['tp_trace'] = [phasee['tp_trace'](1:end-1)]
      phasee['tn_trace'] = [phasee['tn_trace'](1:end-1)]
        if show_graphs:
          clf
          plot (phasee['t'], gR,'b') hold on
          ip = find(phasee['phase_pol']>0)
          plot (phasee['t'](ip), 0.55 * mxamp,'r.')
          in = find(phasee['phase_pol']<0)
          plot (phasee['t'](in),0.45 * mxamp,'g.')
      end
      #Now that we have the polarity, without computing sign(dR/dt) 
      # as in Glover et al 2000, calculate the phase per eq. 3 of that paper
      #first the sum in the numerator
      gR = round(gR/mxamp * 100)+1 gR(find(gR>100))=100
      shb = sum(hb)
      hbsum = zeros(1,100)
      hbsum(1)=hb(1)./shb
      for (i=2:1:100),
         hbsum(i) = hbsum(i-1)+hb(i)./shb
      end
      for(i=1:1:length(phasee['t'])),
         phasee['phase'](i) = pi * hbsum(round(gR(i))) * phasee['phase_pol'](i)
        pass

def phase_estimator(v_name='',
                    t=[],
                    x=[],
                    iz=[],   # zero crossing (peak) locations
                    p_trace=[],
                    tp_trace=[],
                    n_trace=[],
                    tn_trace=[],
                    prd=[],
                    t_mid_prd=[],
                    p_trace_mid_prd=[],
                    phase=[],
                    RV=[],
                    RVT=[],
                    var_vector,
                    phys_fs=(1 / 0.025),
                    zero_phase_offset=0.5,
                    quiet=0,
                    resample_fs=(1 / 0.025),
                    f_cutoff=10,
                    fir_order=80,
                    resample_kernel='linear',
                    demo=0,
                    as_window_width=0,
                    as_percover=0,
                    as_fftwin=0,
                    sep_dups=0,
                    phasee_list=0,
                    show_graphs=0
                    ):
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
    :param frequency_cutoff:
    :param fir_order: BC ???
    :param resample_kernel:
    :param demo:
    :param as_window_width:
    :param as_percover:
    :param fftwin:
    :param sep_dups:
    :return: *_phased: phase estimation of input signal
    """
    if type(phasee_list) is type([]):
        for phasee_column in phasee_list:
            phase_base(more_info['amp_phase'], phasee_column)
    else:
        phase_base(more_info, phasee)
    