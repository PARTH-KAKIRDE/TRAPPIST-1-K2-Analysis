# SFF

k2 = fits.open('/k2.fits')
data = k2[1].data
k2.close()

# Build DataFrame
df = pd.DataFrame(np.array(data))[['TIME', 'SAP_FLUX', 'SAP_FLUX_ERR', 'SAP_QUALITY', 'MOM_CENTR1', 'MOM_CENTR2', 'POS_CORR1', 'POS_CORR2']]

# Quality Filter and dropna
df_clean = df[df['SAP_QUALITY'] == 0].copy()
df_clean = df_clean.reset_index(drop=True)
print(df_clean[['TIME', 'SAP_FLUX', 'MOM_CENTR1', 'MOM_CENTR2']].isna().sum())
df_clean.shape

t_sff = df_clean['TIME'].values
f_sff = df_clean['SAP_FLUX'].values
f_err_sff = df_clean['SAP_FLUX_ERR'].values
cent_col_sff = df_clean['MOM_CENTR1'].values
cent_row_sff = df_clean['MOM_CENTR2'].values

lc_sff = lk.LightCurve(time=t_sff, flux=f_sff, flux_err=f_err_sff, centroid_col=cent_col_sff, centroid_row=cent_row_sff)
lc_sff

lc_sff.plot()

sff = lk.correctors.SFFCorrector(lc_sff)
lc_corr = sff.correct(windows = 2, bins = 30)
sff_flux = lc_corr.flux.value
sff_flux_norm = lc_corr.flux.value / np.median(lc_corr.flux.value)
std_sff_flux = np.std(sff_flux_norm)
print(std_sff_flux)
print(np.min(sff_flux_norm), np.max(sff_flux_norm))
lc_corr.plot()
