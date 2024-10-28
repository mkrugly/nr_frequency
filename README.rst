nr_frequency
============

The `nr_frequency` module provides classes for consistent generation of frequency related parameters such as Arfcn for SSB,
carrier frequency FC, reference PointA, relative offsets e.g. OffsetToPointA etc. making sure the SSB frequency is in
the sync raster and carrier frequency in the channel raster within the defined band frequency range.

It provides methods for handling frequency to arfcn and back, Uplink from Downlink frequencies (and vice versa),
calculation of carrier aggregation related parameters like nominal channel spacing or guardbands.

The implementation is based on the TS 38.104 and TS 38.508. Currently parameters are calculated with the assumption
that the Control resource set zero (Coreset0) and Synchronization Signal Block (SS Block) should be as close as possible
to the beginning of the initial BWP (Coreset0 shall start with the start of initial BWP).

All the input and output frequencies are expressed in kHz.

Moreover it provides methods for the resolution of the SSB candidates possitions (index, start symbols, slots, subframes)
based on the TS 38.213 sec. 4.1

With only a few optional input parameters the module provides an optimal set of consistent NR settings for different scenarios.