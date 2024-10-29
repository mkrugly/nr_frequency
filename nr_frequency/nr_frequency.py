# -*- coding: utf-8 -*-
"""NR frequency settings generation module

This modules provides classes for consistent generation of frequency related parameters such as NR Arfcn for SSB,
carrier frequency FC, reference PointA, relative offsets e.g. OffsetToPointA etc. making sure the SSB frequency is in
the sync raster and carrier frequency in channel raster within the defined band frequency range.

It provides methods for handling frequency to arfcn and back, Uplink from Downlink frequencies (and vice versa),
calculation of carrier aggregation related parameters like nominal channel spacing or guardbands.

The implementation is based on the TS 38.104 and TS 38.508. Currently parameters are calculated with the assumption
that the Control resource set zero (Coreset0) and Synchronization Signal Block (SS Block) should be as close as possible
to the beginning of the initial BWP (Coreset0 shall start with the start of initial BWP).

All the input and output frequencies are expressed in kHz.

Moreover it provides methods for the resolution of the SSB candidates possitions (index, start symbols, slots, subframes)
based on the TS 38.213 sec. 4.1.

With only a few optional input parameters the module provides an optimal set of consistent NR settings for different scenarios.

Example::

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

"""
from typing import List, Dict, Any, Tuple, Callable, Optional
import math
from collections import OrderedDict
from pprint import pformat
import logging

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


def lcm(a: int, b: int) -> int:
    """Function for finding Lowest Common Multiple"""
    return a * b // math.gcd(a, b)


class Numerology:
    """Class for numerology to scs and vice-versa mappings

    (TS 38.104)
    """

    mi_to_scs = {0: 15, 1: 30, 2: 60, 3: 120, 4: 240}
    scs_to_mi = {15: 0, 30: 1, 60: 2, 120: 3, 240: 4}

    @classmethod
    def scs(cls, mi: int = 0) -> int:
        """Class method for mapping the nummerology to subcarrier spacing

        Args:
            mi: numerology

        Returns:
            subcarrier spacing in kHz
        """
        return cls.mi_to_scs.get(mi, -1)

    @classmethod
    def mi(cls, scs: int = 15) -> int:
        """Class method for mapping the subcarrier spacing to nummerology

        Args:
            scs: subcarrier spacing in kHz

        Returns:
            numerology
        """
        return cls.scs_to_mi.get(scs, -1)


