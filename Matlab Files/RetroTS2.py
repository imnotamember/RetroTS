# coding=utf-8
__author__ = 'Joshua Zosky'

from numpy import zeros, savetxt, size
from PeakFinder import peak_finder
from PhaseEstimator import phase_estimator
from RVT_from_PeakFinder import rvt_from_peakfinder


def retro_ts(respiration_file,cardiac_file,phys_fs, n_slices, vol_tr,
             prefix = 'Output_File_Name',
             slice_offset = 0,  #figure this default out - needs to be a matrix of 0's based on Nslices
             rvt_shifts = range(0, 20, 5),
             respiration_cutoff_frequency = 3,
             cardiac_cutoff_frequency = 3,
             interpolation_style = 'linear',
             fir_order = 40,
             quiet = 1,
             demo = 0,
             rvt_out = 0,
             cardiac_out = 0,
             respiration_out = 0,
             slice_order = 'alt+z',
             show_graphs = 1
             ):
    """
    
    :param respiration_file: 
    :param cardiac_file: 
    :param phys_fs: 
    :param n_slices: 
    :param vol_tr: 
    :param prefix: 
    :param slice_offset: 
    :param rvt_shifts: 
    :param respiration_cutoff_frequency: 
    :param cardiac_cutoff_frequency: 
    :param interpolation_style: kind : str or int, optional
        Specifies the kind of interpolation as a string:
            ‘linear’, ‘nearest’, ‘zero’, 'slinear', ‘quadratic, ‘cubic’
            Where 'slinear', ‘quadratic’ and ‘cubic’ refer to a spline interpolation
            of first, second or third order
        Or as an integer specifying the order of the spline interpolator to use. Default is ‘linear’.
    :param fir_order: 
    :param quiet: 
    :param demo:
    :param rvt_out:
    :param cardiac_out:
    :param respiration_out:
    :param slice_order:
    :param show_graphs: 
    :return:
    """
    if not slice_offset:
        slice_offset = zeros((n_slices, 1))
    main_info = {'respiration_file': respiration_file,
                 'cardiac_file': cardiac_file,
                 'phys_fs': phys_fs,
                 'n_slices': n_slices,
                 'vol_tr': vol_tr,
                 'prefix': prefix,
                 'slice_offset': slice_offset,
                 'rvt_shifts': rvt_shifts,
                 'respiration_cutoff_frequency': respiration_cutoff_frequency,
                 'cardiac_cutoff_frequency': cardiac_cutoff_frequency,
                 'interpolation_style': interpolation_style,
                 'fir_order': fir_order,
                 'quiet': quiet,
                 'demo': demo,
                 'rvt_out': rvt_out,
                 'cardiac_out': cardiac_out,
                 'respiration_out': respiration_out,
                 'slice_order': slice_order,
                 'show_graphs': show_graphs
                 }

    # Create information copy for each type of signal
    #   as_percover = Percent overlap of windows for fft
    #   as_windwidth = Window width in seconds for fft, 0 for full window
    #   as_fftwin = 1 => hamming window. 0 => no windowing

    respiration_info = dict(phys_fs=phys_fs, zero_phase_offset=0, quiet=quiet, resample_fs=phys_fs,
                            frequency_cutoff=respiration_cutoff_frequency, fir_order=fir_order,
                            interpolation_style=interpolation_style, demo=demo, as_window_width=0, as_percover=0,
                            as_fftwin=0, sep_dups=0)
    cardiac_info = dict(phys_fs=phys_fs, zero_phase_offset=0, quiet=quiet, resample_fs=phys_fs,
                            frequency_cutoff=cardiac_cutoff_frequency, fir_order=fir_order,
                            interpolation_style=interpolation_style, demo=demo, as_window_width=0, as_percover=0,
                            as_fftwin=0, sep_dups=0)

    # Get the peaks for R and E
    if respiration_file:
        respiration_info['var_vector'] = respiration_file
        respiration_peak, error = peak_finder(**respiration_info)
        if error:
            print 'Died in PeakFinder'
            return
        else:
            respiration_info.update(respiration_peak)
    else:
        respiration_peak = {}
    if cardiac_file:
        cardiac_info['var_vector'] = cardiac_file
        cardiac_peak, error = peak_finder(**cardiac_info)
        if error:
            print 'Died in PeakFinder'
            return
    else:
        cardiac_peak = {}

    main_info['resp_peak'] = respiration_peak
    main_info['card_peak'] = cardiac_peak
    return respiration_info
    """
    # amp_phase:    1 => Amplitude-based phase for respiration.
    #               0 => Time-based phase for cardiac signal
    respiration_peak['amp_phase'] = 1
    cardiac_peak['amp_phase'] = 0

    # prd
    # n_trace_R
    # iz
    # tn_trace
    # t_mid_prd
    # tR
    # prdR
    # p_trace
    # phase
    # v_name
    # p_trace_mid_prd
    # p_trace_R
    # RV
    # n_trace
    # tp_trace
    # t
    # RVT
    # x

    # Get the phase
    if respiration_peak:
        print 'Estimating phase for R'

        respiration_phased = phase_estimator(**respiration_peak, **respiration_info)
    if cardiac_peak:
        print 'Estimating phase for E'
        cardiac_phased = phase_estimator(**cardiac_peak, **cardiac_info)

    if respiration_phased:
        print "Computing RVT from peaks"
        rvt =  rvt_from_peakfinder(respiration_phased)

    return main_info

    # Show RVT graphs goes here, currently not important though

    if 0:
        # Write retroicor regressors
        for i in range(0, opt['Nslices']):
            fname = '%s.RetroCard.slc%02d.1D' % (opt['Prefix'], i)
            #wryte3(cardiac_phased['phz_slc_reg'][:,:,i], fname, 1);
            savetxt(fname, cardiac_phased['phz_slc_reg'][:,:,i], fmt="%12.6G")
            fname = sprintf('%s.RetroResp.slc%02d.1D', Opt.Prefix, i);
            # wryte3(R.phz_slc_reg(:,:,i), fname, 1);
            savetxt(fname, respiration_phased['phz_slc_reg'][:,:,i], fmt="%12.6G")

        # And write the RVT puppy, plus or minus a few seconds delay
        fname = '%s.RetroRVT.1D' % opt['Prefix']
        # wryte3(R.RVTRS_slc, fname, 1);
        savetxt(fname, rvt['RVTRS_slc'], fmt="%12.6G")

    # also generate files as 3dREMLfit likes them
    nn = 0
    nRv = 0
    nRp = 0
    nE = 0
    if not r:
        nn = len(rvt['time_series_time'])
        nRp = size(respiration_phased['phz_slc_reg'],1)
        nRv = size(rvt['RVTRS_slc'],1)

    if not e: # must have E
        nn = len(cardiac_phased['time_series_time']) # ok to overwrite len(R.tst), should be same.
        nE = size(cardiac_phased['phz_slc_reg'], 1)


    if not Opt.Card_out and not Opt.Resp_out not Opt.RVT_out:
        print 'Options Card_out, Resp_out, and RVT_out all 0.\nNo output required.\n'
        return

    Opt.RemlOut = zeros(nn, Opt.Nslices .* ((Opt.RVT_out != 0) .* nRv + (Opt.Resp_out != 0) .* nRp + (Opt.Card_out != 0) .* nE))
    cnt = 0
    head = '# <RetroTSout\n# ni_type = "%d*double"\n# ni_dimen = "%d"\n# ColumnLabels = "' % (size(Opt.RemlOut,2), size(Opt.RemlOut,1))
    tail = '"\n# >\n'
    tailclose = '# </RetroTSout>\n'

    label = head
    """