# Generates BostonHarbor training samples
# Combining the occupancy grid and planned path results
# Each sample is:
# [ waypoint | initial point | goal point | flattened occupancy grid ]

import numpy as np

# Options
dataDir = "data/"
pathFilesFile = "BostonHarbor_paths.txt"
rasterFile = "data/full_shrink.asc"
sampleOutFile = "BostonHarbor_Data.npz"

# Load paths
with open(pathFilesFile) as f:
    pathFiles = f.readlines()
pathFiles = [x.strip() for x in pathFiles]
paths = [np.loadtxt(dataDir + "/" + path, delimiter=",") for path in pathFiles]
print("Loaded {} paths ({})".format(len(paths), pathFilesFile))

# Load occupancy grid
occgrid = np.loadtxt(rasterFile, skiprows=6).astype("uint8")
print("Loaded {}x{} occupancy grid ({})".format(occgrid.shape[0], occgrid.shape[1], rasterFile))
occgrid = np.nan_to_num(occgrid, nan=1)
occgrid = occgrid.flatten()

# Create sample
samples = []
for path in paths:
    init = path[0]
    goal = path[-1]
    for w in path[1:-2]:
        samples.append([w[1], w[0], init[1], init[0], goal[1], goal[0]])

samples = np.array(samples).astype("uint8")

occgrids = np.tile(occgrid, (samples.shape[0], 1))
samples = np.concatenate((samples, occgrids), axis=1)

print("Generated {} samples of length {}".format(samples.shape[0], samples.shape[1]))

np.savez_compressed(sampleOutFile, data=samples)
print("Saved to {}".format(sampleOutFile))
