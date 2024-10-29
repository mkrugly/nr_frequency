nr_frequency
============

Ever struggled to compose consistent frequency parameters for 5G New Radio cells?
Ever tried to configure 5G New Radio contiguous carriers for CA?
Ever wondered where your 5G New Radio cell's SSBlock candidates are located in the time domain?

The `nr_frequency` module will let you do this efficiently.

The `nr_frequency` module provides classes for consistent generation of frequency related parameters such as ARFCN for SSB,
carrier frequency, reference PointA, relative offsets e.g. OffsetToPointA etc. making sure the SSB frequency is in
the sync raster and carrier frequency in the channel raster within the defined band frequency range.

It provides methods for handling frequency to arfcn and back, uplink from downlink frequencies (and vice versa),
calculation of carrier aggregation related parameters like nominal channel spacing or guardband.

The implementation is based on the TS 38.104 and TS 38.508. The parameters are calculated with the assumption
that the Control resource set zero (Coreset0) and Synchronization Signal Block (SS Block) should be as close as possible
to the beginning of the initial BWP (Coreset0 shall start with the start of initial BWP).

All the input and output frequencies are expressed in kHz.

Moreover it provides methods for the resolution of the SSB candidates possitions (index, start symbols, slots, subframes)
based on the TS 38.213 sec. 4.1

With only a few optional input parameters the module provides an optimal set of consistent NR settings for different scenarios.

Usage
-----

