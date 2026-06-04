# Self-Flat-Fielding (SFF) Correction

**Status:** Abandoned
**Reference:** Vanderburg, A. & Johnson, J. A. (2014), *Publications of the Astronomical Society of the Pacific*, 126, 948.

## Method Overview

Self-Flat-Fielding (SFF) is a correction technique developed for K2 photometry that models the relationship between measured flux and spacecraft motion. The method removes roll-induced systematics by fitting the flux as a function of centroid position and dividing out the resulting trend.

In this project, the Lightkurve `SFFCorrector` was applied to the quality-filtered and normalised SAP flux. The implementation used:

* `windows = 2`
* `bins = 30`

These parameters divide the spacecraft roll motion into segments and fit a spline to the flux–position relationship within each segment.

## Results

| Metric                               | Value     |
| ------------------------------------ | --------- |
| Standard deviation before correction | 2,091 ppm |
| Standard deviation after correction  | 2,858 ppm |
| Change                               | +36.7%    |

The correction increased the scatter in the light curve, indicating that the systematic noise was amplified rather than removed.

## Reason for Rejection

SFF performs best when the flux–centroid relationship is densely sampled and the signal-to-noise ratio within each centroid-position bin is sufficiently high.

Although SFF is highly effective for many K2 targets, TRAPPIST-1 is a relatively faint M-dwarf (Kepler magnitude ≈ 12.3). At this brightness level, individual centroid-position bins contain insufficient photon counts to constrain the spline model reliably. As a result, the fitted correction becomes noise-dominated, and dividing by the spline introduces additional scatter into the light curve.

Because the corrected light curve exhibited substantially higher noise than the input data, SFF was not pursued further.

## Code Location

The implementation is preserved in the notebook as a commented-out section titled **"SFF"** immediately after the Exploratory Data Analysis (EDA) stage.

The block contains:

* LightCurve object construction
* `SFFCorrector` initialization
* correction execution
* pre/post-correction noise comparison

## Subsequent Development

Following the failure of SFF, the analysis moved to polynomial decorrelation using the `POS_CORR1` and `POS_CORR2` centroid columns.

This approach reduced the scatter to **1,790 ppm**, outperforming both the original light curve and the SFF-corrected version. Polynomial decorrelation subsequently became the baseline against which all later correction methods were evaluated.

