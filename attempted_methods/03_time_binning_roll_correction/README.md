# Time Binning as Roll-Systematic Correction

**Status:** Abandoned

## Method Overview

Following the limited success of polynomial roll correction, an alternative hypothesis was tested: whether temporal binning could reduce the dominant roll systematic without requiring an explicit correction model.

The underlying idea was that averaging multiple 60-second cadences into a larger time bin might suppress the rapid flux variations associated with K2 spacecraft motion. If successful, this would provide a simple and computationally inexpensive alternative to more sophisticated detrending techniques.

The implementation consisted of the following steps:

1. Start with the polynomial-corrected light curve (1,790 ppm scatter).
2. Divide the time series into 10-minute intervals using `np.digitize()`.
3. Compute the median flux within each bin.
4. Construct a binned light curve.
5. Compare the scatter before and after binning.

## Results

| Metric                            | Value     |
| --------------------------------- | --------- |
| Standard deviation before binning | 1,790 ppm |
| Standard deviation after binning  | 1,794 ppm |
| Change                            | +0.2%     |

The resulting scatter was effectively unchanged. Any difference was well below the level required to indicate a meaningful improvement.

## Reason for Rejection

The failure of this approach is explained by the distinction between **white noise** and **correlated noise**.

### White Noise Behaviour

For uncorrelated noise, averaging multiple measurements reduces the noise according to:

σ_binned = σ / √N

where (N) is the number of samples within a bin.

For a 10-minute bin containing approximately ten 60-second cadences, purely white noise would be expected to decrease by roughly:

sqrt(10) ≈ 3.16×

This principle is widely used in photometric data analysis.

### Correlated Noise Behaviour

The dominant systematic in K2 data is not white noise. Instead, it is caused by spacecraft roll motion and exhibits a characteristic correlation timescale of approximately six hours between thruster firings.

A 10-minute bin is entirely contained within this six-hour correlation length. Consequently, every cadence inside the bin experiences nearly the same roll-induced flux offset.

Averaging multiple measurements that share the same systematic bias does not remove the bias. The median of several identically biased measurements remains biased by essentially the same amount.

As a result:

* photon noise is slightly reduced,
* roll-systematic noise remains unchanged,
* overall scatter shows no meaningful improvement.

## Root Cause Analysis

This experiment demonstrated that the limiting noise source was not high-frequency photon noise but rather a low-frequency, strongly correlated systematic associated with spacecraft pointing drift.

Because the roll systematic operates on timescales far longer than the chosen bin width, temporal averaging cannot serve as a substitute for explicit systematic correction.

The result provided an important diagnostic insight: future improvements would require modelling the origin of the systematic rather than averaging over it.

## Code Location

The time-binning experiment appears later in the notebook than the other attempted roll-correction methods.

The implementation is located after the TPF-based PLD sections and is followed by a markdown note documenting:

* the negligible change in scatter,
* the correlated-noise interpretation,
* and the decision to abandon binning as a correction strategy.

## Subsequent Development

The failure of centroid-based corrections and time-domain averaging motivated a fundamental change in strategy.

Rather than continuing to operate on the extracted light curve, the analysis returned to the raw Target Pixel File (TPF) data. This enabled the use of Pixel Level Decorrelation (PLD), which models spacecraft systematics directly from pixel-level information rather than from derived flux measurements.

The transition to TPF-based processing is documented in:

* **04_lightkurve_pld_corrector**
* **05_global_pld**

and ultimately led to the final adopted per-chunk PLD pipeline.