Single 5G NR cell frequency NR operating band n77, SCS 30 kHz and ΔFRaster 30 kHz (ref. 38.508-1 Table 4.3.1.1.1.77-2)::

    >>> from nr_frequency import nr_frequency
    >>> c = nr_frequency.Config(
    ...        param={
    ...            "scs_ssb": 30,     # SS/PBCH block subcarrier spacing TS 38.101-1 Table 5.4.3.3-1, TS 38.101-2 Table 5.4.3.3-1
    ...            "scs_common": 30,  # subCarrierSpacingCommon in MIB (scs for SIB1, Msg.2/4, broadcast etc.)
    ...            "scs_carrier": 30, # subcarrier spacing for the carrier (SCS-SpecificCarrier),
    ...                               # TS 38.101-1 Table 5.3.5-1, TS 38.101-2 Table 5.3.5-1
    ...            "fc_channel": 3750000, # proposed channel center frequency (maybe shifted
    ...                                   # if not in channel raster or coreset0, BWP start adjustment necessary)
    ...            "band": 77,  # NR operating band
    ...            "bw": 50,    # channel bandwidth
    ...            "pdcchConfigSib1": 24,  # pdcch-ConfigSIB1 in MIB (used to derive )
    ...            "offset_to_carrier": 102,  # offset between Point A and the lower edge of the carrier
    ...        }
    ...    )
    INFO:[{'pattern': 1, 'n_rb': 24, 'n_sym': 2, 'offset': 0}, {'pattern': 1, 'n_rb': 24, 'n_sym': 2, 'offset': 1}, {'pattern': 1, 'n_rb': 24, 'n_sym': 2, 'offset': 2}, {'pattern': 1, 'n_rb': 24, 'n_sym': 2, 'offset': 3}, {'pattern': 1, 'n_rb': 24, 'n_sym': 2, 'offset': 4}, {'pattern': 1, 'n_rb': 24, 'n_sym': 3, 'offset': 0}, {'pattern': 1, 'n_rb': 24, 'n_sym': 3, 'offset': 1}, {'pattern': 1, 'n_rb': 24, 'n_sym': 3, 'offset': 2}, {'pattern': 1, 'n_rb': 24, 'n_sym': 3, 'offset': 3}, {'pattern': 1, 'n_rb': 24, 'n_sym': 3, 'offset': 4}, {'pattern': 1, 'n_rb': 48, 'n_sym': 1, 'offset': 12}, {'pattern': 1, 'n_rb': 48, 'n_sym': 1, 'offset': 14}, {'pattern': 1, 'n_rb': 48, 'n_sym': 1, 'offset': 16}, {'pattern': 1, 'n_rb': 48, 'n_sym': 2, 'offset': 12}, {'pattern': 1, 'n_rb': 48, 'n_sym': 2, 'offset': 14}, {'pattern': 1, 'n_rb': 48, 'n_sym': 2, 'offset': 16}]
    DEBUG:freq_l:3300000, freq_h:4200000, bw:900000, cbw:47880, scs_carrier:30, channel_bw:50
    INFO:Adjusting Dl channel frequency to be in channel raster
    DEBUG:DL fc range:(3323940, 3750000, 4176060), fc_dl: 3750000
    INFO:Setting DL center frequency to 3738480
    INFO:Setting Ul channel frequency based on DL channel frequency
    INFO:Setting Ul channel bandwidth equal to Dl channel bandwidth
    DEBUG:freq_l:3300000, freq_h:4200000, bw:900000, cbw:47880, scs_carrier:30, channel_bw:50
    INFO:Adjusting Ul channel frequency to be in channel raster
    DEBUG:UL FC range:(3323940, 3750000, 4176060), fc_ul: 3750000
    INFO:Setting UL center frequency to 3738480

    >>> cell1_cfg = c.calculate()
    DEBUG:fc_dl:3750000, cwb_dl:47880, bw_ssb:7200, f_offset_rb:360
    INFO:Starting GSCN/F_SS selection from f_ssb_min:3730020
    INFO:Found f_ss:3730080 for gscn:8006
    INFO:Selected GSCN:8006, F_SS:3730080
    INFO:Adjusting channel frequency to align BWP start with Coreset0 start.
    INFO:f_diff(f_off_ssb_carrier:420 - f_offset_rb:360) = 60
    INFO:f_diff (k_ssb:4) <= k_ssb_max:22. Channel frequency shift not needed
    INFO:Absolute Frequency PointA ARFCN:645956 (f_pointA:3689340)
    INFO:Absolute Frequency SSB ARFCN:648672 (f_ss:3730080)
    INFO:Calculated Common Coreset: s_rb=0 (s_crb=102), n_rb=24, n_rbg=4, bitm=111100000000000000000000000000000000000000000
    INFO:Params: {'arfcn_point_a': 645956,
     'arfcn_point_a_ul': 645956,
     'arfcn_ssb': 648672,
     'band': 77,
     'band_bw_dl': 900000,
     'band_bw_ul': 900000,
     'band_dl_f_range': (3300000, 4200000),
     'band_ul_f_range': (3300000, 4200000),
     'bw': 50,
     'bw_ssb': 7200,
     'bw_ul': 50,
     'cbw_dl': 47880,
     'cbw_dl_nrb': 133,
     'cbw_ul': 47880,
     'cbw_ul_nrb': 133,
     'duplex': 'TDD',
     'f_domain_res': '111100000000000000000000000000000000000000000',
     'f_fc_to_point_a': 49140,
     'f_off_to_carrier': 36720,
     'f_offset_rb': 360,
     'f_point_a': 3689340,
     'f_point_a_ul': 3689340,
     'f_ss': 3730080,
     'fc_channel_dl': 3750000,
     'fc_channel_dl_high': 4176060,
     'fc_channel_dl_low': 3323940,
     'fc_channel_dl_range': (3323940, 3750000, 4176060),
     'fc_channel_ul': 3750000,
     'fc_channel_ul_high': 4176060,
     'fc_channel_ul_low': 3323940,
     'fc_channel_ul_range': (3323940, 3750000, 4176060),
     'fc_dl': 3738480,
     'fc_ul': 3738480,
     'freq_raster': 30,
     'gscn': 8006,
     'k_ssb': 4,
     'k_ssb_max': 22,
     'max_location_and_bw_dl': 36300,
     'max_location_and_bw_ul': 36300,
     'n_rb_coreset0': 24,
     'n_sym_coreset0': 2,
     'offset_coreset0_carrier': 0,
     'offset_rb': 1,
     'offset_to_carrier': 102,
     'offset_to_pa': 206,
     'pdcch_cfg_sib1': 24,
     'rb_6_size': 2160,
     'rb_size': 360,
     'scs_carrier': 30,
     'scs_carrier_num': 1,
     'scs_common': 30,
     'scs_common_num': 1,
     'scs_kssb': 15,
     'scs_ssb': 30,
     'scs_ssb_num': 1,
     'ssb_enabled': True,
     'ssb_pattern': 'caseC',
     'use_sync_raster': True}

    >>> cell1_cfg.get("gscn")
    8006
    >>> cell1_cfg.get("k_ssb")
    4
    >>> cell1_cfg.get("fc_channel_dl")
    3750000
    >>> cell1_cfg.get("offset_rb")
    1
    >>> cell1_cfg.get("offset_to_pa")
    206
    >>> cell1_cfg.get("arfcn_point_a")
    645956
    >>> cell1_cfg.get("arfcn_ssb")
    648672