class NrArfcn:
    """Class for frequency, arfcn and gscn calculations

    It provides class methods for carrier frequencies ranges for the given band and bandwidth, gscn calculation, dl
    from ul frequencies and vice versa, checking if frequencies are in channel raster, sync raster etc. as well as for
    frequency to arfcn, frequency to gscn and vice versa calculation

    """

    # TS 38.104 Table 5.2-1: NR operating bands in FR1
    # TS 38.104 Table 5.2-2: NR operating bands in FR2
    bands = {
        1: {"f_ul_low": 1920, "f_ul_high": 1980, "f_dl_low": 2110, "f_dl_high": 2170, "duplex": "FDD"},
        2: {"f_ul_low": 1850, "f_ul_high": 1910, "f_dl_low": 1930, "f_dl_high": 1990, "duplex": "FDD"},
        3: {"f_ul_low": 1710, "f_ul_high": 1785, "f_dl_low": 1805, "f_dl_high": 1880, "duplex": "FDD"},
        5: {"f_ul_low": 824, "f_ul_high": 849, "f_dl_low": 869, "f_dl_high": 894, "duplex": "FDD"},
        7: {"f_ul_low": 2500, "f_ul_high": 2570, "f_dl_low": 2620, "f_dl_high": 2690, "duplex": "FDD"},
        8: {"f_ul_low": 880, "f_ul_high": 915, "f_dl_low": 925, "f_dl_high": 960, "duplex": "FDD"},
        12: {"f_ul_low": 699, "f_ul_high": 716, "f_dl_low": 729, "f_dl_high": 746, "duplex": "FDD"},
        13: {"f_ul_low": 777, "f_ul_high": 787, "f_dl_low": 746, "f_dl_high": 756, "duplex": "FDD"},
        14: {"f_ul_low": 788, "f_ul_high": 798, "f_dl_low": 758, "f_dl_high": 768, "duplex": "FDD"},
        18: {"f_ul_low": 815, "f_ul_high": 830, "f_dl_low": 860, "f_dl_high": 875, "duplex": "FDD"},
        20: {"f_ul_low": 832, "f_ul_high": 862, "f_dl_low": 791, "f_dl_high": 821, "duplex": "FDD"},
        24: {"f_ul_low": 1626.5, "f_ul_high": 1660.5, "f_dl_low": 1525, "f_dl_high": 1559, "duplex": "FDD"},
        25: {"f_ul_low": 1850, "f_ul_high": 1915, "f_dl_low": 1930, "f_dl_high": 1995, "duplex": "FDD"},
        26: {"f_ul_low": 814, "f_ul_high": 849, "f_dl_low": 859, "f_dl_high": 894, "duplex": "FDD"},
        28: {"f_ul_low": 703, "f_ul_high": 748, "f_dl_low": 758, "f_dl_high": 803, "duplex": "FDD"},
        29: {"f_ul_low": -1, "f_ul_high": -1, "f_dl_low": 717, "f_dl_high": 728, "duplex": "SDL"},
        30: {"f_ul_low": 2305, "f_ul_high": 2315, "f_dl_low": 2350, "f_dl_high": 2360, "duplex": "FDD"},
        34: {"f_ul_low": 2010, "f_ul_high": 2025, "f_dl_low": 2010, "f_dl_high": 2025, "duplex": "TDD"},
        38: {"f_ul_low": 2570, "f_ul_high": 2620, "f_dl_low": 2570, "f_dl_high": 2620, "duplex": "TDD"},
        39: {"f_ul_low": 1880, "f_ul_high": 1920, "f_dl_low": 1880, "f_dl_high": 1920, "duplex": "TDD"},
        40: {"f_ul_low": 2300, "f_ul_high": 2400, "f_dl_low": 2300, "f_dl_high": 2400, "duplex": "TDD"},
        41: {"f_ul_low": 2496, "f_ul_high": 2690, "f_dl_low": 2496, "f_dl_high": 2690, "duplex": "TDD"},
        46: {"f_ul_low": 5150, "f_ul_high": 5925, "f_dl_low": 5150, "f_dl_high": 5925, "duplex": "TDD"},
        48: {"f_ul_low": 3550, "f_ul_high": 3700, "f_dl_low": 3550, "f_dl_high": 3700, "duplex": "TDD"},
        50: {"f_ul_low": 1432, "f_ul_high": 1517, "f_dl_low": 1432, "f_dl_high": 1517, "duplex": "TDD"},
        51: {"f_ul_low": 1427, "f_ul_high": 1432, "f_dl_low": 1427, "f_dl_high": 1432, "duplex": "TDD"},
        53: {"f_ul_low": 2483.5, "f_ul_high": 2495, "f_dl_low": 2483.5, "f_dl_high": 2495, "duplex": "TDD"},
        65: {"f_ul_low": 1920, "f_ul_high": 2010, "f_dl_low": 2110, "f_dl_high": 2200, "duplex": "FDD"},
        66: {"f_ul_low": 1710, "f_ul_high": 1780, "f_dl_low": 2110, "f_dl_high": 2200, "duplex": "FDD"},
        67: {"f_ul_low": -1, "f_ul_high": -1, "f_dl_low": 738, "f_dl_high": 758, "duplex": "SDL"},
        70: {"f_ul_low": 1695, "f_ul_high": 1710, "f_dl_low": 1995, "f_dl_high": 2020, "duplex": "FDD"},
        71: {"f_ul_low": 663, "f_ul_high": 698, "f_dl_low": 617, "f_dl_high": 652, "duplex": "FDD"},
        74: {"f_ul_low": 1427, "f_ul_high": 1470, "f_dl_low": 1475, "f_dl_high": 1518, "duplex": "FDD"},
        75: {"f_ul_low": -1, "f_ul_high": -1, "f_dl_low": 1432, "f_dl_high": 1517, "duplex": "SDL"},
        76: {"f_ul_low": -1, "f_ul_high": -1, "f_dl_low": 1427, "f_dl_high": 1432, "duplex": "SDL"},
        77: {"f_ul_low": 3300, "f_ul_high": 4200, "f_dl_low": 3300, "f_dl_high": 4200, "duplex": "TDD"},
        78: {"f_ul_low": 3300, "f_ul_high": 3800, "f_dl_low": 3300, "f_dl_high": 3800, "duplex": "TDD"},
        79: {"f_ul_low": 4400, "f_ul_high": 5000, "f_dl_low": 4400, "f_dl_high": 5000, "duplex": "TDD"},
        80: {"f_ul_low": 1710, "f_ul_high": 1785, "f_dl_low": -1, "f_dl_high": -1, "duplex": "SUL"},
        81: {"f_ul_low": 880, "f_ul_high": 915, "f_dl_low": -1, "f_dl_high": -1, "duplex": "SUL"},
        82: {"f_ul_low": 832, "f_ul_high": 862, "f_dl_low": -1, "f_dl_high": -1, "duplex": "SUL"},
        83: {"f_ul_low": 703, "f_ul_high": 748, "f_dl_low": -1, "f_dl_high": -1, "duplex": "SUL"},
        84: {"f_ul_low": 1920, "f_ul_high": 1980, "f_dl_low": -1, "f_dl_high": -1, "duplex": "SUL"},
        85: {"f_ul_low": 698, "f_ul_high": 716, "f_dl_low": 728, "f_dl_high": 746, "duplex": "FDD"},
        86: {"f_ul_low": 1710, "f_ul_high": 1780, "f_dl_low": -1, "f_dl_high": -1, "duplex": "SUL"},
        89: {"f_ul_low": 824, "f_ul_high": 849, "f_dl_low": -1, "f_dl_high": -1, "duplex": "SUL"},
        90: {"f_ul_low": 2496, "f_ul_high": 2690, "f_dl_low": 2496, "f_dl_high": 2690, "duplex": "TDD"},
        91: {"f_ul_low": 832, "f_ul_high": 862, "f_dl_low": 1427, "f_dl_high": 1432, "duplex": "FDD"},
        92: {"f_ul_low": 832, "f_ul_high": 862, "f_dl_low": 1432, "f_dl_high": 1517, "duplex": "FDD"},
        93: {"f_ul_low": 880, "f_ul_high": 915, "f_dl_low": 1427, "f_dl_high": 1432, "duplex": "FDD"},
        94: {"f_ul_low": 880, "f_ul_high": 915, "f_dl_low": 1432, "f_dl_high": 1517, "duplex": "FDD"},
        95: {"f_ul_low": 2010, "f_ul_high": 2025, "f_dl_low": -1, "f_dl_high": -1, "duplex": "SUL"},
        96: {"f_ul_low": 5925, "f_ul_high": 7125, "f_dl_low": 5925, "f_dl_high": 7125, "duplex": "TDD"},
        97: {"f_ul_low": 2300, "f_ul_high": 2400, "f_dl_low": -1, "f_dl_high": -1, "duplex": "SUL"},
        98: {"f_ul_low": 1880, "f_ul_high": 1920, "f_dl_low": -1, "f_dl_high": -1, "duplex": "SUL"},
        99: {"f_ul_low": 1626.5, "f_ul_high": 1660.5, "f_dl_low": -1, "f_dl_high": -1, "duplex": "SUL"},
        100: {"f_ul_low": 874.4, "f_ul_high": 880, "f_dl_low": 919.4, "f_dl_high": 925, "duplex": "FDD"},
        101: {"f_ul_low": 1900, "f_ul_high": 1910, "f_dl_low": 1900, "f_dl_high": 1910, "duplex": "TDD"},
        102: {"f_ul_low": 5925, "f_ul_high": 6425, "f_dl_low": 5925, "f_dl_high": 6425, "duplex": "TDD"},
        104: {"f_ul_low": 6425, "f_ul_high": 7125, "f_dl_low": 6425, "f_dl_high": 7125, "duplex": "TDD"},
        257: {"f_ul_low": 26500, "f_ul_high": 29500, "f_dl_low": 26500, "f_dl_high": 29500, "duplex": "TDD"},
        258: {"f_ul_low": 24250, "f_ul_high": 27500, "f_dl_low": 24250, "f_dl_high": 27500, "duplex": "TDD"},
        259: {"f_ul_low": 39500, "f_ul_high": 43500, "f_dl_low": 39500, "f_dl_high": 43500, "duplex": "TDD"},
        260: {"f_ul_low": 37000, "f_ul_high": 40000, "f_dl_low": 37000, "f_dl_high": 40000, "duplex": "TDD"},
        261: {"f_ul_low": 27500, "f_ul_high": 28350, "f_dl_low": 27500, "f_dl_high": 28350, "duplex": "TDD"},
        262: {"f_ul_low": 47200, "f_ul_high": 48200, "f_dl_low": 47200, "f_dl_high": 48200, "duplex": "TDD"},
    }

    # TS 38.104 Table 5.4.2.1-1
    global_freq_raster = [
        {"delta_f_global": 5, "freq_offset": 0, "nref_offset": 0},
        {"delta_f_global": 15, "freq_offset": 3000000, "nref_offset": 600000},
        {"delta_f_global": 60, "freq_offset": 24250080, "nref_offset": 2016667},
    ]

    # TS 38.104 table Table 5.4.2.3-1
    channel_freq_raster = {
        (1	, 100): {"band": 1	, "delta_f": 100, "ul_arfcn_low": 384000, "ul_step": 20, "ul_arfcn_high": 396000, "arfcn_low": 422000, "step": 20, "arfcn_high": 434000},
        (2	, 100): {"band": 2	, "delta_f": 100, "ul_arfcn_low": 370000, "ul_step": 20, "ul_arfcn_high": 382000, "arfcn_low": 386000, "step": 20, "arfcn_high": 398000},
        (3	, 100): {"band": 3	, "delta_f": 100, "ul_arfcn_low": 342000, "ul_step": 20, "ul_arfcn_high": 357000, "arfcn_low": 361000, "step": 20, "arfcn_high": 376000},
        (5	, 100): {"band": 5	, "delta_f": 100, "ul_arfcn_low": 164800, "ul_step": 20, "ul_arfcn_high": 169800, "arfcn_low": 173800, "step": 20, "arfcn_high": 178800},
        (7	, 100): {"band": 7	, "delta_f": 100, "ul_arfcn_low": 500000, "ul_step": 20, "ul_arfcn_high": 514000, "arfcn_low": 524000, "step": 20, "arfcn_high": 538000},
        (8	, 100): {"band": 8	, "delta_f": 100, "ul_arfcn_low": 176000, "ul_step": 20, "ul_arfcn_high": 183000, "arfcn_low": 185000, "step": 20, "arfcn_high": 192000},
        (12	, 100): {"band": 12	, "delta_f": 100, "ul_arfcn_low": 139800, "ul_step": 20, "ul_arfcn_high": 143200, "arfcn_low": 145800, "step": 20, "arfcn_high": 149200},
        (13	, 100): {"band": 13	, "delta_f": 100, "ul_arfcn_low": 155400, "ul_step": 20, "ul_arfcn_high": 157400, "arfcn_low": 149200, "step": 20, "arfcn_high": 151200},
        (14	, 100): {"band": 14	, "delta_f": 100, "ul_arfcn_low": 157600, "ul_step": 20, "ul_arfcn_high": 159600, "arfcn_low": 151600, "step": 20, "arfcn_high": 153600},
        (18	, 100): {"band": 18	, "delta_f": 100, "ul_arfcn_low": 163000, "ul_step": 20, "ul_arfcn_high": 166000, "arfcn_low": 172000, "step": 20, "arfcn_high": 175000},
        (20	, 100): {"band": 20	, "delta_f": 100, "ul_arfcn_low": 166400, "ul_step": 20, "ul_arfcn_high": 172400, "arfcn_low": 158200, "step": 20, "arfcn_high": 164200},
        (25	, 100): {"band": 25	, "delta_f": 100, "ul_arfcn_low": 370000, "ul_step": 20, "ul_arfcn_high": 383000, "arfcn_low": 386000, "step": 20, "arfcn_high": 399000},
        (24	, 100): {"band": 24	, "delta_f": 100, "ul_arfcn_low": 325300, "ul_step": 20, "ul_arfcn_high": 332100, "arfcn_low": 305000, "step": 20, "arfcn_high": 311800},
        (26	, 100): {"band": 26	, "delta_f": 100, "ul_arfcn_low": 162800, "ul_step": 20, "ul_arfcn_high": 169800, "arfcn_low": 171800, "step": 20, "arfcn_high": 178800},
        (28	, 100): {"band": 28	, "delta_f": 100, "ul_arfcn_low": 140600, "ul_step": 20, "ul_arfcn_high": 149600, "arfcn_low": 151600, "step": 20, "arfcn_high": 160600},
        (29	, 100): {"band": 29	, "delta_f": 100, "ul_arfcn_low": -1,     "ul_step": -1, "ul_arfcn_high": -1   	, "arfcn_low": 143400, "step": 20, "arfcn_high": 145600},
        (30	, 100): {"band": 30	, "delta_f": 100, "ul_arfcn_low": 461000, "ul_step": 20, "ul_arfcn_high": 463000, "arfcn_low": 470000, "step": 20, "arfcn_high": 472000},
        (34	, 100): {"band": 34	, "delta_f": 100, "ul_arfcn_low": 402000, "ul_step": 20, "ul_arfcn_high": 405000, "arfcn_low": 402000, "step": 20, "arfcn_high": 405000},
        (38	, 100): {"band": 38	, "delta_f": 100, "ul_arfcn_low": 514000, "ul_step": 20, "ul_arfcn_high": 524000, "arfcn_low": 514000, "step": 20, "arfcn_high": 524000},
        (39	, 100): {"band": 39	, "delta_f": 100, "ul_arfcn_low": 376000, "ul_step": 20, "ul_arfcn_high": 384000, "arfcn_low": 376000, "step": 20, "arfcn_high": 384000},
        (40	, 100): {"band": 40	, "delta_f": 100, "ul_arfcn_low": 460000, "ul_step": 20, "ul_arfcn_high": 480000, "arfcn_low": 460000, "step": 20, "arfcn_high": 480000},
        (41	, 15 ): {"band": 41 , "delta_f": 15 , "ul_arfcn_low": 499200, "ul_step":  3, "ul_arfcn_high": 537999, "arfcn_low": 499200, "step":  3, "arfcn_high": 537999},
        (41	, 30 ): {"band": 41 , "delta_f": 30 , "ul_arfcn_low": 499200, "ul_step":  6, "ul_arfcn_high": 537996, "arfcn_low": 499200, "step":  6, "arfcn_high": 537996},
        (46	, 15 ): {"band": 46 , "delta_f": 15 , "ul_arfcn_low": 743334, "ul_step":  1, "ul_arfcn_high": 795000, "arfcn_low": 743334, "step":  1, "arfcn_high": 795000},
        (48	, 15 ): {"band": 48 , "delta_f": 15 , "ul_arfcn_low": 636667, "ul_step":  1, "ul_arfcn_high": 646666, "arfcn_low": 636667, "step":  1, "arfcn_high": 646666},
        (48	, 30 ): {"band": 48 , "delta_f": 30 , "ul_arfcn_low": 636668, "ul_step":  2, "ul_arfcn_high": 646666, "arfcn_low": 636668, "step":  2, "arfcn_high": 646666},
        (50	, 100): {"band": 50	, "delta_f": 100, "ul_arfcn_low": 286400, "ul_step": 20, "ul_arfcn_high": 303400, "arfcn_low": 286400, "step": 20, "arfcn_high": 303400},
        (51	, 100): {"band": 51	, "delta_f": 100, "ul_arfcn_low": 285400, "ul_step": 20, "ul_arfcn_high": 286400, "arfcn_low": 285400, "step": 20, "arfcn_high": 286400},
        (53	, 100): {"band": 53	, "delta_f": 100, "ul_arfcn_low": 496700, "ul_step": 20, "ul_arfcn_high": 499000, "arfcn_low": 496700, "step": 20, "arfcn_high": 499000},
        (65	, 100): {"band": 65	, "delta_f": 100, "ul_arfcn_low": 384000, "ul_step": 20, "ul_arfcn_high": 402000, "arfcn_low": 422000, "step": 20, "arfcn_high": 440000},
        (66	, 100): {"band": 66	, "delta_f": 100, "ul_arfcn_low": 342000, "ul_step": 20, "ul_arfcn_high": 356000, "arfcn_low": 422000, "step": 20, "arfcn_high": 440000},
        (67	, 100): {"band": 67	, "delta_f": 100, "ul_arfcn_low": -1,     "ul_step": -1, "ul_arfcn_high": -1   	, "arfcn_low": 147600, "step": 20, "arfcn_high": 151600},
        (70	, 100): {"band": 70	, "delta_f": 100, "ul_arfcn_low": 339000, "ul_step": 20, "ul_arfcn_high": 342000, "arfcn_low": 399000, "step": 20, "arfcn_high": 404000},
        (71	, 100): {"band": 71	, "delta_f": 100, "ul_arfcn_low": 132600, "ul_step": 20, "ul_arfcn_high": 139600, "arfcn_low": 123400, "step": 20, "arfcn_high": 130400},
        (74	, 100): {"band": 74	, "delta_f": 100, "ul_arfcn_low": 285400, "ul_step": 20, "ul_arfcn_high": 294000, "arfcn_low": 295000, "step": 20, "arfcn_high": 303600},
        (75	, 100): {"band": 75	, "delta_f": 100, "ul_arfcn_low": -1,     "ul_step": -1, "ul_arfcn_high": -1   	, "arfcn_low": 286400, "step": 20, "arfcn_high": 303400},
        (76	, 100): {"band": 76	, "delta_f": 100, "ul_arfcn_low": -1,     "ul_step": -1, "ul_arfcn_high": -1   	, "arfcn_low": 285400, "step": 20, "arfcn_high": 286400},
        (77	, 15 ): {"band": 77	, "delta_f": 15 , "ul_arfcn_low": 620000, "ul_step":  1, "ul_arfcn_high": 680000, "arfcn_low": 620000, "step":  1, "arfcn_high": 680000},
        (77	, 30 ): {"band": 77	, "delta_f": 30 , "ul_arfcn_low": 620000, "ul_step":  2, "ul_arfcn_high": 680000, "arfcn_low": 620000, "step":  2, "arfcn_high": 680000},
        (78	, 15 ): {"band": 78	, "delta_f": 15 , "ul_arfcn_low": 620000, "ul_step":  1, "ul_arfcn_high": 653333, "arfcn_low": 620000, "step":  1, "arfcn_high": 653333},
        (78	, 30 ): {"band": 78	, "delta_f": 30 , "ul_arfcn_low": 620000, "ul_step":  2, "ul_arfcn_high": 653332, "arfcn_low": 620000, "step":  2, "arfcn_high": 653332},
        (79	, 15 ): {"band": 79	, "delta_f": 15 , "ul_arfcn_low": 693334, "ul_step":  1, "ul_arfcn_high": 733333, "arfcn_low": 693334, "step":  1, "arfcn_high": 733333},
        (79	, 30 ): {"band": 79	, "delta_f": 30 , "ul_arfcn_low": 693334, "ul_step":  2, "ul_arfcn_high": 733332, "arfcn_low": 693334, "step":  2, "arfcn_high": 733332},
        (80	, 100): {"band": 80	, "delta_f": 100, "ul_arfcn_low": 342000, "ul_step": 20, "ul_arfcn_high": 357000, "arfcn_low": -1,     "step": -1, "arfcn_high": -1    },
        (81	, 100): {"band": 81	, "delta_f": 100, "ul_arfcn_low": 176000, "ul_step": 20, "ul_arfcn_high": 183000, "arfcn_low": -1,     "step": -1, "arfcn_high": -1    },
        (82	, 100): {"band": 82	, "delta_f": 100, "ul_arfcn_low": 166400, "ul_step": 20, "ul_arfcn_high": 172400, "arfcn_low": -1,     "step": -1, "arfcn_high": -1    },
        (83	, 100): {"band": 83	, "delta_f": 100, "ul_arfcn_low": 140600, "ul_step": 20, "ul_arfcn_high": 149600, "arfcn_low": -1,     "step": -1, "arfcn_high": -1    },
        (84	, 100): {"band": 84	, "delta_f": 100, "ul_arfcn_low": 384000, "ul_step": 20, "ul_arfcn_high": 396000, "arfcn_low": -1,     "step": -1, "arfcn_high": -1    },
        (85	, 100): {"band": 85	, "delta_f": 100, "ul_arfcn_low": 139600, "ul_step": 20, "ul_arfcn_high": 143200, "arfcn_low": 145600, "step": 20, "arfcn_high": 149200},
        (86	, 100): {"band": 86	, "delta_f": 100, "ul_arfcn_low": 342000, "ul_step": 20, "ul_arfcn_high": 356000, "arfcn_low": -1,     "step": -1, "arfcn_high": -1    },
        (89	, 100): {"band": 89	, "delta_f": 100, "ul_arfcn_low": 164800, "ul_step": 20, "ul_arfcn_high": 169800, "arfcn_low": -1,     "step": -1, "arfcn_high": -1    },
        (90	, 15 ): {"band": 90	, "delta_f": 15 , "ul_arfcn_low": 499200, "ul_step":  3, "ul_arfcn_high": 537999, "arfcn_low": 499200, "step":  3, "arfcn_high": 537999},
        (90	, 30 ): {"band": 90	, "delta_f": 30 , "ul_arfcn_low": 499200, "ul_step":  6, "ul_arfcn_high": 537996, "arfcn_low": 499200, "step":  6, "arfcn_high": 537996},
        (90 , 100): {"band": 90 , "delta_f": 100, "ul_arfcn_low": 499200, "ul_step": 20, "ul_arfcn_high": 538000, "arfcn_low": 499200, "step": 20, "arfcn_high": 538000},
        (91	, 100): {"band": 91	, "delta_f": 100, "ul_arfcn_low": 166400, "ul_step": 20, "ul_arfcn_high": 172400, "arfcn_low": 285400, "step": 20, "arfcn_high": 286400},
        (92	, 100): {"band": 92	, "delta_f": 100, "ul_arfcn_low": 166400, "ul_step": 20, "ul_arfcn_high": 172400, "arfcn_low": 286400, "step": 20, "arfcn_high": 303400},
        (93	, 100): {"band": 93	, "delta_f": 100, "ul_arfcn_low": 176000, "ul_step": 20, "ul_arfcn_high": 183000, "arfcn_low": 285400, "step": 20, "arfcn_high": 286400},
        (94	, 100): {"band": 94	, "delta_f": 100, "ul_arfcn_low": 176000, "ul_step": 20, "ul_arfcn_high": 183000, "arfcn_low": 286400, "step": 20, "arfcn_high": 303400},
        (95	, 100): {"band": 95	, "delta_f": 100, "ul_arfcn_low": 402000, "ul_step": 20, "ul_arfcn_high": 405000, "arfcn_low": -1,     "step": -1, "arfcn_high": -1    },
        (96	, 15 ): {"band": 96	, "delta_f": 15 , "ul_arfcn_low": 795000, "ul_step":  1, "ul_arfcn_high": 875000, "arfcn_low": 795000, "step":  1, "arfcn_high": 875000},
        (97	, 100): {"band": 97	, "delta_f": 100, "ul_arfcn_low": 460000, "ul_step": 20, "ul_arfcn_high": 480000, "arfcn_low": -1,     "step": -1, "arfcn_high": -1    },
        (98	, 100): {"band": 98	, "delta_f": 100, "ul_arfcn_low": 376000, "ul_step": 20, "ul_arfcn_high": 384000, "arfcn_low": -1,     "step": -1, "arfcn_high": -1    },
        (99	, 100): {"band": 99	, "delta_f": 100, "ul_arfcn_low": 325300, "ul_step": 20, "ul_arfcn_high": 332100, "arfcn_low": -1,     "step": -1, "arfcn_high": -1    },
        (100, 100): {"band": 100, "delta_f": 100, "ul_arfcn_low": 174880, "ul_step": 20, "ul_arfcn_high": 176000, "arfcn_low": 183880, "step": 20, "arfcn_high": 185000},
        (101, 100): {"band": 101, "delta_f": 100, "ul_arfcn_low": 380000, "ul_step": 20, "ul_arfcn_high": 382000, "arfcn_low": 380000, "step": 20, "arfcn_high": 382000},
        (102, 15 ): {"band": 102, "delta_f": 15 , "ul_arfcn_low": 796334, "ul_step":  1, "ul_arfcn_high": 828333, "arfcn_low": 796334, "step":  1, "arfcn_high": 828333},
        (104, 15 ): {"band": 104, "delta_f": 15 , "ul_arfcn_low": 828334, "ul_step":  1, "ul_arfcn_high": 875000, "arfcn_low": 828334, "step":  1, "arfcn_high": 875000},
        (104, 30 ): {"band": 104, "delta_f": 30 , "ul_arfcn_low": 828334, "ul_step":  2, "ul_arfcn_high": 875000, "arfcn_low": 828334, "step":  2, "arfcn_high": 875000}
    }

    # TS 38.104 table Table 5.4.2.3-2
    channel_freq_raster_fr2 = {
        (257, 60):  {"band": 257, "delta_f": 60,  "ul_arfcn_low": 2054166, "ul_step": 1, "ul_arfcn_high": 2104165, "arfcn_low": 2054166, "step": 1, "arfcn_high": 2104165},
        (257, 120): {"band": 257, "delta_f": 120, "ul_arfcn_low": 2054167, "ul_step": 2, "ul_arfcn_high": 2104165, "arfcn_low": 2054167, "step": 2, "arfcn_high": 2104165},
        (258, 60):  {"band": 258, "delta_f": 60,  "ul_arfcn_low": 2016667, "ul_step": 1, "ul_arfcn_high": 2070832, "arfcn_low": 2016667, "step": 1, "arfcn_high": 2070832},
        (258, 120): {"band": 258, "delta_f": 120, "ul_arfcn_low": 2016667, "ul_step": 2, "ul_arfcn_high": 2070831, "arfcn_low": 2016667, "step": 2, "arfcn_high": 2070831},
        (259, 60):  {"band": 259, "delta_f": 60,  "ul_arfcn_low": 2270833, "ul_step": 1, "ul_arfcn_high": 2337499, "arfcn_low": 2270833, "step": 1, "arfcn_high": 2337499},
        (259, 120): {"band": 259, "delta_f": 120, "ul_arfcn_low": 2270833, "ul_step": 2, "ul_arfcn_high": 2337499, "arfcn_low": 2270833, "step": 2, "arfcn_high": 2337499},
        (260, 60):  {"band": 260, "delta_f": 60,  "ul_arfcn_low": 2229166, "ul_step": 1, "ul_arfcn_high": 2279165, "arfcn_low": 2229166, "step": 1, "arfcn_high": 2279165},
        (260, 120): {"band": 260, "delta_f": 120, "ul_arfcn_low": 2229167, "ul_step": 2, "ul_arfcn_high": 2279165, "arfcn_low": 2229167, "step": 2, "arfcn_high": 2279165},
        (261, 60):  {"band": 261, "delta_f": 60,  "ul_arfcn_low": 2070833, "ul_step": 1, "ul_arfcn_high": 2084999, "arfcn_low": 2070833, "step": 1, "arfcn_high": 2084999},
        (261, 120): {"band": 261, "delta_f": 120, "ul_arfcn_low": 2070833, "ul_step": 2, "ul_arfcn_high": 2084999, "arfcn_low": 2070833, "step": 2, "arfcn_high": 2084999},
        (262, 60):  {"band": 262, "delta_f": 60,  "ul_arfcn_low": 2399166, "ul_step": 1, "ul_arfcn_high": 2415832, "arfcn_low": 2399166, "step": 1, "arfcn_high": 2415832},
        (262, 120): {"band": 262, "delta_f": 120, "ul_arfcn_low": 2399167, "ul_step": 2, "ul_arfcn_high": 2415831, "arfcn_low": 2399167, "step": 2, "arfcn_high": 2415831},
    }

    # TS 38.104 tab. 5.3.2-1
    bandwidth = {
        15: {5: 25, 10: 52, 15: 79, 20: 106, 25: 133, 30: 160, 40: 216, 50: 270, 60: -1, 70: -1, 80: -1, 90: -1, 100: -1},
        30: {5: 11, 10: 24, 15: 38, 20: 51, 25: 65, 30: 78, 40: 106, 50: 133, 60: 162, 70: 189, 80: 217, 90: 245, 100: 273},
        60: {5: -1, 10: 11, 15: 18, 20: 24, 25: 31, 30: 38, 40: 51, 50: 65, 60: 79, 70: 93, 80: 107, 90: 121, 100: 135},
    }

    # TS 38.104 tab. 5.3.2-2
    bandwidth_fr2 = {60: {50: 66, 100: 132, 200: 264, 400: -1}, 120: {50: 32, 100: 66, 200: 132, 400: 264}}

    # TS 38.104 tab. 5.3.3-1
    guardband = {
        15: {5: 242.5, 10: 312.5, 15: 382.5, 20: 452.5, 25: 522.5, 30: 592.5, 40: 552.5, 50: 692.5, 60: -1, 80: -1, 90: -1, 100: -1},
        30: {5: 505, 10: 665, 15: 645, 20: 805, 25: 785, 30: 945, 40: 905, 50: 1045, 60: 825, 70: 965, 80: 925, 90: 885, 100: 845},
        60: {5: -1, 10: 1010, 15: 990, 20: 1330, 25: 1310, 30: 1290, 40: 1610, 50: 1570, 60: 1530, 80: 1450, 90: 1410, 100: 1370},
    }

    # TS 38.104 tab. 5.3.3-2 and tab. 5.3.3-3
    guardband_fr2 = {
        60: {50: 1210, 100: 2450, 200: 4930, 400: -1},
        120: {50: 1900, 100: 2420, 200: 4900, 400: 9860},
        240: {50: -1, 100: 3800, 200: 7720, 400: 15560},
    }

    # TS 38.104 tab. 5.3.5-1
    cbw_per_band_scs = {
        (1, 15): [5, 10, 15, 20, 25, 30, 40, 45, 50],
        (1, 30): [10, 15, 20, 25, 30, 40, 45, 50],
        (1, 60): [10, 15, 20, 25, 30, 40, 45, 50],
        (2, 15): [5, 10, 15, 20, 25, 30, 35, 40],
        (2, 30): [10, 15, 20, 25, 30, 35, 40],
        (2, 60): [10, 15, 20, 25, 30, 35, 40],
        (3, 15): [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
        (3, 30): [10, 15, 20, 25, 30, 35, 40, 45, 50],
        (3, 60): [10, 15, 20, 25, 30, 35, 40, 45, 50],
        (5, 15): [5, 10, 15, 20, 25],
        (5, 30): [10, 15, 20, 25],
        (7, 15): [5, 10, 15, 20, 25, 30, 35, 40, 50],
        (7, 30): [10, 15, 20, 25, 30, 35, 40, 50],
        (7, 60): [10, 15, 20, 25, 30, 35, 40, 50],
        (8, 15): [5, 10, 15, 20, 35],
        (8, 30): [10, 15, 20, 35],
        (12, 15): [5, 10, 15],
        (12, 30): [10, 15],
        (13, 15): [5, 10],
        (13, 30): [10],
        (14, 15): [5, 10],
        (14, 30): [10],
        (18, 15): [5, 10, 15],
        (18, 30): [10, 15],
        (20, 15): [5, 10, 15, 20],
        (20, 30): [10, 15, 20],
        (24, 15): [5, 10],
        (24, 30): [10],
        (24, 60): [10],
        (25, 15): [5, 10, 15, 20, 25, 30, 35, 40, 45],
        (25, 30): [10, 15, 20, 25, 30, 35, 40, 45],
        (25, 60): [10, 15, 20, 25, 30, 35, 40, 45],
        (26, 15): [5, 10, 15, 20, 25, 30],
        (26, 30): [10, 15, 20, 25, 30],
        (28, 15): [5, 10, 15, 20, 25, 30, 40],
        (28, 30): [10, 15, 20, 25, 30, 40],
        (29, 15): [5, 10],
        (29, 30): [10],
        (30, 15): [5, 10],
        (30, 30): [10],
        (34, 15): [5, 10, 15],
        (34, 30): [10, 15],
        (34, 60): [10, 15],
        (38, 15): [5, 10, 15, 20, 25, 30, 40],
        (38, 30): [10, 15, 20, 25, 30, 40],
        (38, 60): [10, 15, 20, 25, 30, 40],
        (39, 15): [5, 10, 15, 20, 25, 30, 40],
        (39, 30): [10, 15, 20, 25, 30, 40],
        (39, 60): [10, 15, 20, 25, 30, 40],
        (40, 15): [54, 10, 15, 20, 25, 30, 40, 50],
        (40, 30): [10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100],
        (40, 60): [10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100],
        (41, 15): [58, 10, 15, 20, 25, 30, 35, 40, 45, 50],
        (41, 30): [10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100],
        (41, 60): [10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100],
        (46, 15): [10, 20, 40],
        (46, 30): [10, 20, 40, 60, 80, 100],
        (46, 60): [10, 20, 40, 60, 80, 100],
        (48, 15): [52, 10, 15, 20, 30, 40, 50],
        (48, 30): [10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        (48, 60): [10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        (50, 15): [52, 10, 15, 20, 30, 40, 50],
        (50, 30): [10, 15, 20, 30, 40, 50, 60, 80],
        (50, 60): [10, 15, 20, 30, 40, 50, 60, 80],
        (51, 15): [5],
        (53, 15): [5, 10],
        (53, 30): [10],
        (53, 60): [10],
        (65, 15): [5, 10, 15, 20, 50],
        (65, 30): [10, 15, 20, 50],
        (65, 60): [10, 15, 20, 50],
        (66, 15): [5, 10, 15, 20, 25, 30, 35, 40, 45],
        (66, 30): [10, 15, 20, 25, 30, 35, 40, 45],
        (66, 60): [10, 15, 20, 25, 30, 35, 40, 45],
        (67, 15): [5, 10, 15, 20],
        (67, 30): [10, 15, 20],
        (70, 15): [5, 10, 15, 20, 25],
        (70, 30): [10, 15, 20, 25],
        (70, 60): [10, 15, 20, 25],
        (71, 15): [5, 10, 15, 20, 25, 30, 35],
        (71, 30): [10, 15, 20, 25, 30, 35],
        (74, 15): [5, 10, 15, 20],
        (74, 30): [10, 15, 20],
        (74, 60): [10, 15, 20],
        (75, 15): [5, 10, 15, 20, 25, 30, 40, 50],
        (75, 30): [10, 15, 20, 25, 30, 40, 50],
        (75, 60): [10, 15, 20, 25, 30, 40, 50],
        (76, 15): [5],
        (77, 15): [10, 15, 20, 25, 30, 40, 50],
        (77, 30): [10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100],
        (77, 60): [10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100],
        (78, 15): [10, 15, 20, 25, 30, 40, 50],
        (78, 30): [10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100],
        (78, 60): [10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100],
        (79, 15): [10, 20, 30, 40, 50],
        (79, 30): [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        (79, 60): [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        (80, 15): [5, 10, 15, 20, 25, 30, 40],
        (80, 30): [10, 15, 20, 25, 30, 40],
        (80, 60): [10, 15, 20, 25, 30, 40],
        (81, 15): [5, 10, 15, 20],
        (81, 30): [10, 15, 20],
        (82, 15): [5, 10, 15, 20],
        (82, 30): [10, 15, 20],
        (83, 15): [5, 10, 15, 20, 25, 30, 40],
        (83, 30): [10, 15, 20, 25, 30, 40],
        (84, 15): [5, 10, 15, 20, 25, 30, 40, 50],
        (84, 30): [10, 15, 20, 25, 30, 40, 50],
        (84, 60): [10, 15, 20, 25, 30, 40, 50],
        (85, 15): [5, 10, 15],
        (85, 30): [10, 15],
        (86, 15): [5, 10, 15, 20, 40],
        (86, 30): [10, 15, 20, 40],
        (86, 60): [10, 15, 20, 40],
        (89, 15): [5, 10, 15, 20],
        (89, 30): [10, 15, 20],
        (90, 15): [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
        (90, 30): [10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100],
        (90, 60): [10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100],
        (91, 15): [5, 10],
        (92, 15): [5, 10, 15, 20],
        (92, 30): [10, 15, 20],
        (93, 15): [5, 10],
        (94, 15): [5, 10, 15, 20],
        (94, 30): [10, 15, 20],
        (95, 15): [5, 10, 15],
        (95, 30): [10, 15],
        (95, 60): [10, 15],
        (96, 15): [20, 40],
        (96, 30): [20, 40, 60, 80, 100],
        (96, 60): [20, 40, 60, 80, 100],
        (97, 15): [5, 10, 15, 20, 25, 30, 40, 50],
        (97, 30): [10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100],
        (97, 60): [10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100],
        (98, 15): [5, 10, 15, 20, 25, 30, 40],
        (98, 30): [10, 15, 20, 25, 30, 40],
        (98, 60): [10, 15, 20, 25, 30, 40],
        (99, 15): [5, 10],
        (99, 30): [10],
        (99, 60): [10],
        (100, 15): [5],
        (101, 15): [5, 10],
        (101, 30): [10],
        (102, 15): [20, 40],
        (102, 30): [20, 40, 60, 80, 100],
        (102, 60): [20, 40, 60, 80, 100],
        (104, 15): [20, 30, 40, 50],
        (104, 30): [20, 30, 40, 50, 60, 70, 80, 90, 100],
        (104, 60): [20, 30, 40, 50, 60, 70, 80, 90, 100],
    }

    # TS 38.104 tab. 5.3.5-2
    cbw_per_band_scs_fr2 = {
        (257, 60): [50, 100, 200],
        (257, 120): [50, 100, 200, 400],
        (258, 60): [50, 100, 200],
        (258, 120): [50, 100, 200, 400],
        (259, 60): [50, 100, 200],
        (259, 120): [50, 100, 200, 400],
        (260, 60): [50, 100, 200],
        (260, 120): [50, 100, 200, 400],
        (261, 60): [50, 100, 200],
        (261, 120): [50, 100, 200, 400],
        (262, 60): [50, 100, 200],
        (262, 120): [50, 100, 200, 400],
    }

    # TS 38.104 tab. 5.4.3.3-1
    ss_raster = {
        (1, 15):  {"band": 1,  "scs_ssb": 15, "pattern": "caseA", "gscn_min": 5279, "step": 1, "gscn_max": 5419},
        (2, 15):  {"band": 2,  "scs_ssb": 15, "pattern": "caseA", "gscn_min": 4829, "step": 1, "gscn_max": 4969},
        (3, 15):  {"band": 3,  "scs_ssb": 15, "pattern": "caseA", "gscn_min": 4517, "step": 1, "gscn_max": 4693},
        (5, 15):  {"band": 5,  "scs_ssb": 15, "pattern": "caseA", "gscn_min": 2177, "step": 1, "gscn_max": 2230},
        (5, 30):  {"band": 5,  "scs_ssb": 30, "pattern": "caseB", "gscn_min": 2183, "step": 1, "gscn_max": 2224},
        (7, 15):  {"band": 7,  "scs_ssb": 15, "pattern": "caseA", "gscn_min": 6554, "step": 1, "gscn_max": 6718},
        (8, 15):  {"band": 8,  "scs_ssb": 15, "pattern": "caseA", "gscn_min": 2318, "step": 1, "gscn_max": 2395},
        (12, 15): {"band": 12, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 1828, "step": 1, "gscn_max": 1858},
        (13, 15): {"band": 13, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 1871, "step": 1, "gscn_max": 1885},
        (14, 15): {"band": 14, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 1901, "step": 1, "gscn_max": 1915},
        (18, 15): {"band": 18, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 2156, "step": 1, "gscn_max": 2182},
        (20, 15): {"band": 20, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 1982, "step": 1, "gscn_max": 2047},
        (24, 15): {"band": 24, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 3818, "step": 1, "gscn_max": 3892},
        (24, 30): {"band": 24, "scs_ssb": 30, "pattern": "caseB", "gscn_min": 3824, "step": 1, "gscn_max": 3886},
        (25, 15): {"band": 25, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 4829, "step": 1, "gscn_max": 4981},
        (26, 15): {"band": 26, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 2153, "step": 1, "gscn_max": 2230},
        (28, 15): {"band": 28, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 1901, "step": 1, "gscn_max": 2002},
        (29, 15): {"band": 29, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 1798, "step": 1, "gscn_max": 1813},
        (30, 15): {"band": 30, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 5879, "step": 1, "gscn_max": 5893},
        (34, 15): {"band": 34, "scs_ssb": 15, "pattern": "caseA", "gscn_min": -1,   "step": -1,"gscn_max": -1, "gscn": (5032, 5043, 5054)},
        (34, 30): {"band": 34, "scs_ssb": 30, "pattern": "caseC", "gscn_min": 5036, "step": 1, "gscn_max": 5050},
        (38, 15): {"band": 38, "scs_ssb": 15, "pattern": "caseA", "gscn_min": -1,   "step": -1,"gscn_max": -1, "gscn": (6432, 6443, 6457, 6468, 6479, 6493, 6507, 6518, 6532, 6543)},
        (38, 30): {"band": 38, "scs_ssb": 30, "pattern": "caseC", "gscn_min": 6437, "step": 1, "gscn_max": 6538},
        (39, 15): {"band": 39, "scs_ssb": 15, "pattern": "caseA", "gscn_min": -1,   "step": -1,"gscn_max": -1, "gscn": (4707, 4715, 4718, 4729, 4732, 4743, 4747, 4754, 4761, 4768, 4772, 4782, 4786, 4793)},
        (39, 30): {"band": 39, "scs_ssb": 30, "pattern": "caseC", "gscn_min": 4712, "step": 1, "gscn_max": 4789},
        (40, 30): {"band": 40, "scs_ssb": 30, "pattern": "caseC", "gscn_min": 5762, "step": 1, "gscn_max": 5989},
        (41, 15): {"band": 41, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 6246, "step": 3, "gscn_max": 6717},
        (41, 30): {"band": 41, "scs_ssb": 30, "pattern": "caseC", "gscn_min": 6252, "step": 3, "gscn_max": 6714},
        (46, 30): {"band": 46, "scs_ssb": 30, "pattern": "caseC", "gscn_min": 8993, "step": 1, "gscn_max": 9530, "gscn": (8996, 9010, 9024, 9038, 9051, 9065, 9079, 9093, 9107, 9121, 9218, 9232, 9246, 9260, 9274, 9288, 9301, 9315, 9329, 9343, 9357, 9371, 9385, 9402, 9416, 9430, 9444, 9458, 9472, 9485, 9499, 9513)},
        (48, 30): {"band": 48, "scs_ssb": 30, "pattern": "caseC", "gscn_min": 7884, "step": 1, "gscn_max": 7982},
        (50, 15): {"band": 50, "scs_ssb": 30, "pattern": "caseC", "gscn_min": 3590, "step": 1, "gscn_max": 3781},
        (51, 15): {"band": 51, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 3572, "step": 1, "gscn_max": 3574},
        (53, 15): {"band": 53, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 6215, "step": 1, "gscn_max": 6232},
        (65, 15): {"band": 65, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 5279, "step": 1, "gscn_max": 5494},
        (66, 15): {"band": 66, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 5279, "step": 1, "gscn_max": 5494},
        (66, 30): {"band": 66, "scs_ssb": 30, "pattern": "caseB", "gscn_min": 5285, "step": 1, "gscn_max": 5488},
        (67, 15): {"band": 67, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 1850, "step": 1, "gscn_max": 1888},
        (70, 15): {"band": 70, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 4993, "step": 1, "gscn_max": 5044},
        (71, 15): {"band": 71, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 1547, "step": 1, "gscn_max": 1624},
        (74, 15): {"band": 74, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 3692, "step": 1, "gscn_max": 3790},
        (75, 15): {"band": 75, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 3584, "step": 1, "gscn_max": 3787},
        (76, 15): {"band": 76, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 3572, "step": 1, "gscn_max": 3574},
        (77, 30): {"band": 77, "scs_ssb": 30, "pattern": "caseC", "gscn_min": 7711, "step": 1, "gscn_max": 8329},
        (78, 30): {"band": 78, "scs_ssb": 30, "pattern": "caseC", "gscn_min": 7711, "step": 1, "gscn_max": 8051},
        (79, 30): {"band": 79, "scs_ssb": 30, "pattern": "caseC", "gscn_min": 8480, "step": 16,"gscn_max": 8880},
        #(79, 30): {"band": 79, "scs_ssb": 30, "pattern": "caseC", "gscn_min": 8475, "step": 1, "gscn_max": 8884},
        (85, 15): {"band": 85, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 1826, "step": 1, "gscn_max": 1858},
        (90, 15): {"band": 90, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 6246, "step": 1, "gscn_max": 6717},
        #(90, 15): {"band": 90, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 6245, "step": 1, "gscn_max": 6718],
        (90, 30): {"band": 90, "scs_ssb": 30, "pattern": "caseC", "gscn_min": 6252, "step": 1, "gscn_max": 6714},
        (91, 15): {"band": 91, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 3572, "step": 1, "gscn_max": 3574},
        (92, 15): {"band": 92, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 3584, "step": 1, "gscn_max": 3787},
        (93, 15): {"band": 93, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 3572, "step": 1, "gscn_max": 3574},
        (94, 15): {"band": 94, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 3584, "step": 1, "gscn_max": 3787},
        (96, 30): {"band": 96, "scs_ssb": 30, "pattern": "caseC", "gscn_min": 9531, "step": 1, "gscn_max": 10363, "gscn": (9548, 9562, 9576, 9590, 9603, 9617, 9631, 9645, 9659, 9673, 9687, 9701, 9714, 9728, 9742, 9756, 9770, 9784, 9798, 9812, 9826, 9840, 9853, 9867, 9881, 9895, 9909, 9923, 9937, 9951, 9964, 9978, 9992, 10006, 10020, 10034, 10048, 10062, 10076, 10090, 10103, 10117, 10131, 10145, 10159, 10173, 10187, 10201, 10214, 10228, 10242, 10256, 10270, 10284, 10298, 10312, 10325, 10339, 10353)},
        (100, 15):{"band": 100, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 2303, "step": 1, "gscn_max": 12307},
        (101, 15):{"band": 101, "scs_ssb": 15, "pattern": "caseA", "gscn_min": 4754, "step": 1, "gscn_max": 14768},
        (101, 30):{"band": 101, "scs_ssb": 30, "pattern": "caseC", "gscn_min": 4760, "step": 1, "gscn_max": 14764},
        (102, 30):{"band": 102, "scs_ssb": 30, "pattern": "caseC", "gscn_min": 9531, "step": 1, "gscn_max": 19877, "gscn": (9535, 9548, 9562, 9576, 9590, 9603, 9617, 9631, 9645, 9659, 9673, 9687, 9701, 9714, 9728, 9742, 9756, 9770, 9784, 9798, 9812, 9826, 9840, 9853, 9867)},
        (104, 30):{"band": 104, "scs_ssb": 30, "pattern": "caseC", "gscn_min": 9882, "step": 7, "gscn_max": 710358},
    }
    # TS 38.104 tab. 5.4.3.3-2
    ss_raster_fr2 = {
        (257, 120): {"band": 257, "scs_ssb": 120, "pattern": "caseD", "gscn_min": 22388, "step": 1, "gscn_max": 22558},
        (257, 240): {"band": 257, "scs_ssb": 240, "pattern": "caseE", "gscn_min": 22390, "step": 2, "gscn_max": 22556},
        (258, 120): {"band": 258, "scs_ssb": 120, "pattern": "caseD", "gscn_min": 22257, "step": 1, "gscn_max": 22443},
        (258, 240): {"band": 258, "scs_ssb": 240, "pattern": "caseE", "gscn_min": 22258, "step": 2, "gscn_max": 22442},
        (259, 120): {"band": 259, "scs_ssb": 120, "pattern": "caseD", "gscn_min": 23140, "step": 1, "gscn_max": 23369},
        (259, 240): {"band": 259, "scs_ssb": 240, "pattern": "caseE", "gscn_min": 23142, "step": 2, "gscn_max": 23368},
        (260, 120): {"band": 260, "scs_ssb": 120, "pattern": "caseD", "gscn_min": 22995, "step": 1, "gscn_max": 23166},
        (260, 240): {"band": 260, "scs_ssb": 240, "pattern": "caseE", "gscn_min": 22996, "step": 2, "gscn_max": 23164},
        (261, 120): {"band": 261, "scs_ssb": 120, "pattern": "caseD", "gscn_min": 22446, "step": 1, "gscn_max": 22492},
        (261, 240): {"band": 261, "scs_ssb": 240, "pattern": "caseE", "gscn_min": 22446, "step": 2, "gscn_max": 22490},
        (262, 120): {"band": 262, "scs_ssb": 120, "pattern": "caseD", "gscn_min": 23586, "step": 1, "gscn_max": 23641},
        (262, 240): {"band": 262, "scs_ssb": 240, "pattern": "caseE", "gscn_min": 23588, "step": 2, "gscn_max": 23640},
    }

    @classmethod
    def band_mode(cls, band: int) -> str:
        """Class method returns a duplex mode for a given band

        Args:
            band: NR band

        Returns:
            duplex mode for a given band or empty string if band is incorrect
        """
        return cls.bands.get(band).get("duplex") if cls.bands.get(band) else ""

    @classmethod
    def cbws_in_band(cls, band: int, scs: int) -> List[int]:
        """Class method returns a list of allowed channel bandwidths for a given band and subcarrier spacing

        Args:
            band: NR band
            scs: subcarrier spacing

        Returns:
            list of supported channel bandwidths
        """
        if cls.is_fr1(band):
            return cls.cbw_per_band_scs.get((band, scs), list())
        else:
            return cls.cbw_per_band_scs_fr2.get((band, scs), list())

    @classmethod
    def channel_frequency_raster(cls, band: int, scs: int) -> int:
        """Class method returns channel frequency raster for a given band and subcarrier spacing

        Args:
            band: NR band
            scs: subcarrier spacing

        Returns:
            delta frequency raster
        """
        freq_raster = 100
        if band in (41, 48, 77, 78, 79, 90, 104):
            freq_raster = 15 if scs == 15 else 30
        elif band in (46, 96, 102):
            freq_raster = 15
        elif band in (257, 258, 259, 260, 261, 262):
            freq_raster = 60 if scs == 60 else 120
        return freq_raster

    @classmethod
    def arfcn(cls, freq: int) -> int:
        """Class method calculates arfcn for a given frequency

        Args:
            freq: frequency in kHz

        Returns:
            corresponding arfcn
        """
        freq_raster = cls.global_freq_raster[0]
        if freq >= 24250000:
            freq_raster = cls.global_freq_raster[2]
        elif freq >= 3000000:
            freq_raster = cls.global_freq_raster[1]
        return int(
            freq_raster.get("nref_offset") + (freq - freq_raster.get("freq_offset")) / freq_raster.get("delta_f_global")
        )

    @classmethod
    def frequency(cls, arfcn: int) -> int:
        """Class method calculates a frequency in kHz for a given arfcn

        Args:
            arfcn: arfcn

        Returns:
            corresponding frequency in kHz
        """
        freq_raster = cls.global_freq_raster[0]
        if arfcn >= 2016667:
            freq_raster = cls.global_freq_raster[2]
        elif arfcn >= 600000:
            freq_raster = cls.global_freq_raster[1]
        return freq_raster.get("freq_offset") + freq_raster.get("delta_f_global") * (arfcn - freq_raster["nref_offset"])

    @classmethod
    def channel_raster(cls, band: int = 66, freq_raster: int = 100) -> Dict[str, Any]:
        """Class method returns the channel raster specific parameters for a given band and optionally frequency raster

        It corresponds to the row in TS 38.104 table Table 5.2-1

        Args:
            band: NR band, defaults to n66
            freq_raster: delta_f_raster

        Returns:
            dict with channel raster parameters
        """
        if cls.is_fr1(band):
            return cls.channel_freq_raster.get((band, freq_raster), dict())
        else:
            return cls.channel_freq_raster_fr2.get((band, freq_raster), dict())

    @classmethod
    def f_in_channel_raster(
        cls, f: int, band: int = 66, freq_raster: int = 100, is_ul: bool = False, rounding_f: Callable = round
    ) -> int:
        """Class method for calculating the closest frequency within the channel raster to the given one

        If necessary a rounding function (ceil, floor, round) can be specified

        Args:
            f: input frequency in kHz
            band: NR band, defaults to n66
            freq_raster: delta_f_raster, defaults to 100kHz
            is_ul: flag if a frequency is UL frequency, defaults to False
            rounding_f: python function for rounding, defaults to build-in round

        Returns:
            closest frequency within the channel raster in kHz
        """
        ch_raster = cls.channel_raster(band, freq_raster)
        prefix = "ul_" if is_ul else ""
        freq_l = cls.frequency(ch_raster.get(prefix + "arfcn_low"))
        freq_h = cls.frequency(ch_raster.get(prefix + "arfcn_high"))
        f_cand = rounding_f(f / ch_raster.get("delta_f")) * ch_raster.get("delta_f")
        if f_cand < freq_l:
            return freq_l
        elif f_cand > freq_h:
            return freq_h
        else:
            return f_cand

    @classmethod
    def dl_f_in_channel_raster(cls, f: int, band: int = 66, freq_raster: int = 100) -> int:
        """Class method for calculating the closest dl frequency within the channel raster to the given one

        Args:
            f: input frequency in kHz
            band: NR band, defaults to n66
            freq_raster: delta_f_raster, defaults to 100kHz

        Returns:
            closest dl frequency within the channel raster in kHz
        """
        return cls.f_in_channel_raster(f, band, freq_raster)

    @classmethod
    def dl_f_in_channel_raster_ceil(cls, f: int, band: int = 66, freq_raster: int = 100) -> int:
        """Class method for calculating the closest round-up dl frequency within the channel raster to the given one

        Args:
            f: input frequency in kHz
            band: NR band, defaults to n66
            freq_raster: delta_f_raster, defaults to 100kHz

        Returns:
            closest dl frequency within the channel raster in kHz
        """
        return cls.f_in_channel_raster(f, band, freq_raster, rounding_f=math.ceil)

    @classmethod
    def dl_f_in_channel_raster_floor(cls, f: int, band: int = 66, freq_raster: int = 100) -> int:
        """Class method for calculating the closest round-down dl frequency within the channel raster to the given one

        Args:
            f: input frequency in kHz
            band: NR band, defaults to n66
            freq_raster: delta_f_raster, defaults to 100kHz

        Returns:
            closest dl frequency within the channel raster in kHz
        """
        return cls.f_in_channel_raster(f, band, freq_raster, rounding_f=math.floor)

    @classmethod
    def ul_f_in_channel_raster(cls, f: int, band: int = 66, freq_raster: int = 100) -> int:
        """Class method for calculating the closest ul frequency within the channel raster to the given one

        Args:
            f: input frequency in kHz
            band: NR band, defaults to n66
            freq_raster: delta_f_raster, defaults to 100kHz

        Returns:
            closest ul frequency within the channel raster in kHz
        """
        return cls.f_in_channel_raster(f, band, freq_raster, is_ul=True)

    @classmethod
    def ul_f_in_channel_raster_ceil(cls, f: int, band: int = 66, freq_raster: int = 100) -> int:
        """Class method for calculating the closest round-up ul frequency within the channel raster to the given one

        Args:
            f: input frequency in kHz
            band: NR band, defaults to n66
            freq_raster: delta_f_raster, defaults to 100kHz

        Returns:
            closest ul frequency within the channel raster in kHz
        """
        return cls.f_in_channel_raster(f, band, freq_raster, is_ul=True, rounding_f=math.ceil)

    @classmethod
    def ul_f_in_channel_raster_floor(cls, f: int, band: int = 66, freq_raster: int = 100) -> int:
        """Class method for calculating the closest round down ul frequency within the channel raster to the given one

        Args:
            f: input frequency in kHz
            band: NR band, defaults to n66
            freq_raster: delta_f_raster, defaults to 100kHz

        Returns:
            closest ul frequency within the channel raster in kHz
        """
        return cls.f_in_channel_raster(f, band, freq_raster, is_ul=True, rounding_f=math.floor)

    @classmethod
    def dl_f_from_ul(cls, f: int, band: int = 66, freq_raster: int = 100):
        """Class method for calculating the dl frequency from a given ul frequency

        Args:
            f: ul frequency in kHz
            band: NR band, defaults to n66
            freq_raster: delta_f_raster, defaults to 100kHz

        Returns:
            dl frequency in kHz
        """
        ch_raster = cls.channel_raster(band, freq_raster)
        ul_dl_distance = cls.frequency(ch_raster.get("arfcn_low")) - cls.frequency(ch_raster.get("ul_arfcn_low"))
        return f + ul_dl_distance

    @classmethod
    def ul_f_from_dl(cls, f: int, band: int = 66, freq_raster: int = 100):
        """Class method for calculating the ul frequency from a given dl frequency

        Args:
            f: dl frequency in kHz
            band: NR band, defaults to n66
            freq_raster: delta_f_raster, defaults to 100kHz

        Returns:
            ul frequency in kHz
        """
        ch_raster = cls.channel_raster(band, freq_raster)
        ul_dl_distance = cls.frequency(ch_raster.get("arfcn_low")) - cls.frequency(ch_raster.get("ul_arfcn_low"))
        return f - ul_dl_distance

    @classmethod
    def fc_range(
        cls, scs_carrier: int, channel_bw: int, band: int = 66, freq_raster: int = 100, is_ul: bool = False
    ) -> Tuple[int, int, int]:
        """Class method for calculating carrier frequency range for a given band, channel bandwidth, scs spacing

        Args:
            scs_carrier: carrier subcarrier spacing
            channel_bw: channel bandwidth
            band: NR band, defaults to n66
            freq_raster: delta_f_raster, defaults to 100kHz
            is_ul: flag if calculation shall be done for UL frequencies

        Returns:
            Tuple with min, middle and max frequencies in kHz
        """
        prefix = "ul_" if is_ul else ""
        ch_raster = cls.channel_raster(band, freq_raster)
        freq_l = cls.frequency(ch_raster.get(prefix + "arfcn_low"))
        freq_h = cls.frequency(ch_raster.get(prefix + "arfcn_high"))
        bw = freq_h - freq_l
        cbw, cbw_nrb = cls.cbw(scs_carrier, channel_bw, band=band)
        logger.debug(
            "freq_l:{}, freq_h:{}, bw:{}, cbw:{}, scs_carrier:{}, channel_bw:{}".format(
                freq_l, freq_h, bw, cbw, scs_carrier, channel_bw
            )
        )
        fc_low = math.ceil((freq_l + cbw / 2) / ch_raster.get("delta_f")) * ch_raster.get("delta_f")
        fc_mid = round((freq_l + bw / 2) / ch_raster.get("delta_f")) * ch_raster.get("delta_f")
        fc_high = math.floor((freq_h - cbw / 2) / ch_raster.get("delta_f")) * ch_raster.get("delta_f")
        return fc_low, fc_mid, fc_high

    @classmethod
    def dl_fc_range(
        cls, scs_carrier: int, channel_bw: int, band: int = 66, freq_raster: int = 100
    ) -> Tuple[int, int, int]:
        """Class method for calculating dl carrier frequency range for a given band, channel bandwidth, scs spacing

        Args:
            scs_carrier: carrier subcarrier spacing
            channel_bw: channel bandwidth
            band: NR band, defaults to n66
            freq_raster: delta_f_raster, defaults to 100kHz

        Returns:
            Tuple with min, middle and max frequencies in kHz
        """
        return cls.fc_range(scs_carrier, channel_bw, band, freq_raster, False)

    @classmethod
    def ul_fc_range(
        cls, scs_carrier: int, channel_bw: int, band: int = 66, freq_raster: int = 100
    ) -> Tuple[int, int, int]:
        """Class method for calculating ul carrier frequency range for a given band, channel bandwidth, scs spacing

        Args:
            scs_carrier: carrier subcarrier spacing
            channel_bw: channel bandwidth
            band: NR band, defaults to n66
            freq_raster: delta_f_raster, defaults to 100kHz

        Returns:
            Tuple with min, middle and max frequencies in kHz
        """
        return cls.fc_range(scs_carrier, channel_bw, band, freq_raster, True)

    @classmethod
    def dl_fc_range_from_ul(
        cls, ul_fc_range: Tuple[int, int, int], band: int = 66, freq_raster: int = 100
    ) -> Tuple[int, int, int]:
        """Class method for calculating dl carrier frequency range for a corresponding ul channel frequency range

        Args:
            ul_fc_range: Tuple with min, middle and max ul frequencies in kHz
            band: NR band, defaults to n66
            freq_raster: delta_f_raster, defaults to 100kHz

        Returns:
            Tuple with min, middle and max dl frequencies in kHz corresponding to the given ul range
        """
        ch_raster = cls.channel_raster(band, freq_raster)
        ul_dl_distance = cls.frequency(ch_raster.get("arfcn_low")) - cls.frequency(ch_raster.get("ul_arfcn_low"))
        return tuple(fc + ul_dl_distance for fc in ul_fc_range)

    @classmethod
    def cbw(cls, scs: int, bw: int, band: int = 66) -> Tuple[int, int]:
        """Class method for calculating channel bandwidth size in kHz and n_rbs

        Args:
            scs: subcarrier spacing in kHz
            bw: bandwidth in MHz
            band: NR band, defaults to n66

        Returns:
            Tuple channel bandwitdh size in kHz and n_rbs
        """
        if cls.is_fr1(band):
            _scs = cls.bandwidth.get(scs)
        else:
            _scs = cls.bandwidth_fr2.get(scs)
        cbw_f = 0
        n_rb = 0
        if _scs:
            n_rb = _scs.get(bw, 0)
            if n_rb and n_rb > 0:
                cbw_f = 12 * scs * n_rb
        return cbw_f, n_rb

    @classmethod
    def bw(cls, scs: int = 30, band: int = 66, is_ul: bool = False) -> int:
        """Class method for calculating bandwidth size for a given Band

        Args:
            scs: min(scs_carrier, scs_ssb) in kHz
            band: NB band, defaults to n66
            is_ul: flag indicating if calculation shall be done for UL band, defaults to False

        Returns:
            bandwidth in kHz
        """
        raster = cls.channel_frequency_raster(band=band, scs=scs)
        prefix = "ul_" if is_ul else ""
        ch_raster = cls.channel_raster(band, raster)
        freq_l = cls.frequency(ch_raster.get(prefix + "arfcn_low"))
        freq_h = cls.frequency(ch_raster.get(prefix + "arfcn_high"))
        return freq_h - freq_l

    @classmethod
    def gb(cls, scs: int, bw: int, band: int = 66) -> int:
        """Class method gets the minimum guard band for the given channel bandwidth and subcarrier spacing

        Args:
            scs: subcarrier spacing in kHz
            bw: bandwidth in MHz
            band: NR band, needed to determine FR1 or FR2 ranges, defaults to 66

        Returns:
            minimum guardband in kHz or -1 if not available
        """
        if cls.is_fr1(band):
            _scs = cls.guardband.get(scs)
        else:
            _scs = cls.guardband_fr2.get(scs)
        return _scs.get(bw)

    @classmethod
    def f_band_range(cls, scs: int, band: int = 66, is_ul: bool = False) -> Tuple[int, int]:
        """Class method return the lowest and the highest frequency for a given band

        Args:
            scs: min(scs_carrier, scs_ssb) in kHz
            band: NB band, defaults to n66
            is_ul: flag indicating if calculation shall be done for UL band, defaults to False

        Returns:
            Tuple with lowest and highest frequency in the band in kHz
        """
        raster = cls.channel_frequency_raster(band=band, scs=scs)
        prefix = "ul_" if is_ul else ""
        ch_raster = cls.channel_raster(band, raster)
        freq_l = cls.frequency(ch_raster.get(prefix + "arfcn_low"))
        freq_h = cls.frequency(ch_raster.get(prefix + "arfcn_high"))
        return freq_l, freq_h

    @classmethod
    def dl_f_band_range(cls, scs: int, band: int = 66) -> Tuple[int, int]:
        """lass method return the lowest and the highest dl frequency for a given band

        Args:
            scs: min(scs_carrier, scs_ssb) in kHz
            band: NR band, defaults to n66

        Returns:
            Tuple with lowest and highest frequency in the band in kHz
        """
        return cls.f_band_range(scs=scs, band=band)

    @classmethod
    def ul_f_band_range(cls, scs: int, band: int = 66) -> Tuple[int, int]:
        """lass method return the lowest and the highest ul frequency for a given band

        Args:
            scs: min(scs_carrier, scs_ssb) in kHz
            band: NR band, defaults to n66

        Returns:
            Tuple with lowest and highest frequency in the band in kHz
        """
        return cls.f_band_range(scs=scs, band=band, is_ul=True)

    @classmethod
    def is_fr1(cls, band: int) -> bool:
        """Class method checks if given band is FR1 band

        Args:
            band: NB band, defaults to 66

        Returns:
            True if band belongs to FR1, False otherwise
        """
        return True if cls.channel_freq_raster.get((band, 100)) or cls.channel_freq_raster.get((band, 15)) else False

    @classmethod
    def gscn_raster(cls, scs_ssb: int, band: int = 66) -> Dict[str, Any]:
        """Class method return the sync raster parameters for a given scs and band

        It corresponds to the row in TS 38.104 Table 5.4.3.3-1 and Table 5.4.3.3-2.

        Args:
            scs_ssb: SSB subcarrier spacing in kHz
            band: NR band, default to n66

        Returns:
            dict with sync raster parameters
        """
        if cls.is_fr1(band):
            return cls.ss_raster.get((band, scs_ssb))
        else:
            return cls.ss_raster_fr2.get((band, scs_ssb))

    @classmethod
    def gscn_align_with_raster(cls, gscn: int, scs_ssb: int, band: int, prev: bool = False, next: bool = False) -> int:
        """Class method ensures align the given gscn to the band specific sync raster

        It shifts the gscn up or down to ensure it is within the band sync raster.

        Args:
            gscn: gscn to be aligned
            scs_ssb: SSB subcarrier spacing in kHz
            band: NR band, default to 66
            prev: flag to indicate if alignment shall be done to previous gscn value
            next: flag to indicate if alignment shall be done to next gscn value

        Returns:
            aligned gscn
        """
        gscn_params = cls.gscn_raster(scs_ssb=scs_ssb, band=band)
        gscn_lst = gscn_params.get("gscn", [])
        # handle case where explicit GSCN list it given
        if gscn_lst:
            logger.info("Fixed GSCN list available (for band:{}, scs_ssb:{})".format(band, scs_ssb))
            gscn_min = gscn_lst[0]
            gscn_max = gscn_lst[-1]
            try:
                gscn_inx = next(x for x, val in enumerate(gscn_lst) if val >= gscn)
                if gscn_inx == 0:
                    logger.info(
                        "Selected gscn:{} is lower than or equal gscn_min:{} (for band:{}, scs_ssb:{})".format(
                            gscn, gscn_min, band, scs_ssb
                        )
                    )
            except StopIteration as e:
                logger.info(
                    "Selected gscn:{} is greater than gscn_max:{} (for band:{}, scs_ssb:{})".format(
                        gscn, gscn_max, band, scs_ssb
                    )
                )
                gscn_inx = len(gscn_lst) - 1
            if next and gscn_inx < len(gscn_lst) - 1:
                gscn_inx += 1
            elif prev and gscn_inx > 0:
                gscn_inx -= 1
            logger.info(f"Selecting gscn:{gscn} (fixed list index: {gscn_inx})")
            gscn = gscn_lst[gscn_inx]
        # handle case where min, max and step is given
        else:
            gscn_min = gscn_params.get("gscn_min")
            gscn_max = gscn_params.get("gscn_max")
            gscn_step = gscn_params.get("step")
            gscn = math.ceil(gscn / gscn_step) * gscn_step
            if next:
                gscn = gscn + gscn_step
            elif prev:
                gscn = gscn - gscn_step
            if gscn > gscn_max:
                logger.info(
                    "Selected gscn:{} is greater than gscn_max:{} (for band:{}, scs_ssb:{})".format(
                        gscn, gscn_max, band, scs_ssb
                    )
                )
                logger.info("Selecting gscn_max:{}".format(gscn_max))
                gscn = gscn_max
            elif gscn < gscn_min:
                logger.info(
                    "Selected gscn:{} is lower than gscn_min:{} (for band:{}, scs_ssb:{})".format(
                        gscn, gscn_min, band, scs_ssb
                    )
                )
                logger.info("Selecting gscn_min:{}".format(gscn_min))
                gscn = gscn_min

        return gscn

    @classmethod
    def gscn_next(cls, gscn: int, scs_ssb: int, band: int) -> int:
        """Class method aligns the gscn up

        Args:
            gscn: gscn to be aligned
            scs_ssb: SSB subcarrier spacing in kHz
            band: NR band, default to 66

        Returns:
            aligned gscn
        """
        return cls.gscn_align_with_raster(gscn=gscn, scs_ssb=scs_ssb, band=band, next=True)

    @classmethod
    def gscn_prev(cls, gscn: int, scs_ssb: int, band: int) -> int:
        """Class method aligns the gscn down

        Args:
            gscn: gscn to be aligned
            scs_ssb: SSB subcarrier spacing in kHz
            band: NR band, default to 66
            prev: flag to indicate if alignment shall be done to previous gscn value
            next: flag to indicate if alignment shall be done to next gscn value

        Returns:
            aligned gscn
        """
        return cls.gscn_align_with_raster(gscn=gscn, scs_ssb=scs_ssb, band=band, prev=True)

    @classmethod
    def gscn_to_f(cls, gscn: int, freq_raster: int = 100) -> int:
        """Class method converts gscn to SSB frequency in kHz

        Args:
            gscn: gscn to be aligned
            freq_raster: delta frequency raster in kHz, defaults to 100

        Returns:
            corresponding frequency in kHz
        """
        f_ssb = 0
        if 2 <= gscn < 7499:
            m = (1, 3, 5) if freq_raster == 100 else (3,)
            for i in m:
                n = (gscn - (i - 3) / 2) / 3
                if n.is_integer():
                    f_ssb = n * 1200 + i * 50
        elif 7499 <= gscn < 22256:
            n = gscn - 7499
            f_ssb = 3000000 + n * 1440
        elif 22256 <= gscn <= 26639:
            n = gscn - 22256
            f_ssb = 24250080 + n * 17280
        return int(f_ssb)

    @classmethod
    def f_to_gscn(cls, f_ssb: int, freq_raster: int = 100, rounding_f: Callable = math.ceil) -> int:
        """Class method converts SSB frequency in kHz to gscn

        Args:
            f_ssb: SSB frequency in kHz
            freq_raster: delta frequency raster in kHz, defaults to 100
            rounding_f: python rounding function, defaults to math.ceil

        Returns:
            corresponding frequency in kHz
        """
        gscn = 0
        if f_ssb < 3000000:
            m = (1, 3, 5) if freq_raster == 100 else (3,)
            f_gscn = {}
            for i in m:
                _n = rounding_f((f_ssb - i * 50) / 1200)
                _gscn = 3 * _n + (i - 3) / 2
                _f_ssb = cls.gscn_to_f(_gscn, freq_raster)
                if _f_ssb - f_ssb >= 0:
                    f_gscn.update({_f_ssb - f_ssb: _gscn})
            if f_gscn:
                k = sorted(f_gscn.keys())
                gscn = f_gscn.get(k[0])
        elif 3000000 <= f_ssb < 24250000:
            n = rounding_f((f_ssb - 3000000) / 1440)
            gscn = 7499 + n
        elif 24250000 <= f_ssb <= 100000000:
            n = rounding_f((f_ssb - 24250080) / 17280)
            gscn = 22256 + n
        return int(gscn)

    @classmethod
    def max_location_and_bw(cls, rb_start: int = 0, scs: int = 30, bw: int = 100, band: int = 66) -> int:
        """Class method calculates the max RIV for a given parameters

        Args:
            rb_start: starr RB number
            scs: subcarrier spacing in kHz
            bw: bandwidth in MHz, defaults to 100
            band: NR band, default to n66

        Returns:
            calculated RIV
        """
        n_size_bwp = 275
        cbw_f, l_rb = cls.cbw(scs=scs, bw=bw, band=band)
        riv = 0
        if 0 < l_rb <= (n_size_bwp - rb_start):
            if (l_rb - 1) <= int(math.floor(n_size_bwp / 2)):
                riv = n_size_bwp * (l_rb - 1) + rb_start
            else:
                riv = n_size_bwp * (n_size_bwp - l_rb + 1) + (n_size_bwp - 1 - rb_start)
        return riv


class CoresetZero:
    """Class holding correset0 parameters tables from 38.213 sec 13

    (TS 38.104
    """

    # TS 38.213 Tab 13-1, 13-4
    tab_fr1 = {
        (15, 15): [
            {"pattern": 1, "n_rb": 24, "n_sym": 2, "offset": 0},
            {"pattern": 1, "n_rb": 24, "n_sym": 2, "offset": 2},
            {"pattern": 1, "n_rb": 24, "n_sym": 2, "offset": 4},
            {"pattern": 1, "n_rb": 24, "n_sym": 3, "offset": 0},
            {"pattern": 1, "n_rb": 24, "n_sym": 3, "offset": 2},
            {"pattern": 1, "n_rb": 24, "n_sym": 3, "offset": 4},
            {"pattern": 1, "n_rb": 48, "n_sym": 1, "offset": 12},
            {"pattern": 1, "n_rb": 48, "n_sym": 1, "offset": 16},
            {"pattern": 1, "n_rb": 48, "n_sym": 2, "offset": 12},
            {"pattern": 1, "n_rb": 48, "n_sym": 2, "offset": 16},
            {"pattern": 1, "n_rb": 48, "n_sym": 3, "offset": 12},
            {"pattern": 1, "n_rb": 48, "n_sym": 3, "offset": 16},
            {"pattern": 1, "n_rb": 96, "n_sym": 1, "offset": 38},
            {"pattern": 1, "n_rb": 96, "n_sym": 2, "offset": 38},
            {"pattern": 1, "n_rb": 96, "n_sym": 3, "offset": 38},
        ],
        (15, 30): [
            {"pattern": 1, "n_rb": 24, "n_sym": 2, "offset": 5},
            {"pattern": 1, "n_rb": 24, "n_sym": 2, "offset": 6},
            {"pattern": 1, "n_rb": 24, "n_sym": 2, "offset": 7},
            {"pattern": 1, "n_rb": 24, "n_sym": 2, "offset": 8},
            {"pattern": 1, "n_rb": 24, "n_sym": 3, "offset": 5},
            {"pattern": 1, "n_rb": 24, "n_sym": 3, "offset": 6},
            {"pattern": 1, "n_rb": 24, "n_sym": 3, "offset": 7},
            {"pattern": 1, "n_rb": 24, "n_sym": 3, "offset": 8},
            {"pattern": 1, "n_rb": 48, "n_sym": 1, "offset": 18},
            {"pattern": 1, "n_rb": 48, "n_sym": 1, "offset": 20},
            {"pattern": 1, "n_rb": 48, "n_sym": 2, "offset": 18},
            {"pattern": 1, "n_rb": 48, "n_sym": 2, "offset": 20},
            {"pattern": 1, "n_rb": 48, "n_sym": 3, "offset": 18},
            {"pattern": 1, "n_rb": 48, "n_sym": 3, "offset": 20},
        ],
        (30, 15): [
            {"pattern": 1, "n_rb": 48, "n_sym": 1, "offset": 2},
            {"pattern": 1, "n_rb": 48, "n_sym": 1, "offset": 6},
            {"pattern": 1, "n_rb": 48, "n_sym": 2, "offset": 2},
            {"pattern": 1, "n_rb": 48, "n_sym": 2, "offset": 6},
            {"pattern": 1, "n_rb": 48, "n_sym": 3, "offset": 2},
            {"pattern": 1, "n_rb": 48, "n_sym": 3, "offset": 6},
            {"pattern": 1, "n_rb": 96, "n_sym": 1, "offset": 28},
            {"pattern": 1, "n_rb": 96, "n_sym": 2, "offset": 28},
            {"pattern": 1, "n_rb": 96, "n_sym": 3, "offset": 28},
        ],
        (30, 30): [
            {"pattern": 1, "n_rb": 24, "n_sym": 2, "offset": 0},
            {"pattern": 1, "n_rb": 24, "n_sym": 2, "offset": 1},
            {"pattern": 1, "n_rb": 24, "n_sym": 2, "offset": 2},
            {"pattern": 1, "n_rb": 24, "n_sym": 2, "offset": 3},
            {"pattern": 1, "n_rb": 24, "n_sym": 2, "offset": 4},
            {"pattern": 1, "n_rb": 24, "n_sym": 3, "offset": 0},
            {"pattern": 1, "n_rb": 24, "n_sym": 3, "offset": 1},
            {"pattern": 1, "n_rb": 24, "n_sym": 3, "offset": 2},
            {"pattern": 1, "n_rb": 24, "n_sym": 3, "offset": 3},
            {"pattern": 1, "n_rb": 24, "n_sym": 3, "offset": 4},
            {"pattern": 1, "n_rb": 48, "n_sym": 1, "offset": 12},
            {"pattern": 1, "n_rb": 48, "n_sym": 1, "offset": 14},
            {"pattern": 1, "n_rb": 48, "n_sym": 1, "offset": 16},
            {"pattern": 1, "n_rb": 48, "n_sym": 2, "offset": 12},
            {"pattern": 1, "n_rb": 48, "n_sym": 2, "offset": 14},
            {"pattern": 1, "n_rb": 48, "n_sym": 2, "offset": 16},
        ],
    }
    # TS 38.213 Tab 13-5, 13-6
    tab_fr1_min40 = {
        (30, 15): [
            {"pattern": 1, "n_rb": 48, "n_sym": 1, "offset": 4},
            {"pattern": 1, "n_rb": 48, "n_sym": 2, "offset": 4},
            {"pattern": 1, "n_rb": 48, "n_sym": 3, "offset": 4},
            {"pattern": 1, "n_rb": 96, "n_sym": 1, "offset": 0},
            {"pattern": 1, "n_rb": 96, "n_sym": 1, "offset": 56},
            {"pattern": 1, "n_rb": 96, "n_sym": 2, "offset": 0},
            {"pattern": 1, "n_rb": 96, "n_sym": 2, "offset": 56},
            {"pattern": 1, "n_rb": 96, "n_sym": 3, "offset": 0},
            {"pattern": 1, "n_rb": 96, "n_sym": 3, "offset": 56},
        ],
        (30, 30): [
            {"pattern": 1, "n_rb": 24, "n_sym": 2, "offset": 0},
            {"pattern": 1, "n_rb": 24, "n_sym": 2, "offset": 4},
            {"pattern": 1, "n_rb": 24, "n_sym": 3, "offset": 0},
            {"pattern": 1, "n_rb": 24, "n_sym": 3, "offset": 4},
            {"pattern": 1, "n_rb": 48, "n_sym": 1, "offset": 0},
            {"pattern": 1, "n_rb": 48, "n_sym": 1, "offset": 28},
            {"pattern": 1, "n_rb": 48, "n_sym": 2, "offset": 0},
            {"pattern": 1, "n_rb": 48, "n_sym": 2, "offset": 28},
            {"pattern": 1, "n_rb": 48, "n_sym": 3, "offset": 0},
            {"pattern": 1, "n_rb": 48, "n_sym": 3, "offset": 28},
        ],
    }

    tab_fr2 = {
        (120, 60): [
            {"pattern": 1, "n_rb": 48, "n_sym": 1, "offset": 0},
            {"pattern": 1, "n_rb": 48, "n_sym": 1, "offset": 8},
            {"pattern": 1, "n_rb": 48, "n_sym": 2, "offset": 0},
            {"pattern": 1, "n_rb": 48, "n_sym": 2, "offset": 8},
            {"pattern": 1, "n_rb": 48, "n_sym": 3, "offset": 0},
            {"pattern": 1, "n_rb": 48, "n_sym": 3, "offset": 8},
            {"pattern": 1, "n_rb": 96, "n_sym": 1, "offset": 28},
            {"pattern": 1, "n_rb": 96, "n_sym": 2, "offset": 28},
            {"pattern": 2, "n_rb": 48, "n_sym": 1, "offset": -41},
            {"pattern": 2, "n_rb": 48, "n_sym": 1, "offset": 49},
            {"pattern": 2, "n_rb": 96, "n_sym": 1, "offset": -41},
            {"pattern": 2, "n_rb": 96, "n_sym": 1, "offset": 97},
        ],
        (120, 120): [
            {"pattern": 1, "n_rb": 24, "n_sym": 2, "offset": 0},
            {"pattern": 1, "n_rb": 24, "n_sym": 2, "offset": 4},
            {"pattern": 1, "n_rb": 48, "n_sym": 1, "offset": 14},
            {"pattern": 1, "n_rb": 48, "n_sym": 2, "offset": 14},
            {"pattern": 3, "n_rb": 24, "n_sym": 2, "offset": -20},
            {"pattern": 3, "n_rb": 24, "n_sym": 2, "offset": 24},
            {"pattern": 3, "n_rb": 48, "n_sym": 2, "offset": -20},
            {"pattern": 3, "n_rb": 48, "n_sym": 2, "offset": 48},
        ],
        (240, 60): [
            {"pattern": 1, "n_rb": 96, "n_sym": 1, "offset": 0},
            {"pattern": 1, "n_rb": 96, "n_sym": 1, "offset": 16},
            {"pattern": 1, "n_rb": 96, "n_sym": 2, "offset": 0},
            {"pattern": 1, "n_rb": 96, "n_sym": 2, "offset": 16},
        ],
        (240, 120): [
            {"pattern": 1, "n_rb": 48, "n_sym": 1, "offset": 0},
            {"pattern": 1, "n_rb": 48, "n_sym": 1, "offset": 8},
            {"pattern": 1, "n_rb": 48, "n_sym": 2, "offset": 0},
            {"pattern": 1, "n_rb": 48, "n_sym": 2, "offset": 8},
            {"pattern": 2, "n_rb": 24, "n_sym": 1, "offset": -41},
            {"pattern": 2, "n_rb": 24, "n_sym": 1, "offset": 25},
            {"pattern": 2, "n_rb": 48, "n_sym": 1, "offset": -41},
            {"pattern": 2, "n_rb": 48, "n_sym": 1, "offset": 49},
        ],
    }

    @classmethod
    def coreset_zero(
        cls, inx: int = 0, scs_ssb: int = 30, scs: int = 30, is_fr1: bool = True, is_min40: bool = False
    ) -> Dict[str, Any]:
        """Class method returns the coreset0 specific parameters for a given coreset0 index, scs_ssb, scs

        It corresponds to the row in TS 38.104 table Table 5.2-1

        Args:
            inx: coreset0 index, defaults to 0
            scs_ssb: SSB subcarrier spacing in kHz, default to 30
            scs: subcarrier spacing in kHz, defaults to 30
            is_fr1: flag indicates if tables for FR1 shall be checked, defaults to True
            is_min40: falg indicates if table for FR1 and min channel bandwidth of 40MHz shall be used

         Returns:
            dict with coreset0 parameters
        """
        if not is_fr1:
            tab = cls.tab_fr2.get((scs_ssb, scs), list())
        elif is_min40:
            tab = cls.tab_fr1_min40.get((scs_ssb, scs), list())
        else:
            tab = cls.tab_fr1.get((scs_ssb, scs), list())
        if len(tab) > inx:
            logger.info("{}".format(tab))
            return tab[inx]
        else:
            return dict()

    @classmethod
    def freq_domain_res(cls, n_rb: int = 24) -> str:
        """Class method the common coreset frequency domain resource map based on a given n_rb

        It corresponds to the row in TS 38.104 table Table 5.2-1

        Args:
            n_rb: number of RBs for a common coreset

         Returns:
            bitmap as string
        """
        f_domain_res = "111100000000000000000000000000000000000000000"
        if n_rb == 48:
            f_domain_res = "111111110000000000000000000000000000000000000"
        elif n_rb == 96:
            f_domain_res = "111111111111111100000000000000000000000000000"
        return f_domain_res


class CaConfig:
    """Class for carrier aggregation related calculations

    It provides class methods for carrier aggregation related parameters e.g. nominal channel spacing, guardbands etc.
    calculations

    """

    @classmethod
    def mi_zero(cls, bw_c1: int, bw_c2: int, band: int) -> int:
        _mi_zero = -1
        for scs in (240, 120, 60, 30, 15):
            logger.info(
                "checking mi_zero for {} in {}".format(
                    set([bw_c1, bw_c2]), set(NrArfcn.cbws_in_band(band=band, scs=scs))
                )
            )
            if set([bw_c1, bw_c2]).issubset(set(NrArfcn.cbws_in_band(band=band, scs=scs))):
                _mi_zero = Numerology.mi(scs)
                logger.info("Found mi_zero: {}".format(_mi_zero))
                break
        return _mi_zero

    @classmethod
    def nominal_spacing(cls, bw_c1: int, bw_c2: int, scs_c1: int, scs_c2: int, band: int) -> int:
        """Class method calculates nominal channel spacing for two contiguous channel bandwidths

        The formula originates from TS 38.104 sec. 5.4.1.2

        Args:
            bw_c1: 1st channel bandwidth
            bw_c2: 2nd channel bandwidth
            scs_c1: subcarrier spacing of the 1st channel bandwidth
            scs_c1: subcarrier spacing of the 2nd channel bandwidth
            band: Nr band

         Returns:
            calculated nominal spacing in kHz, -1 if input parameters incorrect
        """
        logger.info(
            "Calculating nominal channel spacing for band:{}, channel_bandwidth pair:({}, {})"
            " and subcarrier_spacing pair:({}, {})".format(band, bw_c1, bw_c2, scs_c1, scs_c2)
        )
        gb_c1 = NrArfcn.gb(scs=scs_c1, bw=bw_c1, band=band)
        gb_c2 = NrArfcn.gb(scs=scs_c2, bw=bw_c2, band=band)
        if gb_c1 == -1:
            logger.warning(
                "Cannot determine guardband for band:{}, channel_bandwidth:{} and subcarrier_spacing:{}".format(
                    band, bw_c1, scs_c1
                )
            )
            return -1
        if gb_c2 == -1:
            logger.warning(
                "Cannot determine guardband for band:{}, channel_bandwidth:{} and subcarrier_spacing:{}".format(
                    band, bw_c2, scs_c2
                )
            )
            return -1

        freq_raster = NrArfcn.channel_frequency_raster(band=band, scs=min(scs_c1, scs_c2))
        nom_spacing = -1
        if (freq_raster % 60) == 0:
            mi_zero = cls.mi_zero(bw_c1=bw_c1, bw_c2=bw_c2, band=band)
            if mi_zero != -1:
                nom_spacing = (
                    math.floor((bw_c1 + bw_c2 - 2 * abs(gb_c1 - gb_c2) / 1000) / (0.06 * 2 ** (mi_zero - 1)))
                    * 60
                    * 2 ** (mi_zero - 2)
                )
        elif (freq_raster % 15) == 0:
            mi_zero = cls.mi_zero(bw_c1=bw_c1, bw_c2=bw_c2, band=band)
            if mi_zero != -1:
                nom_spacing = (
                    math.floor((bw_c1 + bw_c2 - 2 * abs(gb_c1 - gb_c2) / 1000) / (0.015 * 2 ** (mi_zero + 1)))
                    * 15
                    * 2**mi_zero
                )
        else:
            nom_spacing = math.floor((bw_c1 + bw_c2 - 2 * abs(gb_c1 - gb_c2)) / 0.6) * 300

        if nom_spacing > -1:
            logger.info("Calculated nominal channel spacing is {} kHz".format(nom_spacing))
        else:
            logger.warning("Could not determine the nominal channel spacing. Check input parameters")
        return nom_spacing

    @classmethod
    def intra_cont_channel_spacing(cls, nom_channel_spacing: int, band: int, scs: int) -> List[int]:
        """Class method calculates the allowed channel spacing values for intra band contiguous ca based on teh given
        nominal channel spacing

        Currently the 3 largest values are returned

        Args:
            nom_channel_spacing: nominal channel spacing for CA
            band: Nr band
            scs: subcarrier spacing

         Returns:
            calculated list of allowed channel spacing values
        """
        allowed_channel_spacings = [nom_channel_spacing]
        freq_raster = NrArfcn.channel_frequency_raster(band=band, scs=scs)
        if freq_raster > -1:
            _lcm = lcm(scs, freq_raster)
            _cs = (nom_channel_spacing // _lcm) * _lcm
            # save just 3 values for starter
            i = 3
            while i > 0 and _cs > 0:
                allowed_channel_spacings.append(_cs)
                _cs -= _lcm
                i -= 1
        return allowed_channel_spacings


class Config:
    """Class for calculation of the optimal frequency settings

    It takes only a few optional input parameters in a form of a profile and performs all necessary calculations to
    find the most optimal scenario settings.

    The implementation is based on the TS 38.104 and TS 38.508. Currently parameters are calculated with the assumption
    the Coreset0 and SS Block should be as close as possible (Coreset0 shall start with the start of iniBWP)
    to the beginning of the BWP.

    All the input and output frequencies are expressed in kHz.

    Example::

        >>> c = Config(param={'scs_ssb': 30, 'scs_common': 15, 'scs_carrier': 15, 'fc_channel': 3750000,
        ...                  'band': 77, 'bw': 50, 'pdcchConfigSib1': 4, 'offset_to_carrier': 0})
        >>> cell_params = c.calculate()

    Args:
        param: dictionary with option input parameters

    """

    def __init__(self, param: Dict[str, Any] = None):
        if param is None:
            param = dict()
        self._input_param_error = False
        self.band = param.get("band", 66)
        self.duplex = NrArfcn.band_mode(self.band)
        self.scs_carrier = param.get("scs_carrier", 30)
        self.scs_common = param.get("scs_common", 30)
        self.bw = param.get("bw", 40)
        self.bw_ul = param.get("bw_ul")
        self.fc_channel_dl = param.get("fc_channel")
        self.fc_channel_ul = param.get("fc_channel_ul")
        if param.get("SsbTransmission", "enabled") == "enabled" and not self.is_sul:
            self.ssb_enabled = True
        else:
            self.ssb_enabled = False
        self.offset_to_carrier = param.get("offset_to_carrier", 0)
        self.f_fc_to_point_a = param.get("f_fc_to_point_a", 49140)
        if not self.is_sul:
            self.scs_ssb = param.get("scs_ssb", 30)
            self.pdcch_cfg_sib1 = param.get("pdcchConfigSib1", 164)
            self.use_sync_raster = param.get("use_sync_raster", True)
            self.gscn = 0
            self.f_ss = 0
        # initialize parameters
        self._init_params()

    @property
    def is_sul(self):
        return NrArfcn.band_mode(self.band) in ("SUL",)

    @property
    def is_sdl(self):
        return NrArfcn.band_mode(self.band) in ("SDL",)

    @property
    def min_scs(self):
        return self.scs_carrier if self.is_sul else min(self.scs_carrier, self.scs_ssb)

    def _freq_raster(self):
        self.freq_raster = NrArfcn.channel_frequency_raster(band=self.band, scs=self.min_scs)

    def _pdcch_cfg_sib1(self):
        inx = self.pdcch_cfg_sib1 >> 4
        is_min40 = True if self.band in (79,) else False
        is_fr1 = NrArfcn.is_fr1(self.band)
        cr_zero = CoresetZero.coreset_zero(
            inx=inx, scs_ssb=self.scs_ssb, scs=self.scs_carrier, is_fr1=is_fr1, is_min40=is_min40
        )

        if not cr_zero:
            self._input_param_error = True
            logger.warning(
                "Could not find the CoresetZero RB settings for table index:{}, scs_ssb:{}, scs:{}, band:{}".format(
                    inx, self.scs_ssb, self.scs_carrier, self.band
                )
            )
            logger.warning("Using CoresetZero RB settings table index:0")
            cr_zero = CoresetZero.coreset_zero(
                inx=0, scs_ssb=self.scs_ssb, scs=self.scs_carrier, is_fr1=is_fr1, is_min40=is_min40
            )

        self.offset_rb = cr_zero.get("offset")
        self.f_offset_rb = 12 * self.offset_rb * self.scs_common
        self.n_rb_coreset0 = cr_zero.get("n_rb")
        self.f_domain_res = CoresetZero.freq_domain_res(self.n_rb_coreset0)
        self.n_sym_coreset0 = cr_zero.get("n_sym")

    def _fc_dl_net(self):
        self.fc_dl = int(self.fc_channel_dl + self.f_fc_to_point_a - self.f_off_to_carrier - self.cbw_dl / 2)
        logger.info("Setting DL center frequency to {}".format(self.fc_dl))
        if self.fc_dl > self.band_dl_f_range[1]:
            logger.warning(
                "DL center frequency({}) is outside the band range ({} - {}). \
            Consider using different offset_to_carrier or fc_channel.".format(
                    self.fc_dl, self.band_dl_f_range[0], self.band_dl_f_range[1]
                )
            )

    def _fc_ul_net(self):
        self.fc_ul = int(self.fc_channel_ul + self.f_fc_to_point_a - self.f_off_to_carrier - self.cbw_ul / 2)
        logger.info("Setting UL center frequency to {}".format(self.fc_ul))
        if self.fc_ul > self.band_ul_f_range[1]:
            logger.warning(
                "UL center frequency({}) is outside the band range ({} - {}). \
            Consider using different offset_to_carrier or fc_channel.".format(
                    self.fc_ul, self.band_ul_f_range[0], self.band_ul_f_range[1]
                )
            )

    def _init_fc_dl(self):
        logger.info("Adjusting Dl channel frequency to be in channel raster")
        self.fc_channel_dl = NrArfcn.dl_f_in_channel_raster(
            f=self.fc_channel_dl, band=self.band, freq_raster=self.freq_raster
        )
        self.fc_channel_dl_low = self.fc_channel_dl_range[0]
        self.fc_channel_dl_high = self.fc_channel_dl_range[2]
        logger.debug("DL fc range:{}, fc_dl: {}".format(self.fc_channel_dl_range, self.fc_channel_dl))
        if self.fc_channel_dl_low > self.fc_channel_dl:
            self._input_param_error = True
            logger.warning(
                "DL FC:{} not in the allowed fc range "
                "({},{}) for the selected BW:{}".format(
                    self.fc_channel_dl, self.fc_channel_dl_low, self.fc_channel_dl_high, self.bw
                )
            )
            logger.info("Setting DL FC to {}".format(self.fc_channel_dl_low))

            self.fc_channel_dl = self.fc_channel_dl_low
        elif self.fc_channel_dl_high < self.fc_channel_dl:
            self._input_param_error = True
            logger.warning(
                "DL FC:{} not in the allowed fc range "
                "({},{}) for the selected BW:{}".format(
                    self.fc_channel_dl, self.fc_channel_dl_low, self.fc_channel_dl_high, self.bw
                )
            )
            logger.info("Setting DL FC to {}".format(self.fc_channel_dl_high))
            self.fc_channel_dl = self.fc_channel_dl_high
        # set initial net side dl center frequency
        self._fc_dl_net()

    def _init_fc_ul(self):
        logger.info("Adjusting Ul channel frequency to be in channel raster")
        self.fc_channel_ul = NrArfcn.ul_f_in_channel_raster(
            f=self.fc_channel_ul, band=self.band, freq_raster=self.freq_raster
        )
        self.fc_channel_ul_low = self.fc_channel_ul_range[0]
        self.fc_channel_ul_high = self.fc_channel_ul_range[2]
        logger.debug("UL FC range:{}, fc_ul: {}".format(self.fc_channel_ul_range, self.fc_channel_ul))
        if self.fc_channel_ul_low > self.fc_channel_ul:
            self._input_param_error = True
            logger.warning(
                "UL FC:{} not in the allowed fc range ({},{}) "
                "for the selected BW:{}".format(
                    self.fc_channel_ul, self.fc_channel_ul_low, self.fc_channel_ul_high, self.bw_ul
                )
            )
            logger.info("Setting UL FC to {}".format(self.fc_channel_ul_low))
            self.fc_channel_ul = self.fc_channel_ul_low
        elif self.fc_channel_ul_high < self.fc_channel_ul:
            self._input_param_error = True
            logger.warning(
                "UL FC:{} not in the allowed fc range ({},{}) "
                "for the selected BW:{}".format(
                    self.fc_channel_ul, self.fc_channel_ul_low, self.fc_channel_ul_high, self.bw_ul
                )
            )
            logger.info("Setting UL FC to {}".format(self.fc_channel_ul_high))
            self.fc_channel_ul = self.fc_channel_ul_high
        # set initial net side ul center frequency
        self._fc_ul_net()

    def _k_ssb_max(self):
        if self.scs_carrier == 15:
            # self.k_ssb_max = 23
            self.k_ssb_max = 11
        elif self.scs_carrier == 30:
            self.k_ssb_max = 22
        else:
            self.k_ssb_max = 11

    def _init_params(self):
        self._freq_raster()
        self.f_off_to_carrier = self.offset_to_carrier * self.scs_carrier * 12
        self.rb_size = 12 * self.scs_carrier
        self.rb_6_size = 6 * self.rb_size
        self.offset_coreset0_carrier = 0
        self.scs_carrier_num = Numerology.mi(self.scs_carrier)
        self.scs_common_num = Numerology.mi(self.scs_common)

        if not self.is_sul:
            self.f_point_a = 0
            self.arfcn_point_a = 0
            self.offset_to_pa = 0
            self._pdcch_cfg_sib1()
            self._k_ssb_max()
            self.cbw_dl, self.cbw_dl_nrb = NrArfcn.cbw(scs=self.scs_carrier, bw=self.bw, band=self.band)
            self.band_bw_dl = NrArfcn.bw(scs=self.min_scs, band=self.band)
            self.band_dl_f_range = NrArfcn.dl_f_band_range(scs=self.min_scs, band=self.band)
            self.fc_channel_dl_range = NrArfcn.dl_fc_range(
                scs_carrier=self.scs_carrier, channel_bw=self.bw, band=self.band, freq_raster=self.freq_raster
            )
            self._init_fc_dl()
            self.bw_ssb = 12 * 20 * self.scs_ssb
            self.scs_kssb = 15 if self.scs_common in (15, 30) else self.scs_common  # TS 38.211 sec. 7.4.3.1
            self.scs_ssb_num = Numerology.mi(self.scs_ssb)
            self.k_ssb = 0
            self.arfcn_ssb = 0
            self.ssb_pattern = NrArfcn.gscn_raster(scs_ssb=self.scs_ssb, band=self.band).get("pattern")
            self.max_location_and_bw_dl = NrArfcn.max_location_and_bw(scs=self.scs_carrier, bw=self.bw, band=self.band)

        if not self.is_sdl:
            self.f_point_a_ul = 0
            self.arfcn_point_a_ul = 0
            if self.fc_channel_ul is None:
                logger.info("Setting Ul channel frequency based on DL channel frequency")
                self.fc_channel_ul = NrArfcn.ul_f_from_dl(
                    f=self.fc_channel_dl, band=self.band, freq_raster=self.freq_raster
                )
            if self.bw_ul is None:
                logger.info("Setting Ul channel bandwidth equal to Dl channel bandwidth")
                self.bw_ul = self.bw
            self.cbw_ul, self.cbw_ul_nrb = NrArfcn.cbw(scs=self.scs_carrier, bw=self.bw_ul, band=self.band)
            self.band_bw_ul = NrArfcn.bw(scs=self.min_scs, band=self.band, is_ul=True)
            self.band_ul_f_range = NrArfcn.ul_f_band_range(scs=self.min_scs, band=self.band)
            self.fc_channel_ul_range = NrArfcn.ul_fc_range(
                scs_carrier=self.scs_carrier, channel_bw=self.bw_ul, band=self.band, freq_raster=self.freq_raster
            )
            self._init_fc_ul()
            self.max_location_and_bw_ul = NrArfcn.max_location_and_bw(scs=self.scs_carrier, bw=self.bw_ul, band=self.band)

    def f_ssb_min(self) -> int:
        logger.debug(
            "fc_dl:{}, cwb_dl:{}, bw_ssb:{}, f_offset_rb:{}".format(
                self.fc_channel_dl, self.cbw_dl, self.bw_ssb, self.offset_rb * 12 * self.scs_carrier
            )
        )
        return int(self.fc_channel_dl - self.cbw_dl / 2 + self.bw_ssb / 2 + self.offset_rb * 12 * self.scs_carrier)

    def f_off_ssb_carrier(self, f_ssb: int) -> int:
        return int(f_ssb - self.bw_ssb / 2 - (self.fc_channel_dl - self.cbw_dl / 2))

    @staticmethod
    def mod_zero(f: int, m: int = 15) -> bool:
        return not f % m

    def calculate_gscn(self):
        _f_ssb_min = self.f_ssb_min()
        if self.use_sync_raster:
            logger.info("Starting GSCN/F_SS selection from f_ssb_min:{}".format(_f_ssb_min))
            gscn = NrArfcn.f_to_gscn(f_ssb=_f_ssb_min, freq_raster=self.freq_raster)
            f_ss = NrArfcn.gscn_to_f(gscn=gscn, freq_raster=self.freq_raster)
            logger.info("Found f_ss:{} for gscn:{}".format(f_ss, gscn))
            if _f_ssb_min < 3000000 and self.freq_raster == 100:
                for i in range(2):
                    _f_off_ssb_carrier = self.f_off_ssb_carrier(f_ssb=f_ss)
                    if self.mod_zero(f=_f_off_ssb_carrier, m=15):
                        logger.info(
                            "f_off_ssb_carrier: {} for gscn:{} (f_ss:{}) is multiple "
                            "of 15kHz".format(_f_off_ssb_carrier, gscn, f_ss)
                        )
                        break
                    else:
                        gscn_old = gscn
                        gscn = gscn + 1
                        f_ss = NrArfcn.gscn_to_f(gscn=gscn, freq_raster=self.freq_raster)
                        logger.info(
                            "f_ss:{} for gscn:{} is not multiple of 15kHz. Trying {}".format(f_ss, gscn_old, gscn)
                        )
            # align to gscn raster
            gscn = NrArfcn.gscn_align_with_raster(gscn=gscn, scs_ssb=self.scs_ssb, band=self.band)
            f_ss = NrArfcn.gscn_to_f(gscn=gscn, freq_raster=self.freq_raster)
            logger.info("Selected GSCN:{}, F_SS:{}".format(gscn, f_ss))
            self.gscn = gscn
            self.f_ss = f_ss
        else:
            self.f_ss = _f_ssb_min

    def shift_channel_freq(self):
        logger.info("Adjusting channel frequency to align BWP start with Coreset0 start.")
        # get f_off_ssb_carrier - f_offset_rb difference
        f_diff = self.f_off_ssb_carrier(f_ssb=self.f_ss) - self.f_offset_rb
        logger.info(
            "f_diff(f_off_ssb_carrier:{} - f_offset_rb:{}) = {}".format(
                self.f_off_ssb_carrier(f_ssb=self.f_ss), self.f_offset_rb, f_diff
            )
        )
        # check f_diff within the range of max_k_ssb
        k_ssb = int(f_diff / self.scs_kssb)
        if k_ssb <= self.k_ssb_max:
            self.k_ssb = k_ssb
            logger.info(
                "f_diff (k_ssb:{}) <= k_ssb_max:{}. Channel frequency shift not needed".format(k_ssb, self.k_ssb_max)
            )
        else:
            logger.info(
                "f_diff (k_ssb:{}) > k_ssb_max:{}. Channel frequency shift needed".format(k_ssb, self.k_ssb_max)
            )
            # try to find the f_shift, k_ssb pair to make the f_shift with freq_raster step
            # if not possible set k_ssb to 0 and f_shift will f_diff
            f_shift_up = f_diff
            k_ssb = 0
            # for i in reversed(range(self.k_ssb_max+1)):
            for i in range(self.k_ssb_max + 1):
                _f_shift = f_diff - i * self.scs_kssb
                logger.info("trying _f_shift:{}, k_ssb:{}, f_k_ssb:{}".format(_f_shift, i, i * self.scs_kssb))
                if _f_shift > 0 and _f_shift % self.freq_raster == 0:
                    f_shift_up = _f_shift
                    k_ssb = i
                    break
            self.k_ssb = k_ssb
            if self.fc_channel_dl + f_shift_up <= self.fc_channel_dl_high:
                self.fc_channel_dl = self.fc_channel_dl + f_shift_up
                logger.info(
                    "Shifting Channel Frequency up by shift:{} to {}, k_ssb:{}".format(
                        f_shift_up, self.fc_channel_dl, k_ssb
                    )
                )
            else:
                gscn_prev = self.gscn - 1
                f_ss_prev = NrArfcn.gscn_to_f(gscn=gscn_prev, freq_raster=self.freq_raster)
                f_shift_down = self.f_ss - f_ss_prev - f_shift_up
                logger.info("Shifting Channel Frequency up not possible (out of allowed range). Shifting down needed.")
                self.f_ss = f_ss_prev
                self.gscn = gscn_prev
                logger.info("Using previous GSCN:{} (F_SS: {})".format(self.gscn, self.f_ss))
                self.fc_channel_dl = self.fc_channel_dl - f_shift_down
                logger.info(
                    "Shifting Channel Frequency down by shift:{} to {}, k_ssb:{}".format(
                        f_shift_down, self.fc_channel_dl, k_ssb
                    )
                )
            self._fc_dl_net()
            # make sure UL fc is adjusted to DL fc
            self.fc_channel_ul = NrArfcn.ul_f_from_dl(
                f=self.fc_channel_dl, band=self.band, freq_raster=self.freq_raster
            )
            self._fc_ul_net()

    def gscn_ss(self) -> Tuple[int, int]:
        if self.gscn == 0:
            self.calculate_gscn()
        return self.gscn, self.f_ss

    def offset_to_point_a(self) -> int:
        scs = 15 if NrArfcn.is_fr1(self.band) else 60
        return int((self.f_off_to_carrier + self.f_offset_rb) / (12 * scs))

    def point_a_offsets(self):
        if not self.is_sul:
            self.f_point_a = self.fc_dl - self.f_fc_to_point_a
        if not self.is_sdl:
            if self.is_sul:
                self.f_point_a_ul = self.fc_ul - self.f_fc_to_point_a
            else:
                self.f_point_a_ul = NrArfcn.ul_f_from_dl(f=self.f_point_a, band=self.band, freq_raster=self.freq_raster)
        if self.ssb_enabled:
            self.offset_to_pa = self.offset_to_point_a()

    def arfcns(self):
        if not self.is_sul:
            self.arfcn_point_a = NrArfcn.arfcn(self.f_point_a)
            logger.info("Absolute Frequency PointA ARFCN:{} (f_pointA:{})".format(self.arfcn_point_a, self.f_point_a))
        if not self.is_sdl:
            self.arfcn_point_a_ul = NrArfcn.arfcn(self.f_point_a_ul)
            if self.is_sul:
                logger.info("Absolute Frequency PointA ARFCN:{} (f_pointA:{})".format(self.arfcn_point_a_ul, self.f_point_a_ul))

        if self.ssb_enabled:
            self.arfcn_ssb = NrArfcn.arfcn(self.f_ss)
            logger.info("Absolute Frequency SSB ARFCN:{} (f_ss:{})".format(self.arfcn_ssb, self.f_ss))

    def _f_domain_resources(self):
        s_rb_coreset0 = self.offset_to_carrier + self.offset_coreset0_carrier
        s_rb_coreset_common = 6 * math.ceil(s_rb_coreset0 / 6)
        s_rb_coreset_common_bwpgrid = s_rb_coreset_common - self.offset_to_carrier
        s_rbg_coreset_common_bwpgrid = math.floor(s_rb_coreset_common_bwpgrid / 6)
        n_rbg_coreset_common = math.floor((s_rb_coreset0 + self.n_rb_coreset0 - s_rb_coreset_common) / 6)
        n_rb_coreset_common = 6 * n_rbg_coreset_common
        self.f_domain_res = (
            "".zfill(s_rbg_coreset_common_bwpgrid)
            + "1" * n_rbg_coreset_common
            + "".zfill(45 - s_rbg_coreset_common_bwpgrid - n_rbg_coreset_common)
        )
        logger.info(
            f"Calculated Common Coreset: s_rb={s_rb_coreset_common_bwpgrid} (s_crb={s_rb_coreset_common}), "
            f"n_rb={n_rb_coreset_common}, n_rbg={n_rbg_coreset_common}, bitm={self.f_domain_res}"
        )

    def get(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if not callable(k) and not k.startswith("_")}

    def calculate(self, log_params: bool = True) -> Dict[str, Any]:
        if self.ssb_enabled:
            self.calculate_gscn()
            self.shift_channel_freq()
        self.point_a_offsets()
        self.arfcns()
        if not self.is_sul:
            self._f_domain_resources()
        ret = self.get()
        if log_params:
            logger.info("Params: {}".format(pformat(ret)))
        return ret


class SsbPositions:
    """Class for calculation of the ssb positions

    Different properties return SSB position parameters (index, start symbols, slots, subframes) for the configured input.
    The initial input parameters can be modified using class properties.

    Example::

        >>> import nr_frequency
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

    """

    # from 38.213 sec. 4.1
    start_symbols = {
        ("caseA", 0): [i + 14 * n for n in (0, 1) for i in (2, 8)],
        ("caseA", 1): [i + 14 * n for n in (0, 1, 2, 3) for i in (2, 8)],
        ("caseB", 0): [i + 28 * n for n in (0,) for i in (4, 8, 16, 20)],
        ("caseB", 1): [i + 28 * n for n in (0, 1) for i in (4, 8, 16, 20)],
        ("caseC", 0): [i + 14 * n for n in (0, 1) for i in (2, 8)],
        ("caseC", 1): [i + 14 * n for n in (0, 1, 2, 3) for i in (2, 8)],
        ("caseD", 0): [
            i + 28 * n for n in (0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18) for i in (4, 8, 16, 20)
        ],
        ("caseE", 0): [i + 56 * n for n in (0, 1, 2, 3, 5, 6, 7, 8) for i in (8, 12, 16, 20, 32, 36, 40, 44)],
    }

    SF_IN_FRAME = 10
    SF_IN_HALFFRAME = 5
    SYMBOLS_IN_SLOT = 14

    def __init__(
        self,
        band: int,
        scs_common: int,
        scs_ssb: int,
        in_onegroup: str,
        group_presence: Optional[str] = None,
        ssb_periodicity: Optional[int] = 20,
    ):
        """SsbPositions class constructor

        Args:
            band: NR band
            scs_common: common subcarrier spacing
            scs_ssb: ssb subcarrier spacing
            in_onegroup: positionsInBusrt in one group
            group_presence: positionsInBurst group presence
            ssb_periodicity: SSB periodicity
        """
        self._band = band
        self._scs_common = scs_common
        self._scs_ssb = scs_ssb
        self._ssb_in_onegroup = in_onegroup
        self._ssb_group_presence = group_presence
        self._ssb_periodicity_scell = ssb_periodicity

    @property
    def scs_ssb(self) -> int:
        """int: ssb subcarrier spacing"""
        return self._scs_ssb

    @scs_ssb.setter
    def scs_ssb(self, scs: int):
        self._scs_ssb = scs

    @property
    def scs_common(self) -> int:
        """int: common subcarrier spacing"""
        return self._scs_common

    @scs_common.setter
    def scs_common(self, scs: int):
        self._scs_common = scs

    @property
    def band(self) -> int:
        """int: band"""
        return self._band

    @band.setter
    def band(self, band: int):
        self._band = band

    @property
    def in_onegroup(self) -> str:
        """str: positionsInBusrt in one group"""
        return self._ssb_in_onegroup

    @in_onegroup.setter
    def in_onegroup(self, in_onegroup: str):
        self._ssb_in_onegroup = in_onegroup

    @property
    def group_presence(self) -> str:
        """str: positionsInBurst group presence"""
        return self._ssb_in_onegroup

    @group_presence.setter
    def group_presence(self, group_presence: str):
        self._ssb_group_presence = group_presence

    @property
    def ssb_periodicity(self) -> int:
        """int: ssb periodicity serving cell in ms"""
        return self._ssb_periodicity_scell

    @ssb_periodicity.setter
    def ssb_periodicity(self, ssb_periodicity: int):
        self._ssb_periodicity_scell = ssb_periodicity

    @property
    def ssb_positions_in_burst_map(self):
        """str: positionsInBurst bitmap"""
        bitm = ""
        if self._ssb_group_presence and NrArfcn.is_fr1(self.band) is False:
            for g in list(self._ssb_group_presence):
                bitm += self._ssb_in_onegroup if int(g) else "".zfill(len(self._ssb_in_onegroup))
        else:
            bitm = self._ssb_in_onegroup
        return bitm

    @property
    def ssb_pattern(self) -> str:
        """str: ssb pattern (caseA, caseB, caseC, caseD"""
        return NrArfcn.gscn_raster(scs_ssb=self._scs_ssb, band=self._band).get("pattern")

    @property
    def ssb_candidates_index(self) -> List[int]:
        """:obj:`list` of :obj:`int`: SSB indices"""
        return [i for i, v in enumerate(list(self.ssb_positions_in_burst_map)) if v == "1"]

    @property
    def ssb_candidates_start_symbols(self) -> List[int]:
        """:obj:`list` of :obj:`int`: SSB start symbols"""
        mode = NrArfcn.band_mode(self._band)
        band_freqs = NrArfcn.bands.get(self._band)
        option = 0
        if self.ssb_pattern in ("caseA", "caseB") and band_freqs and band_freqs.get("f_dl_high") > 3000:
            option = 1
        elif self.ssb_pattern in ("caseC",) and band_freqs:
            if (
                (mode in ("FDD",) and band_freqs.get("f_dl_high") > 3000)
                or (mode in ("TDD", "SDL") and band_freqs.get("f_dl_high") > 2400)
                or (mode in ("TDD", "SUL") and band_freqs.get("f_ul_high") > 2400)
            ):
                option = 1

        s_symbols = self.start_symbols.get((self.ssb_pattern, option))
        return [
            s_symbols[i] for i, v in enumerate(list(self.ssb_positions_in_burst_map)) if i < len(s_symbols) and v == "1"
        ]

    @property
    def ssb_candidates_start_symbols_common_raster(self) -> List[int]:
        """:obj:`list` of :obj:`int`: SSB start symbols in a common symbol raster (using common scs)"""
        mi_ssb = Numerology.mi(self._scs_ssb)
        mi = Numerology.mi(self._scs_common)
        return [int(ssb_sym * 2 ** (mi - mi_ssb)) for ssb_sym in self.ssb_candidates_start_symbols]

    @property
    def ssb_candidates_slots(self) -> List[int]:
        """:obj:`list` of :obj:`int`: SSB slots in a common symbol raster (using common scs)"""
        return self.uniqlist(
            [int(sym / self.SYMBOLS_IN_SLOT) for sym in self.ssb_candidates_start_symbols_common_raster]
        )

    @property
    def ssb_candidates_subframes(self) -> List[int]:
        """:obj:`list` of :obj:`int`: SSB subframes in a common symbol raster (using common scs)"""
        return self.uniqlist([int(slot / self.slots_in_sf) for slot in self.ssb_candidates_slots])

    @property
    def ssb_candidates(self) -> Dict[int, Tuple[int, int, int]]:
        """:obj:`dict`: SSB canditates as dictionary with ssb index as key and SSB (start_symbol, slot, subframe) tuple as value"""
        return self._ssb_candidates()

    @property
    def ssb_candidates_relative(self) -> Dict[int, Tuple[int, int, int]]:
        """:obj:`dict`: SSB canditates as dictionary with ssb index as key and SSB (start_symbol, slot, subframe) tuple as value.
        SSB start symbols and slots are relative to subframe.
        """
        return self._ssb_candidates(relative=True)

    @property
    def slots_in_sf(self) -> int:
        """int: number of slots per subframe"""
        return self._slots_in_sf(self._scs_common)

    def ssb_candidate_slots_in_frame(self, sfn: int = 0) -> List[int]:
        """Method to calculate the slots with SSB for a given SystemFrameNumber

        Args:
            sfn: System Frame Number

         Returns:
            list of ssb slots
        """
        if (sfn * 10) % self.ssb_periodicity:
            return []
        else:
            slots = self.ssb_candidates_slots
            if self.ssb_periodicity < 10:
                slots = [slot + offset for slot in self.ssb_candidates_slots for offset in (0, self.slots_in_sf * 5)]
                slots.sort()
            return slots

    def _ssb_candidates(self, relative: bool = False) -> Dict[int, Tuple[int, int, int]]:
        l = []
        mi = Numerology.mi(self._scs_common)
        slots_in_sf = self._slots_in_sf(self._scs_common)
        for sym in self.ssb_candidates_start_symbols_common_raster:
            slot = int(sym / self.SYMBOLS_IN_SLOT)
            sf = int(slot / slots_in_sf)
            if relative:
                sym %= self.SYMBOLS_IN_SLOT
                slot %= slots_in_sf
            l.append((sym, slot, sf))
        return dict(zip(self.ssb_candidates_index, l))

    def _slots_in_sf(self, scs: int) -> int:
        mi = Numerology.mi(scs)
        return 2**mi

    def uniqlist(self, l: List[Any]) -> List[Any]:
        """Helper method make the list with unqiue values

        Args:
            l: list to search for unique values

         Returns:
            list with unique values
        """
        return list(OrderedDict.fromkeys(l))


def main():
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
    # c = Config(param={'scs_ssb': 15, 'scs_common': 15, 'scs_carrier': 15, 'fc_channel': 2130000,
    #                  'band': 66, 'bw': 40, 'pdcchConfigSib1': 100})
    c = Config(
        param={
            "scs_ssb": 30,
            "scs_common": 30,
            "scs_carrier": 30,
            "fc_channel": 3750000,
            "band": 77,
            "bw": 50,
            "pdcchConfigSib1": 164,
            "offset_to_carrier": 0,
        }
    )
    cell1_params = c.calculate()
    nom_cs = CaConfig.nominal_spacing(bw_c1=50, bw_c2=80, scs_c1=30, scs_c2=30, band=77)
    c2 = Config(
        param={
            "scs_ssb": 30,
            "scs_common": 30,
            "scs_carrier": 30,
            "fc_channel": c.fc_channel_dl + nom_cs,
            "band": 77,
            "bw": 80,
            "pdcchConfigSib1": 164,
            "offset_to_carrier": 0,
            "use_sync_raster": False,
        }
    )
    cell2_params = c2.calculate()


if __name__ == "__main__":
    main()
