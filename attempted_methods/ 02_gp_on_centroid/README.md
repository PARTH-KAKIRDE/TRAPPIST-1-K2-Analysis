# Gaussian Process Modelling on Centroid Position

**Status:** Abandoned

## Method Overview

Following the polynomial roll correction stage, which reduced the light-curve scatter to **1,790 ppm**, a Gaussian Process (GP) approach was explored to model the flux–centroid relationship more flexibly than a low-order polynomial.

Unlike the earlier GP detrending stage, which modelled stellar variability as a function of time, this experiment treated the roll systematic as a function of spacecraft position. The underlying assumption was that flux variations induced by K2 roll motion could be represented by a smooth nonlinear mapping between centroid position and measured flux.

The implementation consisted of the following steps:

1. Sort the quality-filtered, normalised flux by `POS_CORR1`, converting the problem from the time domain to the position domain.
2. Bin the sorted flux into 300 bins across the centroid-position range.
3. Fit a `celerite2` SHOTerm Gaussian Process to the binned flux-position relation.
4. Predict the GP trend at all cadence positions.
5. Divide the predicted trend out of the original flux.
6. Restore the original temporal ordering of the light curve.

## Results

| Metric                               | Value     |
| ------------------------------------ | --------- |
| Standard deviation before correction | 1,790 ppm |
| Standard deviation after correction  | 1,778 ppm |
| Change                               | -0.7%     |

The correction produced only a marginal reduction in scatter, corresponding to an improvement of approximately **12 ppm**.

More importantly, a significant edge artefact appeared near the extremes of the centroid-position distribution. In these regions, the training data became sparse and the GP prediction approached zero. Dividing the flux by a near-zero model resulted in artificial amplification of the corrected flux, producing excursions as large as **1.313** (31.3% above the nominal baseline).

These artefacts were substantially larger than any expected planetary transit signal and rendered the corrected light curve unsuitable for transit detection.

## Reason for Rejection

The method failed for two independent reasons.

### 1. Negligible Noise Improvement

The reduction from 1,790 ppm to 1,778 ppm represented a change of only 12 ppm. This improvement is comparable to the uncertainty associated with the standard deviation estimate itself and therefore cannot be considered statistically meaningful.

### 2. Severe Edge Amplification Artefacts

Sparse sampling at the edges of the centroid-position distribution caused the GP model to extrapolate poorly. As the predicted trend approached zero, the flux correction became unstable and generated large artificial features that would likely be mistaken for astrophysical signals.

## Root Cause Analysis

The fundamental limitation of this approach is that the flux–centroid relationship is not stationary throughout the campaign.

The relationship between spacecraft position and measured flux changes:

* between observing chunks,
* within individual chunks,
* and during periods of detector thermal settling.

A single GP fitted across the entire centroid-position range therefore attempts to model multiple different relationships simultaneously. The resulting model represents only an average behaviour and fails to capture the local variations that dominate the systematic noise.

Consequently, the GP fit provides little improvement in the well-sampled regions while producing unstable behaviour in sparsely sampled regions.

## Code Location

The implementation is preserved in the notebook as a commented-out section titled **"GP on Centroid Position"** immediately after the polynomial roll-correction stage.

The block contains:

* centroid sorting logic,
* binning operations,
* `celerite2` GP construction,
* prediction and correction steps,
* and diagnostic plots used to identify the edge-amplification artefact.

A markdown note immediately following the code documents the observed failure mode and the resulting decision to abandon the method.

## Subsequent Development

After the failure of centroid-domain Gaussian Process modelling, the analysis moved to time-binning approaches aimed at suppressing correlated roll noise through cadence averaging.

This work is documented in **03_time_binning_roll_correction**.

