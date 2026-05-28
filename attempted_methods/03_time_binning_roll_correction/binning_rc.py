# Time Binning Roll Correction

bins = int((times.max() - times.min()) / (10/1440))
bin_edges1 = np.linspace(times.min(), times.max(), bins)
print(len(bin_edges1))
bin_indices1 = np.digitize(times, bin_edges1)
print(len(np.unique(bin_indices1)))
unique_bins1 = np.unique(bin_indices1)
t_binned = []
f_binned = []

for bin_idx1 in unique_bins1:
  positions1 = np.where(bin_indices1 == bin_idx1)[0]
  t_binned.append(np.median(times[positions1]))
  f_binned.append(np.median(f_pld[positions1]))

t_binned = np.array(t_binned)
f_binned = np.array(f_binned)

print(len(t_binned), len(f_binned))
print(np.isnan(t_binned).sum())
print(np.isnan(f_binned).sum())
print(np.std(f_binned))
