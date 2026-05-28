# GP on Centroid Position
sort_idx1 = np.argsort(p1_roll_corr)
flux_sorted = f_roll_corr[sort_idx1]
p1_sorted = p1_roll_corr[sort_idx1]

# Binning
bin_edges = np.linspace(p1_sorted.min(), p1_sorted.max(), 301)
print(len(bin_edges))
bin_indices = np.digitize(p1_sorted, bin_edges)
print(len(np.unique(bin_indices)))
unique_bins = np.unique(bin_indices)
binned_p1 = []
p1_binned_flux = []

for bin_idx in unique_bins:
  positions = np.where(bin_indices == bin_idx)[0]
  binned_p1.append(np.median(p1_sorted[positions]))
  p1_binned_flux.append(np.median(flux_sorted[positions]))

p1_binned = np.array(binned_p1)
flux_binned = np.array(p1_binned_flux)

print(len(p1_binned), len(flux_binned))
print(np.std(flux_binned))
print(p1_binned.min(), p1_binned.max())

# GP
kernel1 = celerite2.terms.SHOTerm(sigma=np.std(flux_binned), rho=0.1, tau=1.0)
gp1 = celerite2.GaussianProcess(kernel1, mean=1.0)
gp1.compute(p1_binned, yerr=np.std(flux_binned))
gp1_trend1 = gp1.predict(flux_binned, t=p1_sorted)
gp1_corrected_flux1 = flux_sorted / gp1_trend1

unsort_idx = np.argsort(sort_idx1)
restored = gp1_corrected_flux1[unsort_idx]
f_gp = restored/np.median(restored)

print(len(f_gp), f_gp.min(), f_gp.max())
print(np.std(f_gp), np.std(f_roll_corr))
print(len(f_gp), len(t_roll_corr))

plt.figure(figsize=(14,4))
plt.scatter(p1_roll_corr, f_gp, color ='red', s = 0.5, alpha = 0.3)
plt.ylabel('Flux GP')
plt.xlabel('P1 Roll Corr')
plt.title('K2 Rolling Effect Correlation')
plt.tight_layout()
plt.show()

plt.figure(figsize=(14,4))
plt.scatter(t_roll_corr, f_gp, color ='red', s = 0.5, alpha = 0.3)
plt.ylabel('Flux Roll Corr')
plt.xlabel('Time Roll Corr')
plt.title('K2 Rolling Effect Correlation')
plt.tight_layout()
plt.show()
