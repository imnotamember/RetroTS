# coding=utf-8
__author__ = 'Joshua Zosky'

from numpy import zeros, size, savetxt, column_stack, shape
from PeakFinder import peak_finder
from PhaseEstimator import phase_estimator
from RVT_from_PeakFinder import rvt_from_peakfinder


def retro_ts(respiration_file, cardiac_file, phys_fs, number_of_slices, volume_tr,
             prefix='Output_File_Name',
             slice_offset=0,
             slice_major=1,
             rvt_shifts=range(0, 21, 5),
             respiration_cutoff_frequency=3,
             cardiac_cutoff_frequency=3,
             interpolation_style='linear',
             fir_order=40,
             quiet=1,
             demo=0,
             rvt_out=1,
             cardiac_out=1,
             respiration_out=1,
             slice_order='alt+z',
             show_graphs=0
             ):
    """
    
    :param respiration_file: 
    :param cardiac_file: 
    :param phys_fs: 
    :param number_of_slices:
    :param volume_tr:
    :param prefix: 
    :param slice_offset:
    :param slice_major:
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
                 'slice_major': slice_major,
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
    respiration_info = dict(main_info)
    # Amplitude-based phase for respiration
    respiration_info['amp_phase'] = 1
    # respiration_info['as_percover'] = 50  # Percent overlap of windows for fft
    # respiration_info['as_windwidth'] = 0  # Window width in seconds for fft, 0 for full window
    # respiration_info['as_fftwin'] = 0     # 1 == hamming window. 0 == no windowing
    cardiac_info = dict(main_info)
    # Time-based phase for cardiac signal
    cardiac_info['amp_phase'] = 0

    # Get the peaks for respiration_info and cardiac_info
    if respiration_file:
        respiration_peak, error = peak_finder(respiration_info, respiration_file)
        if error:
            print 'Died in PeakFinder'
            return
    else:
        respiration_peak = {}
    if cardiac_file:
        cardiac_peak, error = peak_finder(cardiac_info, cardiac_file)
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
        print 'Estimating phase for respiration_info'
        respiration_phased = phase_estimator(respiration_info['amp_phase'], respiration_info)
    else:
        respiration_phased = {}
    if cardiac_peak:
        print 'Estimating phase for cardiac_info'
        print cardiac_info['v']
        cardiac_phased = phase_estimator(cardiac_info['amp_phase'], cardiac_info)
    else:
        cardiac_phased = {}

    respiration_info.update(respiration_phased)
    cardiac_info.update(cardiac_phased)

    if respiration_phased:
        print "Computing RVT from peaks"
        print respiration_info['p_trace_r']
        rvt = rvt_from_peakfinder(respiration_phased)

    respiration_info.update(rvt)


    """
    # Not sure if this code is necessary, 'if 0' is never run in MATLAB
    # Show RVT graphs goes here, currently not important though

    if 0:
        # Write retroicor regressors
        for i in range(0, opt['Nslices']):
            fname = '%s.RetroCard.slc%02d.1D' % (opt['Prefix'], i)
            #wryte3(cardiac_phased['phase_slice_reg'][:,:,i], fname, 1);
            savetxt(fname, cardiac_phased['phase_slice_reg'][:,:,i], fmt="%12.6G")
            fname = sprintf('%s.RetroResp.slc%02d.1D', Opt.Prefix, i);
            # wryte3(respiration_info.phase_slice_reg(:,:,i), fname, 1);
            savetxt(fname, respiration_phased['phase_slice_reg'][:,:,i], fmt="%12.6G")

        # And write the RVT puppy, plus or minus a few seconds delay
        fname = '%s.RetroRVT.1D' % opt['Prefix']
        # wryte3(respiration_info.rvtrs_slc, fname, 1);
        savetxt(fname, rvt['rvtrs_slc'], fmt="%12.6G")
    """
    # also generate files as 3dREMLfit likes them
    n_n = 0
    n_r_v = 0
    n_r_p = 0
    n_e = 0
    if respiration_info:
        n_n = len(respiration_info['time_series_time'])
        n_r_p = size(respiration_info['phase_slice_reg'],1)
        n_r_v = size(respiration_info['rvtrs_slc'],1)

    if cardiac_info: # must have cardiac_info
        n_n = len(cardiac_phased['time_series_time'])  # ok to overwrite len(respiration_info.tst), should be same.
        n_e = size(cardiac_phased['phase_slice_reg'], 1)

    if main_info['cardiac_out'] == 0 and main_info['respiration_out'] == 0 and main_info['rvt_out'] == 0:
        print 'Options cardiac_out, respiration_out, and RVT_out all 0.\nNo output required.\n'
        return

    temp_y_axis = main_info['number_of_slices'] * ((main_info['rvt_out']) * n_r_v
                                                   + (main_info['respiration_out']) * n_r_p
                                                   + (main_info['cardiac_out']) * n_e)
    main_info['reml_out'] = zeros((n_n, temp_y_axis))
    cnt = 0
    head = '<RetroTSout\n' \
           'ni_type = "%d*double"\n' \
           'ni_dimen = "%d"\n' \
           'ColumnLabels = "'\
           % (size((main_info['reml_out'], 2)), size((main_info['reml_out'], 1)))
    tail = '"\n>'
    tailclose = '</RetroTSout>'

    label = head

    main_info['reml_out'] = []
    if main_info['slice_major'] == 0: # old approach, not handy for 3dREMLfit
        # RVT
        if main_info['rvt_out'] != 0:
            for j in range(0, size(respiration_info['rvtrs_slc'], 2)):
                for i in range(0, main_info['number_of_slices']):
                    cnt += 1
                    main_info['reml_out'][:,cnt] = respiration_info['rvtrs_slc'][:,j]  # same for each slice
                    label = '%s s%d.RVT%d ;' % (label, i, j)
        # Resp
        if main_info['respiration_out'] != 0:
            for j in range(0, size(respiration_info['phase_slice_reg'], 2)):
                for i in range(0, main_info['number_of_slices']):
                    cnt += 1
                    main_info['reml_out'][:,cnt] = respiration_info['phase_slice_reg'][:,j,i]
                    label = '%s s%d.Resp%d ;' % (label, i, j)
        # Card
        if main_info['Card_out'] != 0:
            for j in range(0, size(cardiac_info['phase_slice_reg'], 2)):
                for i in range(0, main_info['number_of_slices']):
                    cnt += 1
                    main_info['reml_out'][:,cnt] = cardiac_info['phase_slice_reg'][:,j,i]
                    label = '%s s%d.Card%d ;' % (label, i, j)
        fid = open(('%s.retrots.1D', main_info['prefix']), 'w')
    else:
        for i in range(0, main_info['number_of_slices']):
            if main_info['rvt_out'] != 0:
                # RVT
                for j in range(0, shape(respiration_info['rvtrs_slc'])[0]):
                    cnt += 1
                    main_info['reml_out'].append(respiration_info['rvtrs_slc'][j])  # same regressor for each slice
                    label = '%s s%d.RVT%d ;' % (label, i, j)
            if main_info['respiration_out'] != 0:
                # Resp
                for j in range(0, shape(respiration_info['phase_slice_reg'])[1]):
                    cnt += 1
                    main_info['reml_out'].append(respiration_info['phase_slice_reg'][:, j, i])
                    label = '%s s%d.Resp%d ;' % (label, i, j)
            if main_info['cardiac_out'] != 0:
                # Card
                for j in range(0, shape(cardiac_info['phase_slice_reg'])[1]):
                    cnt += 1
                    main_info['reml_out'].append(cardiac_info['phase_slice_reg'][:, j, i])
                    label = '%s s%d.Card%d ;' % (label, i, j)
        fid = open(('%s.slibase.1D' % main_info['prefix']), 'w')

    # remove very last ';'
    label = label[1:-2]

    savetxt('%s.slibase.1D' % main_info['prefix'],
            column_stack(main_info['reml_out']),
            fmt='%.3f',
            delimiter=' ',
            newline='\n',
            header=('%s%s' % (label, tail)),
            footer=('%s' % tailclose))
    """
    fid.write('%s', label)
    fid.write('%s ', tail)
    for i in range(0, len(main_info['reml_out'])):
        fid.write('%s ', main_info['reml_out'][i, :])
        fprintf(fid, '\n ')
    fprintf(fid, '%s', tailclose)
    fclose(fid)
    """
    main_info['error'] = 0

    return main_info
