# coding=utf-8
__author__ = 'Joshua Zosky'

from numpy import zeros, savetxt, size
from PeakFinder import peak_finder
from PhaseEstimator import phase_estimator
from RVT_from_PeakFinder import rvt_from_peakfinder


def retro_ts(respiration_file,cardiac_file,phys_fs, number_of_slices, volume_tr,
             prefix = 'Output_File_Name',
             slice_offset = 0,
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
    :param number_of_slices:
    :param volume_tr:
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
        slice_offset = zeros((number_of_slices, 1))
    main_info = {'respiration_file': respiration_file,
                 'cardiac_file': cardiac_file,
                 'phys_fs': phys_fs,
                 'number_of_slices': number_of_slices,
                 'volume_tr': volume_tr,
                 'prefix': prefix,
                 'slice_offset': slice_offset,
                 'rvt_shifts': rvt_shifts,
                 'respiration_cutoff_frequency': respiration_cutoff_frequency,
                 'cardiac_cutoff_frequency': cardiac_cutoff_frequency,
                 'interpolation_style': interpolation_style,  # replacement for 'ResamKernel' variable name
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
    respiration_info = main_info
    # Amplitude-based phase for respiration
    respiration_info['amp_phase'] = 1
    # respiration_info['as_percover'] = 50  # Percent overlap of windows for fft
    # respiration_info['as_windwidth'] = 0  # Window width in seconds for fft, 0 for full window
    # respiration_info['as_fftwin'] = 0     # 1 == hamming window. 0 == no windowing
    cardiac_info = main_info
    # Time-based phase for cardiac signal
    cardiac_info['amp_phase'] = 0

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

    main_info['resp_peak'] = respiration_peak
    main_info['card_peak'] = cardiac_peak
    respiration_info.update(respiration_peak)
    cardiac_info.update(cardiac_peak)

    # Get the phase
    if respiration_peak:
        print 'Estimating phase for R'
        respiration_phased = phase_estimator(respiration_info['amp_phase'], respiration_info)
        #return respiration_phased
    else:
        respiration_phased = {}
    if cardiac_peak:
        print 'Estimating phase for E'
        print cardiac_info['v']
        cardiac_phased = phase_estimator(cardiac_info['amp_phase'], cardiac_info)
        #return cardiac_phased
    else:
        cardiac_phased = {}

    respiration_info.update(respiration_phased)
    cardiac_info.update(cardiac_phased)

    if respiration_phased:
        print "Computing RVT from peaks"
        print respiration_info['p_trace_r']
        rvt = rvt_from_peakfinder(respiration_phased)

    respiration_info.update(rvt)

    return respiration_info
    """
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