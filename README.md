TRAPPIST-1 K2 CAMPAIGN 12 — EXOPLANET TRANSIT ANALYSIS
=======================================================


OVERVIEW
--------
This project applies an end-to-end photometric pipeline to NASA K2 Campaign
12 short-cadence data for TRAPPIST-1 (EPIC 246199087), an ultra-cool M-dwarf
40.5 light-years from Earth hosting seven known Earth-sized planets.

Starting from raw pixel data, the pipeline works through systematic noise
correction, blind transit detection, false positive screening, transit
parameter fitting, timing variation analysis, and habitability assessment —
deriving all orbital and physical parameters directly from the photometry.

Transit detection used two independent algorithms: Transit Least Squares
(TLS), an established shape-matched filter, and CETRA, a GPU-based likelihood
ratio search. Running both allowed a direct benchmark of their sensitivity,
period recovery accuracy, and computational cost on the same dataset.

Detection strategy was partially blind. Inner planets b, c, and d were
found through an iterative search with no period priors. Outer planets e, f,
and g required targeted searches using period windows informed by the known
resonance chain structure. Published periods were then used as inputs for
transit model fitting and all downstream physical characterisation.

The project was built as a guided learning exercise in observational astronomy
and scientific Python, and is designed to be adaptable to comparable transit
photometry datasets with moderate reconfiguration.

For full methodology, results, and pipeline documentation see:
docs/TRAPPIST1_K2_Complete_Handover.docx


TARGET AND DATASET
------------------
Target      :  TRAPPIST-1 (EPIC 246199087)  
Campaign    :  K2 Campaign 12 (December 2016 to March 2017)  
Cadence     :  60-second short cadence  
Clean points:  103,812 after quality filtering and PLD correction  
Baseline    :  79 days  
Noise floor :  706 ppm after 10-minute binning  
Detections  :  6 planets  
               b, c, d — confirmed  
               e, f, g — strong candidates  


GETTING STARTED
---------------
1. Clone the repository

       git clone https://github.com/yourusername/TRAPPIST-1-K2-Analysis.git

2. Install dependencies

       pip install -r requirements.txt

3. Download the data

   Follow the instructions in data/README.txt to download the K2 Campaign 12
   light curve FITS file and Target Pixel File for EPIC 246199087 from the
   MAST archive.

4. Place the downloaded files in your Google Drive folder

       k2.fits
       trappist1_tpf.fits

   Then update the DRIVE variable in the first notebook cell to point to
   that folder:

       DRIVE = "/content/drive/MyDrive/YourFolderName"

5. Run the notebook

   Open notebooks/Trappist_Kepler_K2.ipynb and execute cells sequentially
   from top to bottom.

   Google Colab execution is supported. GPU runtime is required for the
   CETRA transit search cells (Runtime > Change runtime type > T4 GPU).


DEPENDENCIES
------------
1. astropy
2. numpy
3. scipy
4. pandas
5. matplotlib
6. celerite2
7. lightkurve
8. transitleastsquares
9. cetra
10. batman-package 


ACKNOWLEDGEMENTS
----------------
Data from the MAST archive at the Space Telescope Science Institute.
Uses Astropy (Astropy Collaboration 2013, 2018), Transit Least Squares
(Hippke and Heller 2019, A&A 623, A39), batman (Kreidberg 2015, PASP 127,
1161), and CETRA. Habitable zone boundaries from Kopparapu et al. 2013
(ApJ 765, 131).