Example of a contiguous intra-band two carriers configuration (NR operating band n77, SCS 30 kHz and ΔFRaster 30 kHz)::

    >>> from nr_frequency.nr_frequency import Config, CaConfig
    >>> c1 = Config(
    ...         param={
    ...             "scs_ssb": 30,
    ...             "scs_common": 30,
    ...             "scs_carrier": 30,
    ...             "fc_channel": 3750000,
    ...             "band": 77,
    ...             "bw": 50,
    ...             "pdcchConfigSib1": 164,
    ...             "offset_to_carrier": 0,
    ...         }
    ...     )
    INFO:[{'pattern': 1, 'n_rb': 24, 'n_sym': 2, 'offset': 0}, {'pattern': 1, 'n_rb': 24, 'n_sym': 2, 'offset': 1}, {'pattern': 1, 'n_rb': 24, 'n_sym': 2, 'offset': 2}, {'pattern': 1, 'n_rb': 24, 'n_sym': 2, 'offset': 3}, {'pattern': 1, 'n_rb': 24, 'n_sym': 2, 'offset': 4}, {'pattern': 1, 'n_rb': 24, 'n_sym': 3, 'offset': 0}, {'pattern': 1, 'n_rb': 24, 'n_sym': 3, 'offset': 1}, {'pattern': 1, 'n_rb': 24, 'n_sym': 3, 'offset': 2}, {'pattern': 1, 'n_rb': 24, 'n_sym': 3, 'offset': 3}, {'pattern': 1, 'n_rb': 24, 'n_sym': 3, 'offset': 4}, {'pattern': 1, 'n_rb': 48, 'n_sym': 1, 'offset': 12}, {'pattern': 1, 'n_rb': 48, 'n_sym': 1, 'offset': 14}, {'pattern': 1, 'n_rb': 48, 'n_sym': 1, 'offset': 16}, {'pattern': 1, 'n_rb': 48, 'n_sym': 2, 'offset': 12}, {'pattern': 1, 'n_rb': 48, 'n_sym': 2, 'offset': 14}, {'pattern': 1, 'n_rb': 48, 'n_sym': 2, 'offset': 16}]
    DEBUG:freq_l:3300000, freq_h:4200000, bw:900000, cbw:47880, scs_carrier:30, channel_bw:50
    INFO:Adjusting Dl channel frequency to be in channel raster
    DEBUG:DL fc range:(3323940, 3750000, 4176060), fc_dl: 3750000
    INFO:Setting DL center frequency to 3775200
    INFO:Setting Ul channel frequency based on DL channel frequency
    INFO:Setting Ul channel bandwidth equal to Dl channel bandwidth
    DEBUG:freq_l:3300000, freq_h:4200000, bw:900000, cbw:47880, scs_carrier:30, channel_bw:50
    INFO:Adjusting Ul channel frequency to be in channel raster
    DEBUG:UL FC range:(3323940, 3750000, 4176060), fc_ul: 3750000
    INFO:Setting UL center frequency to 3775200

    >>> cell1_cfg = c1.calculate()
    DEBUG:fc_dl:3750000, cwb_dl:47880, bw_ssb:7200, f_offset_rb:4320
    INFO:Starting GSCN/F_SS selection from f_ssb_min:3733980
    INFO:Found f_ss:3734400 for gscn:8009
    INFO:Selected GSCN:8009, F_SS:3734400
    INFO:Adjusting channel frequency to align BWP start with Coreset0 start.
    INFO:f_diff(f_off_ssb_carrier:4740 - f_offset_rb:4320) = 420
    INFO:f_diff (k_ssb:28) > k_ssb_max:22. Channel frequency shift needed
    INFO:trying _f_shift:420, k_ssb:0, f_k_ssb:0
    INFO:Shifting Channel Frequency up by shift:420 to 3750420, k_ssb:0
    INFO:Setting DL center frequency to 3775620
    INFO:Setting UL center frequency to 3775620
    INFO:Absolute Frequency PointA ARFCN:648432 (f_pointA:3726480)
    INFO:Absolute Frequency SSB ARFCN:648960 (f_ss:3734400)
    INFO:Calculated Common Coreset: s_rb=0 (s_crb=0), n_rb=48, n_rbg=8, bitm=111111110000000000000000000000000000000000000
    INFO:Params: {'arfcn_point_a': 648432,
     'arfcn_point_a_ul': 648432,
     'arfcn_ssb': 648960,
     'band': 77,
     'band_bw_dl': 900000,
     'band_bw_ul': 900000,
     'band_dl_f_range': (3300000, 4200000),
     'band_ul_f_range': (3300000, 4200000),
     'bw': 50,
     'bw_ssb': 7200,
     'bw_ul': 50,
     'cbw_dl': 47880,
     'cbw_dl_nrb': 133,
     'cbw_ul': 47880,
     'cbw_ul_nrb': 133,
     'duplex': 'TDD',
     'f_domain_res': '111111110000000000000000000000000000000000000',
     'f_fc_to_point_a': 49140,
     'f_off_to_carrier': 0,
     'f_offset_rb': 4320,
     'f_point_a': 3726480,
     'f_point_a_ul': 3726480,
     'f_ss': 3734400,
     'fc_channel_dl': 3750420,
     'fc_channel_dl_high': 4176060,
     'fc_channel_dl_low': 3323940,
     'fc_channel_dl_range': (3323940, 3750000, 4176060),
     'fc_channel_ul': 3750420,
     'fc_channel_ul_high': 4176060,
     'fc_channel_ul_low': 3323940,
     'fc_channel_ul_range': (3323940, 3750000, 4176060),
     'fc_dl': 3775620,
     'fc_ul': 3775620,
     'freq_raster': 30,
     'gscn': 8009,
     'k_ssb': 0,
     'k_ssb_max': 22,
     'max_location_and_bw_dl': 36300,
     'max_location_and_bw_ul': 36300,
     'n_rb_coreset0': 48,
     'n_sym_coreset0': 1,
     'offset_coreset0_carrier': 0,
     'offset_rb': 12,
     'offset_to_carrier': 0,
     'offset_to_pa': 24,
     'pdcch_cfg_sib1': 164,
     'rb_6_size': 2160,
     'rb_size': 360,
     'scs_carrier': 30,
     'scs_carrier_num': 1,
     'scs_common': 30,
     'scs_common_num': 1,
     'scs_kssb': 15,
     'scs_ssb': 30,
     'scs_ssb_num': 1,
     'ssb_enabled': True,
     'ssb_pattern': 'caseC',
     'use_sync_raster': True}

    >>> nom_cs = CaConfig.nominal_spacing(bw_c1=50, bw_c2=80, scs_c1=30, scs_c2=30, band=77)
    INFO:Calculating nominal channel spacing for band:77, channel_bandwidth pair:(50, 80) and subcarrier_spacing pair:(30, 30)
    INFO:checking mi_zero for {80, 50} in set()
    INFO:checking mi_zero for {80, 50} in set()
    INFO:checking mi_zero for {80, 50} in {100, 70, 40, 10, 15, 80, 50, 20, 25, 90, 60, 30}
    INFO:Found mi_zero: 2
    INFO:Calculated nominal channel spacing is 64860 kHz

    >>> c2 = Config(
    ...         param={
    ...             "scs_ssb": 30,
    ...             "scs_common": 30,
    ...             "scs_carrier": 30,
    ...             "fc_channel": c1.fc_channel_dl + nom_cs,
    ...             "band": 77,
    ...             "bw": 80,
    ...             "pdcchConfigSib1": 164,
    ...             "offset_to_carrier": 0,
    ...             "use_sync_raster": False,
    ...         }
    ...     )
    INFO:[{'pattern': 1, 'n_rb': 24, 'n_sym': 2, 'offset': 0}, {'pattern': 1, 'n_rb': 24, 'n_sym': 2, 'offset': 1}, {'pattern': 1, 'n_rb': 24, 'n_sym': 2, 'offset': 2}, {'pattern': 1, 'n_rb': 24, 'n_sym': 2, 'offset': 3}, {'pattern': 1, 'n_rb': 24, 'n_sym': 2, 'offset': 4}, {'pattern': 1, 'n_rb': 24, 'n_sym': 3, 'offset': 0}, {'pattern': 1, 'n_rb': 24, 'n_sym': 3, 'offset': 1}, {'pattern': 1, 'n_rb': 24, 'n_sym': 3, 'offset': 2}, {'pattern': 1, 'n_rb': 24, 'n_sym': 3, 'offset': 3}, {'pattern': 1, 'n_rb': 24, 'n_sym': 3, 'offset': 4}, {'pattern': 1, 'n_rb': 48, 'n_sym': 1, 'offset': 12}, {'pattern': 1, 'n_rb': 48, 'n_sym': 1, 'offset': 14}, {'pattern': 1, 'n_rb': 48, 'n_sym': 1, 'offset': 16}, {'pattern': 1, 'n_rb': 48, 'n_sym': 2, 'offset': 12}, {'pattern': 1, 'n_rb': 48, 'n_sym': 2, 'offset': 14}, {'pattern': 1, 'n_rb': 48, 'n_sym': 2, 'offset': 16}]
    DEBUG:freq_l:3300000, freq_h:4200000, bw:900000, cbw:78120, scs_carrier:30, channel_bw:80
    INFO:Adjusting Dl channel frequency to be in channel raster
    DEBUG:DL fc range:(3339060, 3750000, 4160940), fc_dl: 3815280
    INFO:Setting DL center frequency to 3825360
    INFO:Setting Ul channel frequency based on DL channel frequency
    INFO:Setting Ul channel bandwidth equal to Dl channel bandwidth
    DEBUG:freq_l:3300000, freq_h:4200000, bw:900000, cbw:78120, scs_carrier:30, channel_bw:80
    INFO:Adjusting Ul channel frequency to be in channel raster
    DEBUG:UL FC range:(3339060, 3750000, 4160940), fc_ul: 3815280
    INFO:Setting UL center frequency to 3825360
    cell2_cfg = c2.calculate()
    DEBUG:fc_dl:3815280, cwb_dl:78120, bw_ssb:7200, f_offset_rb:4320
    INFO:Adjusting channel frequency to align BWP start with Coreset0 start.
    INFO:f_diff(f_off_ssb_carrier:4320 - f_offset_rb:4320) = 0
    INFO:f_diff (k_ssb:0) <= k_ssb_max:22. Channel frequency shift not needed
    INFO:Absolute Frequency PointA ARFCN:651748 (f_pointA:3776220)
    INFO:Absolute Frequency SSB ARFCN:652276 (f_ss:3784140)
    INFO:Calculated Common Coreset: s_rb=0 (s_crb=0), n_rb=48, n_rbg=8, bitm=111111110000000000000000000000000000000000000
    INFO:Params: {'arfcn_point_a': 651748,
     'arfcn_point_a_ul': 651748,
     'arfcn_ssb': 652276,
     'band': 77,
     'band_bw_dl': 900000,
     'band_bw_ul': 900000,
     'band_dl_f_range': (3300000, 4200000),
     'band_ul_f_range': (3300000, 4200000),
     'bw': 80,
     'bw_ssb': 7200,
     'bw_ul': 80,
     'cbw_dl': 78120,
     'cbw_dl_nrb': 217,
     'cbw_ul': 78120,
     'cbw_ul_nrb': 217,
     'duplex': 'TDD',
     'f_domain_res': '111111110000000000000000000000000000000000000',
     'f_fc_to_point_a': 49140,
     'f_off_to_carrier': 0,
     'f_offset_rb': 4320,
     'f_point_a': 3776220,
     'f_point_a_ul': 3776220,
     'f_ss': 3784140,
     'fc_channel_dl': 3815280,
     'fc_channel_dl_high': 4160940,
     'fc_channel_dl_low': 3339060,
     'fc_channel_dl_range': (3339060, 3750000, 4160940),
     'fc_channel_ul': 3815280,
     'fc_channel_ul_high': 4160940,
     'fc_channel_ul_low': 3339060,
     'fc_channel_ul_range': (3339060, 3750000, 4160940),
     'fc_dl': 3825360,
     'fc_ul': 3825360,
     'freq_raster': 30,
     'gscn': 0,
     'k_ssb': 0,
     'k_ssb_max': 22,
     'max_location_and_bw_dl': 16499,
     'max_location_and_bw_ul': 16499,
     'n_rb_coreset0': 48,
     'n_sym_coreset0': 1,
     'offset_coreset0_carrier': 0,
     'offset_rb': 12,
     'offset_to_carrier': 0,
     'offset_to_pa': 24,
     'pdcch_cfg_sib1': 164,
     'rb_6_size': 2160,
     'rb_size': 360,
     'scs_carrier': 30,
     'scs_carrier_num': 1,
     'scs_common': 30,
     'scs_common_num': 1,
     'scs_kssb': 15,
     'scs_ssb': 30,
     'scs_ssb_num': 1,
     'ssb_enabled': True,
     'ssb_pattern': 'caseC',
     'use_sync_raster': False}

Finding SSB candidates positions::

    >>> from nr_frequency import nr_frequency
    >>> ss = nr_frequency.SsbPositions(band=257, scs_common=120, scs_ssb=120, in_onegroup='10000000', group_presence='10101010')
    >>> ss.ssb_candidates
    {0: (4, 0, 0), 16: (144, 10, 1), 32: (284, 20, 2), 48: (424, 30, 3)}
    >>> ss.scs_ssb=30
    >>> ss.scs_common=30
    >>> ss.band=77
    >>> ss.ssb_candidates
    {0: (2, 0, 0)}
    >>> ss.in_onegroup='11110001'
    >>> ss.ssb_candidates
    {0: (2, 0, 0), 1: (8, 0, 0), 2: (16, 1, 0), 3: (22, 1, 0), 7: (50, 3, 1)}
    >>> ss.ssb_pattern
    'caseC'
    >>> ss.ssb_candidates_start_symbols
    [2, 8, 16, 22, 50]
    >>> ss.ssb_candidates_index
    [0, 1, 2, 3, 7]